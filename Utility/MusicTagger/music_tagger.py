#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
music_tagger.py —— 批量给音频文件写入歌词 + 封面，导入 iPhone「音乐」播放时自动显示。

特点：跨机器通用。只依赖 Python 3.9+ 和 mutagen，歌词与封面全部联网自动获取，
      不需要在本地预先准备任何素材文件。

安装依赖（每台电脑执行一次）：
    python3 -m pip install mutagen

常用用法：
    python3 music_tagger.py "<音乐文件夹>"                    # 递归处理，输出到 <文件夹>/_tagged
    python3 music_tagger.py "<音乐文件夹>" --dry-run --limit 5  # 只看匹配结果，不写文件
    python3 music_tagger.py "<音乐文件夹>" --out "~/Desktop/out" --jobs 4
    python3 music_tagger.py "<单个文件.m4a>"                    # 单文件也可以

数据源：
    歌词 —— LRCLIB (https://lrclib.net)，免费开放接口
    封面 —— iTunes Search API，自动在 US/TW/HK 区之间兜底

规则：
    * 音频真实格式按文件头判断，不看扩展名（m4a 被命名成 .mp3 也能正确处理）
    * 原文件永不修改，一律输出副本
    * 匹配结果写入 report.csv，低置信度的会单独标出供人工复核
    * 结果缓存在 ~/.cache/music-tagger/，重复运行不重复请求网络
"""

import argparse
import csv
import hashlib
import json
import os
import re
import shutil
import sys
import threading
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

try:
    from mutagen import File as MutagenFile
    from mutagen.id3 import (
        ID3, ID3NoHeaderError, APIC, USLT, TIT2, TPE1, TALB, TRCK, TDRC, TCON,
    )
    from mutagen.flac import FLAC, Picture
    from mutagen.mp4 import MP4, MP4Cover
except ImportError:
    sys.exit("缺少依赖，请先执行： python3 -m pip install mutagen")

UA = "music-tagger/1.0 (local script)"
EXT_FOR = {"mp3": ".mp3", "mp4": ".m4a", "flac": ".flac", "wav": ".wav"}

# 嵌入封面尺寸。iOS「音乐」通过 Finder 同步时，嵌入封面过大会导致封面不显示
# （实测 1400x1400 / 460KB 会出问题，600x600 / ~35KB 稳定），所以默认取 600。
COVER_PX = os.environ.get("MUSIC_TAGGER_COVER_PX", "600x600")

# 手动素材覆盖：命令行给了 --cover-file / --lyrics-file / --lrc-file / --title 等时填充。
# 用于联网查不到的歌（冷门、翻唱、自录、独立音乐）—— 此时跳过网络，直接用本地素材。
OVERRIDE = {
    "cover_bytes": None,
    "plain_lyrics": None,
    "synced_lyrics": None,
    "title": None,
    "artist": None,
    "album": None,
    "year": None,
    "genre": None,
}
SUPPORTED = set(EXT_FOR)

# 线上商店区域：中国区搜不到中文歌，必须用这几个
STOREFRONTS = ["TW", "HK", "US"]

BAD_WORDS = ("live", "現場", "现场", "演唱會", "演唱会", "remix", "instrumental",
             "karaoke", "伴奏", "翻自", "cover", "demo", "acoustic version")

_print_lock = threading.Lock()
_itunes_lock = threading.Lock()
_itunes_last = [0.0]
ITUNES_INTERVAL = 1.2  # 秒，iTunes Search API 约 20 次/分钟，留足余量


def log(msg):
    with _print_lock:
        print(msg, flush=True)


def itunes_json(params):
    """iTunes 接口有频率限制：全局串行 + 最小间隔，避免批量时被拒。"""
    with _itunes_lock:
        wait = ITUNES_INTERVAL - (time.time() - _itunes_last[0])
        if wait > 0:
            time.sleep(wait)
        try:
            return http_json("https://itunes.apple.com/search", params)
        finally:
            _itunes_last[0] = time.time()


# ---------------------------------------------------------------- 网络

def http_json(url, params=None, retries=4, timeout=25):
    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            last = e
            if e.code in (429, 500, 502, 503, 504):
                time.sleep(1.5 * (i + 1))
                continue
            raise
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            last = e
            time.sleep(1.0 * (i + 1))
    raise last if last else RuntimeError("unknown error")


def http_bytes(url, retries=3, timeout=40):
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as e:
            last = e
            time.sleep(1.0 * (i + 1))
    raise last


# ---------------------------------------------------------------- 文本匹配

def norm(s):
    if not s:
        return ""
    s = unicodedata.normalize("NFKC", s).lower()
    s = re.sub(r"[^\w\u4e00-\u9fff]+", "", s)
    return s


def sim(a, b):
    """0~1 相似度，兼容简繁与中英混排。"""
    na, nb = norm(a), norm(b)
    if not na or not nb:
        return 0.0
    if na == nb:
        return 1.0
    if na in nb or nb in na:
        return 0.85
    sa, sb = set(na), set(nb)
    return len(sa & sb) / max(len(sa), len(sb))


def has_bad_word(s):
    low = (s or "").lower()
    return any(w in low for w in BAD_WORDS)


# ---------------------------------------------------------------- 格式

def detect_format(path: Path) -> str:
    with open(path, "rb") as fh:
        head = fh.read(12)
    if len(head) < 12:
        return "unknown"
    if head[4:8] == b"ftyp":
        return "mp4"
    if head[:4] == b"fLaC":
        return "flac"
    if head[:4] == b"RIFF" and head[8:12] == b"WAVE":
        return "wav"
    if head[:4] == b"OggS":
        return "ogg"
    if head[:3] == b"ID3":
        return "mp3"
    if head[0] == 0xFF and (head[1] & 0xE0) == 0xE0:
        return "mp3"
    return "unknown"


def audio_duration(path: Path):
    try:
        f = MutagenFile(path)
        if f is not None and getattr(f, "info", None):
            return float(f.info.length)
    except Exception:
        pass
    return None


def guess_mime(data: bytes) -> str:
    if data[:3] == b"\xff\xd8\xff":
        return "image/jpeg"
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return "image/png"
    return "image/jpeg"


# ---------------------------------------------------------------- 文件名解析

def parse_filename(stem: str):
    """把 "歌名-歌手" / "01. 歌名 - 歌手" / "歌手 - 歌名" 解析成 (title, artist)。"""
    s = re.sub(r"^\s*\d{1,3}[\.\-、_)]\s*", "", stem).strip()
    for sep in ("-", "–", "—", "_"):
        if sep in s:
            left, right = s.rsplit(sep, 1)
            left, right = left.strip(), right.strip()
            if left and right:
                # 约定是「歌名-歌手」，右侧更像人名（短于左侧）时保持原序
                return left, right
    return s, ""


# ---------------------------------------------------------------- 缓存

class Cache:
    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def key(self, title, artist):
        h = hashlib.sha1(f"{norm(artist)}|{norm(title)}".encode()).hexdigest()[:16]
        return self.root / h

    def get(self, title, artist):
        d = self.key(title, artist)
        meta = d / "meta.json"
        if not meta.exists():
            return None
        try:
            data = json.loads(meta.read_text(encoding="utf-8"))
        except Exception:
            return None
        cov = d / "cover.jpg"
        if cov.exists():
            data["cover_bytes"] = cov.read_bytes()
        return data

    def put(self, title, artist, data, cover_bytes=None):
        d = self.key(title, artist)
        d.mkdir(parents=True, exist_ok=True)
        payload = {k: v for k, v in data.items() if k != "cover_bytes"}
        (d / "meta.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        if cover_bytes:
            (d / "cover.jpg").write_bytes(cover_bytes)
        if data.get("plain_lyrics"):
            (d / "lyrics.txt").write_text(data["plain_lyrics"], encoding="utf-8")


# ---------------------------------------------------------------- 歌词

def pick_lrclib(cands, title, artist, dur):
    best, best_score = None, -99.0
    for c in cands:
        s = 0.0
        cd = c.get("duration")
        if cd and dur:
            diff = abs(float(cd) - float(dur))
            if diff <= 2:
                s += 4.0
            elif diff <= 5:
                s += 2.0
            elif diff > 12:
                s -= 3.0
        s += 2.0 * sim(title, c.get("trackName"))
        s += 1.5 * sim(artist, c.get("artistName"))
        if has_bad_word(c.get("trackName")):
            s -= 1.5
        if s > best_score:
            best, best_score = c, s
    return best, best_score


def fetch_lyrics(title, artist, dur):
    query = f"{title} {artist}".strip()
    cands = http_json("https://lrclib.net/api/search", {"q": query})
    if not isinstance(cands, list) or not cands:
        return None
    best, score = pick_lrclib(cands, title, artist, dur)
    if best is None or score < 2.0:
        return None
    if not best.get("plainLyrics"):
        return None

    # search 结果不一定带 syncedLyrics，按 id 再取一次完整记录
    synced = best.get("syncedLyrics")
    plain = best.get("plainLyrics")
    if not synced and best.get("id"):
        try:
            full = http_json(f"https://lrclib.net/api/get/{best['id']}")
            synced = full.get("syncedLyrics")
            plain = plain or full.get("plainLyrics")
        except Exception:
            pass

    return {
        "plain_lyrics": plain,
        "synced_lyrics": synced or "",
        "lrclib_track": best.get("trackName"),
        "lrclib_artist": best.get("artistName"),
        "lrclib_album": best.get("albumName"),
        "lyrics_score": round(score, 2),
    }


# ---------------------------------------------------------------- 封面

def pick_itunes(results, title, artist):
    best, best_score = None, -99.0
    for r in results:
        s = 2.0 * sim(title, r.get("trackName"))
        s += 1.5 * sim(artist, r.get("artistName"))
        if has_bad_word(r.get("trackName")) or has_bad_word(r.get("collectionName")):
            s -= 2.0
        if r.get("artworkUrl100"):
            s += 0.5
        if s > best_score:
            best, best_score = r, s
    return best, best_score


def fetch_cover(title, artist):
    last_err = None
    for store in STOREFRONTS:
        try:
            d = itunes_json({
                "term": f"{artist} {title}".strip(),
                "entity": "song", "limit": 8, "country": store,
            })
        except Exception as e:
            last_err = e
            continue
        results = d.get("results") or []
        if not results:
            continue
        best, score = pick_itunes(results, title, artist)
        if best is None or score < 1.5:
            continue
        raw = best.get("artworkUrl100", "")
        url = re.sub(r"/\d+x\d+bb\.(?:jpg|png)$", f"/{COVER_PX}bb.jpg", raw) if raw else ""
        if not url:
            continue
        try:
            data = http_bytes(url)
            if len(data) > 5000:
                return {
                    "cover_bytes": data,
                    "itunes_album": best.get("collectionName"),
                    "itunes_track": best.get("trackName"),
                    "itunes_artist": best.get("artistName"),
                    "itunes_year": (best.get("releaseDate") or "")[:4],
                    "itunes_track_no": best.get("trackNumber"),
                    "itunes_track_count": best.get("trackCount"),
                    "itunes_genre": best.get("primaryGenreName"),
                    "store": store,
                    "cover_score": round(score, 2),
                }
        except Exception as e:
            last_err = e
            continue
    if last_err:
        log(f"      封面获取失败：{type(last_err).__name__}")
    return None


# ---------------------------------------------------------------- 写标签

def tag_mp3(path, lyrics, cover, m):
    try:
        tags = ID3(path)
    except ID3NoHeaderError:
        tags = ID3()
    tags.delall("APIC")
    tags.delall("USLT")
    if cover:
        tags.add(APIC(encoding=0, mime=guess_mime(cover), type=3, desc="Cover", data=cover))
    if lyrics:
        tags.add(USLT(encoding=1, lang="eng", desc="", text=lyrics))
    tags.add(TIT2(encoding=1, text=m["title"]))
    tags.add(TPE1(encoding=1, text=m["artist"]))
    if m["album"]:
        tags.add(TALB(encoding=1, text=m["album"]))
    if m["track"]:
        tags.add(TRCK(encoding=1, text=m["track"]))
    if m["year"]:
        tags.add(TDRC(encoding=1, text=m["year"]))
    if m["genre"]:
        tags.add(TCON(encoding=1, text=m["genre"]))
    tags.save(path, v2_version=3)


def tag_mp4(path, lyrics, cover, m):
    audio = MP4(path)
    if audio.tags is None:
        audio.add_tags()
    if lyrics:
        audio["\xa9lyr"] = [lyrics]
    if cover:
        fmt = MP4Cover.FORMAT_JPEG if guess_mime(cover) == "image/jpeg" else MP4Cover.FORMAT_PNG
        audio["covr"] = [MP4Cover(cover, imageformat=fmt)]
    audio["\xa9nam"] = [m["title"]]
    audio["\xa9ART"] = [m["artist"]]
    if m["album"]:
        audio["\xa9alb"] = [m["album"]]
    if m["year"]:
        audio["\xa9day"] = [m["year"]]
    if m["genre"]:
        audio["\xa9gen"] = [m["genre"]]
    if m["track"] and "/" in m["track"]:
        try:
            a, b = m["track"].split("/")
            audio["trkn"] = [(int(a), int(b))]
        except ValueError:
            pass
    audio.save()


def tag_flac(path, lyrics, cover, m):
    audio = FLAC(path)
    if lyrics:
        audio["LYRICS"] = lyrics
    audio["TITLE"] = m["title"]
    audio["ARTIST"] = m["artist"]
    if m["album"]:
        audio["ALBUM"] = m["album"]
    if m["year"]:
        audio["DATE"] = m["year"]
    if m["genre"]:
        audio["GENRE"] = m["genre"]
    if cover:
        audio.clear_pictures()
        pic = Picture()
        pic.type = 3
        pic.mime = guess_mime(cover)
        pic.data = cover
        audio.add_picture(pic)
    audio.save()


def tag_wav(path, lyrics, cover, m):
    """WAV 只能靠 ID3 chunk 存标签，兼容性弱于 m4a/mp3，但总比没有强。"""
    from mutagen.wave import WAVE

    audio = WAVE(path)
    if audio.tags is None:
        audio.add_tags()
    t = audio.tags
    for fid in list(t.keys()):
        if fid.startswith(("APIC", "USLT")):
            del t[fid]
    if cover:
        t.add(APIC(encoding=0, mime=guess_mime(cover), type=3, desc="Cover", data=cover))
    if lyrics:
        t.add(USLT(encoding=1, lang="eng", desc="", text=lyrics))
    t.add(TIT2(encoding=1, text=m["title"]))
    t.add(TPE1(encoding=1, text=m["artist"]))
    if m["album"]:
        t.add(TALB(encoding=1, text=m["album"]))
    audio.save()


# ---------------------------------------------------------------- 主流程

def gather_info(src: Path, title: str, artist: str, cache: Cache, do_lyrics: bool):
    """阶段一：只取歌词，可多线程并发。返回 (info, 是否命中缓存)。"""
    # 手动给了歌词或封面（哪怕只是其中之一）就完全跳过网络，交给 finish_file 注入
    if OVERRIDE["plain_lyrics"] is not None or OVERRIDE["cover_bytes"] is not None:
        return {}, False

    cached = cache.get(title, artist)
    if cached is not None:
        return cached, True
    info = {}
    if do_lyrics:
        try:
            got = fetch_lyrics(title, artist, audio_duration(src))
            if got:
                info.update(got)
        except Exception:
            pass
    return info, False


def finish_file(src: Path, rel: Path, info: dict, was_cached: bool,
                out_root: Path, cache: Cache, do_cover=True, dry_run=False,
                note: str = ""):
    """阶段二：补封面（全局节流串行）→ 写标签 → 返回报告行。"""
    fmt = detect_format(src)
    title, artist = parse_filename(src.stem)
    row = {
        "file": str(rel), "format": fmt, "title": "", "artist": "", "album": "",
        "year": "", "lyrics": "无", "lyrics_chars": 0, "lrc": "无",
        "cover": "无", "source": "", "status": "", "note": note,
    }
    if fmt not in SUPPORTED:
        row["status"] = "skip"
        row["note"] = "不支持的格式"
        return row

    # 手动素材覆盖：优先级最高，注入后不再联网、不写缓存
    manual = any(OVERRIDE[k] is not None
                 for k in ("plain_lyrics", "synced_lyrics", "cover_bytes"))
    if manual:
        if OVERRIDE["plain_lyrics"] is not None:
            info["plain_lyrics"] = OVERRIDE["plain_lyrics"]
            info["lyrics_score"] = 99
        if OVERRIDE["synced_lyrics"] is not None:
            info["synced_lyrics"] = OVERRIDE["synced_lyrics"]
        if OVERRIDE["cover_bytes"] is not None:
            info["cover_bytes"] = OVERRIDE["cover_bytes"]
            info["cover_score"] = 99
        info["store"] = "手动"
        row["note"] = (row["note"] + " 手动素材").strip()

    if do_cover and not info.get("cover_bytes"):
        try:
            got = fetch_cover(title, artist)
            if got:
                info.update(got)
        except Exception as e:
            row["note"] = (row["note"] + f" 封面异常{type(e).__name__}").strip()

    if manual:
        pass  # 手动素材是针对单个文件的，写缓存会污染同名查询
    elif not was_cached:
        cache.put(title, artist, info, info.get("cover_bytes"))
    else:
        row["note"] = (row["note"] + " 缓存").strip()

    lyrics = info.get("plain_lyrics") or ""
    cover = info.get("cover_bytes") or b""

    meta = {
        "title": info.get("lrclib_track") or info.get("itunes_track") or title,
        "artist": info.get("lrclib_artist") or info.get("itunes_artist") or artist,
        "album": info.get("lrclib_album") or info.get("itunes_album") or "",
        "year": info.get("itunes_year") or "",
        "genre": info.get("itunes_genre") or "",
        "track": "",
    }
    tn, tc = info.get("itunes_track_no"), info.get("itunes_track_count")
    if tn and tc:
        meta["track"] = f"{tn}/{tc}"

    # 手动指定的元数据优先级最高
    for k in ("title", "artist", "album", "year", "genre"):
        if OVERRIDE[k]:
            meta[k] = OVERRIDE[k]

    row.update({
        "title": meta["title"], "artist": meta["artist"], "album": meta["album"],
        "year": meta["year"],
        "lyrics": "有" if lyrics else "无", "lyrics_chars": len(lyrics),
        "cover": "有" if cover else "无",
        "source": info.get("store", ""),
    })

    low_conf = False
    if lyrics and info.get("lyrics_score", 99) < 3.5:
        low_conf = True
    if cover and info.get("cover_score", 99) < 2.5:
        low_conf = True
    row["status"] = "low" if low_conf else "ok"

    # 同步歌词单独落一个 .lrc 旁挂文件（原生音乐 App 用不到，Flacbox 等第三方播放器可滚动）
    # 先判定再 dry-run 返回，否则 --dry-run 时永远看不到 lrc 状态
    synced = info.get("synced_lyrics") or ""
    if synced:
        row["lrc"] = "有"

    if dry_run:
        return row

    dst = out_root / rel.with_suffix(EXT_FOR[fmt])
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)

    if fmt == "mp3":
        tag_mp3(dst, lyrics, cover, meta)
    elif fmt == "mp4":
        tag_mp4(dst, lyrics, cover, meta)
    elif fmt == "flac":
        tag_flac(dst, lyrics, cover, meta)
    else:
        tag_wav(dst, lyrics, cover, meta)

    if synced:
        header = (f"[ti:{meta['title']}]\n[ar:{meta['artist']}]\n"
                  f"[al:{meta['album']}]\n[by:LRCLIB]\n")
        dst.with_suffix(".lrc").write_text(header + synced.strip() + "\n", encoding="utf-8")

    if not lyrics and not cover:
        row["status"] = "bare"
    return row


def collect(target: Path, recursive=True):
    if target.is_file():
        return [(target, Path(target.name))]
    items = []
    it = target.rglob("*") if recursive else target.glob("*")
    for p in sorted(it):
        if p.is_file() and not p.name.startswith(".") and "_tagged" not in p.parts:
            items.append((p, p.relative_to(target)))
    return items


def main():
    ap = argparse.ArgumentParser(
        description="批量给音频写入歌词+封面，供 iPhone「音乐」显示",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="例：python3 music_tagger.py ~/Music/playlist --dry-run --limit 3")
    ap.add_argument("target", help="音乐文件夹或单个音频文件")
    ap.add_argument("--out", default=None, help="输出目录，默认 <目标>/_tagged")
    ap.add_argument("--cache", default=str(Path.home() / ".cache" / "music-tagger"))
    ap.add_argument("--jobs", type=int, default=1, help="并发歌词请求数（封面始终串行以避开限流）")
    ap.add_argument("--limit", type=int, default=0, help="只处理前 N 个文件，用于试跑")
    ap.add_argument("--dry-run", action="store_true", help="只匹配不写文件")
    ap.add_argument("--no-lyrics", action="store_true")
    ap.add_argument("--no-cover", action="store_true")
    ap.add_argument("--no-recursive", action="store_true")
    g = ap.add_argument_group("手动素材（联网查不到时用，指定后不再联网）")
    g.add_argument("--cover-file", help="本地封面图片，jpg/png")
    g.add_argument("--lyrics-file", help="本地纯文本歌词")
    g.add_argument("--lrc-file", help="本地带时间轴的 .lrc（会自动剥出一份纯文本歌词）")
    g.add_argument("--title")
    g.add_argument("--artist")
    g.add_argument("--album")
    g.add_argument("--year")
    g.add_argument("--genre")
    args = ap.parse_args()

    # 手动素材注入全局 OVERRIDE
    if args.cover_file:
        p = Path(args.cover_file).expanduser()
        if not p.exists():
            sys.exit(f"找不到封面文件：{p}")
        OVERRIDE["cover_bytes"] = p.read_bytes()
    if args.lyrics_file:
        p = Path(args.lyrics_file).expanduser()
        if not p.exists():
            sys.exit(f"找不到歌词文件：{p}")
        OVERRIDE["plain_lyrics"] = p.read_text(encoding="utf-8").strip()
    if args.lrc_file:
        p = Path(args.lrc_file).expanduser()
        if not p.exists():
            sys.exit(f"找不到 LRC 文件：{p}")
        OVERRIDE["synced_lyrics"] = p.read_text(encoding="utf-8").strip()
        if OVERRIDE["plain_lyrics"] is None:
            # 只给了 lrc 时，剥掉时间戳反推一份纯文本歌词给原生音乐 App 用
            plain = "\n".join(re.sub(r"^(\[[^\]]*\]\s*)+", "", ln).strip()
                              for ln in OVERRIDE["synced_lyrics"].splitlines())
            OVERRIDE["plain_lyrics"] = plain.strip()
    for k in ("title", "artist", "album", "year", "genre"):
        v = getattr(args, k)
        if v:
            OVERRIDE[k] = v

    target = Path(args.target).expanduser().resolve()
    if not target.exists():
        sys.exit(f"路径不存在：{target}")

    out_root = Path(args.out).expanduser() if args.out else (
        target if target.is_file() else target / "_tagged")
    cache = Cache(Path(args.cache).expanduser())

    items = collect(target, not args.no_recursive and target.is_dir())
    if args.limit:
        items = items[:args.limit]
    if not items:
        sys.exit("没有找到音频文件")

    log(f"共 {len(items)} 个文件，输出到：{out_root}")
    log("=" * 68)

    rows, t0 = [], time.time()

    # 阶段一：歌词并发拉取（封面不参与，避免打爆 iTunes 限流）
    infos = {}
    jobs = max(1, args.jobs)
    if jobs > 1 and not args.no_lyrics:
        with ThreadPoolExecutor(max_workers=jobs) as ex:
            futs = {rel: ex.submit(gather_info, src, *parse_filename(src.stem),
                                   cache, True)
                    for src, rel in items}
            for src, rel in items:
                try:
                    infos[rel] = futs[rel].result()
                except Exception:
                    infos[rel] = ({}, False)
    else:
        for src, rel in items:
            try:
                infos[rel] = gather_info(src, *parse_filename(src.stem),
                                         cache, not args.no_lyrics)
            except Exception:
                infos[rel] = ({}, False)

    # 阶段二：串行补封面并写标签
    for i, (src, rel) in enumerate(items, 1):
        log(f"[{i}/{len(items)}] {rel}")
        info, was_cached = infos.get(rel, ({}, False))
        row = finish_file(src, rel, info, was_cached, out_root, cache,
                          do_cover=not args.no_cover, dry_run=args.dry_run)
        log(f"        歌词 {row['lyrics']}({row['lyrics_chars']}字) 滚动LRC {row['lrc']}"
            f" 封面 {row['cover']} | {row['title']} - {row['artist']} [{row['status']}]"
            + (f" {row['note']}" if row["note"] else ""))
        rows.append(row)

    if not args.dry_run:
        report = out_root / "report.csv"
        with open(report, "w", newline="", encoding="utf-8-sig") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        log(f"\n报告：{report}")

    ok = sum(1 for r in rows if r["status"] == "ok")
    low = sum(1 for r in rows if r["status"] == "low")
    bare = sum(1 for r in rows if r["status"] == "bare")
    skip = sum(1 for r in rows if r["status"] == "skip")
    log("=" * 68)
    log(f"完成：正常 {ok} / 低置信 {low} / 无素材 {bare} / 跳过 {skip}"
        f" | 耗时 {time.time() - t0:.0f}s")
    if low:
        log("低置信条目请查看 report.csv 的 status=low 行，必要时手工修正。")


if __name__ == "__main__":
    main()
