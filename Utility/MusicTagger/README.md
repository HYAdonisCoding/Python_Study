# MusicTagger

批量给本地音频文件写入**歌词**和**专辑封面**，让手机播放器打开就有图、有词。

只依赖 Python 3.9+ 和 `mutagen`。歌词与封面**全部联网自动抓**，换电脑不用带任何素材文件。

---

## 一、先看能力边界（重要，别踩坑）

| 场景 | 效果 |
|---|---|
| 在 **iOS 原生「音乐」App** 看封面 | ✅ 正常显示 |
| 在 **iOS 原生「音乐」App** 看歌词 | ⚠️ 能看到整段文字，但**不会滚动** |
| 在 **第三方播放器**（One Player / Flacbox / Vinyls 等） | ✅ 封面 + **逐行滚动歌词** |
| 在 macOS「音乐」App | ✅ 封面 + 歌词（不滚动） |

**为什么原生 App 不滚动**：Apple 官方支持文档写明，本地导入的音频文件「歌词」按钮是灰的，同步滚动歌词只对 Apple Music 曲库曲目开放。这是产品设计限制，**不是你文件的标签写错了**。

要滚动歌词，必须用支持 LRC 的第三方播放器。脚本会为每首歌额外生成同名 `.lrc` 旁挂文件，正是给这类播放器用的。

---

## 二、安装

```bash
python3 -m pip install mutagen
```

就这一个依赖。脚本用 Python 标准库发 HTTP 请求，不需要 `requests`。

---

## 三、快速开始

```bash
# 1. 先试跑 5 首，只看匹配结果，不写任何文件
python3 music_tagger.py "/你的/音乐文件夹" --dry-run --limit 5

# 2. 确认匹配没问题后正式跑
python3 music_tagger.py "/你的/音乐文件夹"

# 3. 结果在 <音乐文件夹>/_tagged/，原文件不会被改动
```

单文件也可以：

```bash
python3 music_tagger.py "/你的/音乐/某首歌.mp3"
```

指定输出目录、开并发：

```bash
python3 music_tagger.py "/你的/音乐文件夹" --out ~/Desktop/out --jobs 4
```

---

## 四、参数

| 参数 | 说明 |
|---|---|
| `target` | 音乐文件夹或单个音频文件（必填） |
| `--out PATH` | 输出目录，默认 `<目标>/_tagged` |
| `--dry-run` | 只匹配、不写文件，用来先看结果对不对 |
| `--limit N` | 只处理前 N 个文件，试跑用 |
| `--jobs N` | 并发歌词请求数，默认 1。封面始终串行以避开 iTunes 限流 |
| `--no-lyrics` | 跳过歌词，只补封面 |
| `--no-cover` | 跳过封面，只补歌词 |
| `--no-recursive` | 不递归子目录 |
| `--cache PATH` | 缓存目录，默认 `~/.cache/music-tagger` |

**手动素材**（联网查不到时用，一旦指定就完全不联网）：

| 参数 | 说明 |
|---|---|
| `--cover-file PATH` | 本地封面图片（jpg / png） |
| `--lyrics-file PATH` | 本地纯文本歌词 |
| `--lrc-file PATH` | 本地带时间轴的 `.lrc`，会自动剥出一份纯文本歌词 |
| `--title` `--artist` `--album` `--year` `--genre` | 手动指定元数据，覆盖自动匹配结果 |

环境变量：

| 变量 | 默认 | 说明 |
|---|---|---|
| `MUSIC_TAGGER_COVER_PX` | `600x600` | 嵌入封面尺寸。**不建议改大**，见「常见问题 4」 |

---

## 五、文件名规则（决定匹配准确率）

脚本从文件名里猜歌名和歌手，规则是：

1. 先剥掉开头的序号：`01.` `01-` `01、` `01_` `01)` 都支持
2. 再按 `-` `–` `—` `_` **从右往左**切开，左边是歌名、右边是歌手

能正确识别的例子：

```
美人鱼-林俊杰.mp3                    → 美人鱼 / 林俊杰
01. 修炼爱情 - 林俊杰.mp3            → 修炼爱情 / 林俊杰
04. 丑八怪-薛之谦.flac               → 丑八怪 / 薛之谦
```

识别不了的情况：文件名里没有歌手、或者歌手名里本身带 `-`。这些会退回成「整个文件名当歌名、歌手留空」，匹配分不够就标 `low`（低置信）让你人工看。

**改文件名比改脚本划算。** 统一成 `歌名-歌手.ext` 是投产比最高的一步。

---

## 六、输出结构

```
你的音乐文件夹/
└── _tagged/                     ← 输出，结构镜像源目录
    ├── 01. 华语/
    │   ├── 美人鱼-林俊杰.m4a     ← 已写入封面 + 歌词
    │   └── 美人鱼-林俊杰.lrc     ← 逐行时间轴歌词（第三方播放器用）
    ├── report.csv               ← 逐文件处理报告
    └── ...
```

**原文件永不修改**，一律复制到 `_tagged/` 再打标签。

**扩展名会被纠正**：脚本读文件头（magic bytes）判断真实格式，不看后缀。所以一个名叫 `.mp3` 但实际是 AAC/MP4 容器的文件，输出会是 `.m4a`。这不是 bug，是修正——iOS 和后缀写错的文件容易出各种怪问题。

支持的输入格式：`mp3` / `m4a`(mp4) / `flac` / `wav`。

---

## 七、怎么看 report.csv

`status` 列是重点：

| status | 含义 | 要不要处理 |
|---|---|---|
| `ok` | 歌词和封面都匹配到了，置信度够 | 不用 |
| `low` | 匹配到了但**置信度低**，可能配错歌 | **要人工看** |
| `bare` | 歌词和封面都没拿到 | 要人工看 |
| `skip` | 格式不支持 | 忽略 |

`low` 是最需要警惕的。典型症状：歌词长度异常（比如 4000+ 字，明显是串到别的歌了）、或者歌名歌手对不上。打开 `report.csv` 按 `status` 排序，逐个核对就行。

---

## 八、三种歌词落地方式

脚本一次输出两种：

| 位置 | 内容 | 给谁用 |
|---|---|---|
| 文件内 `©lyr` / `USLT` / `LYRICS` 字段 | 纯文本歌词（无时间戳） | iOS 原生音乐 App、macOS 音乐 App |
| 同名 `.lrc` 旁挂文件 | 带 `[mm:ss.xx]` 时间轴 | One Player、Flacbox、Vinyls 等第三方播放器 |

如果你只想用第三方播放器、嫌 `.lrc` 文件碍事，可以把它内嵌进音频（这样单文件自包含，换设备也不会丢）：

```python
from mutagen.mp4 import MP4
import re, pathlib

audio = pathlib.Path("某首歌.m4a")
lrc = audio.with_suffix(".lrc").read_text(encoding="utf-8")
# 只保留时间轴行，丢掉 [ti:] [ar:] 这类描述标签
lines = [l.strip() for l in lrc.splitlines()
         if l.strip() and re.match(r"^\[\d{2}:\d{2}\.\d{2,3}\]", l.strip())]
a = MP4(str(audio))
a["©lyr"] = "\n".join(lines)
a.save()
```

注意：内嵌时间轴歌词后，iOS 原生音乐 App 会把时间戳原样显示出来（一排 `[00:12.34]`），很难看。所以**只在你确定用第三方播放器时才这么做**。

---

## 九、手动指定素材（联网查不到时）

有些歌 LRCLIB 和 iTunes 都没有：独立音乐、翻唱、live、自录、小众语种。这时走手动模式，把素材喂给它：

```bash
python3 music_tagger.py "/音乐/某首冷门歌.mp3" \
  --cover-file 封面.jpg \
  --lrc-file 歌词.lrc \
  --title "歌名" --artist "歌手" --album "专辑" --year 2024
```

要点：

- 一旦给了 `--cover-file` / `--lyrics-file` / `--lrc-file` 中**任意一个**，就完全不联网，也不写缓存
- `--lrc-file` 会自动剥掉 `[00:12.34]` 时间戳，生成一份纯文本歌词写进 `©lyr`（给原生 App）；同时把原始 `.lrc` 旁挂输出（给第三方播放器）。一份输入，两种落地
- `--title` `--artist` `--album` `--year` `--genre` 会覆盖自动匹配结果
- 报告里会标 `手动素材`，一眼能认出来

实测输出：

```
[1/1] Because of You-Kelly Clarkson.mp3
        歌词 有(1635字) 滚动LRC 有 封面 有 | Because of You - Kelly Clarkson [ok] 手动素材
完成：正常 1 / 低置信 0 / 无素材 0 / 跳过 0 | 耗时 0s
```

注意 `耗时 0s`——手动模式不发任何网络请求。

> **关于旧的 `embed_music_tags.py`**：它已被本脚本取代，功能已全部合并进来（手动指定素材、wav 支持）。旧版有个危险行为：**直接改写源文件**而不是复制副本，且把同一份歌词套到文件夹里所有文件。这两点都没有保留。如果你还有旧脚本，可以删了。

## 十、常见问题

### 1. 报错 `can't sync to MPEG frame` 或 `moov atom not found`

文件后缀和真实格式不一致。脚本内部已按文件头判断格式，正常不会触发。如果你手动用别的工具改过标签，用 `ffprobe 文件名` 确认真实容器：

```bash
ffprobe -v error -show_entries format=format_name -of default=noprint_wrappers=1 "你的文件.mp3"
```

### 2. 中文歌匹配不到

iTunes Search API 在**中国区（CN）搜不到大部分中文歌**。脚本已默认按 `TW → HK → US` 三个商店兜底，能匹配到繁体（「鄧紫棋」↔「邓紫棋」也是靠这个）。

如果还是搜不到，通常是：
- 文件名里歌手写的是简称（`JJ` 而不是 `林俊杰`）
- 这首歌不在 iTunes 曲库里（独立音乐、翻唱、live）

### 3. 跑得慢

正常。iTunes Search API 限制约 **20 次/分钟**，脚本做了全局串行 + 1.2 秒间隔。100 首歌大约 15–25 分钟。

`--jobs` 只影响歌词请求（LRCLIB 没这么严的限流），封面永远是串行的。

### 4. 封面在 iPhone 上不显示

按可能性排序：

1. **iPhone 资料库里有两条同名曲目**，你播的是旧的没打标签那份。iOS 对同曲目分开存，长按 → 显示简介 → 看文件大小能区分。
2. **封面缓存没刷新**。iOS 音乐按「艺人+专辑」缓存封面，之前进过没图的版本就会一直吐空图。删歌 → 强杀音乐 App → 重启手机 → 重新同步。
3. **嵌入封面太大**。所以脚本默认 600×600 / 约 35 KB。1400×1400 / 460 KB 这种在 Finder 同步时有被跳过的报告。真要高清图，用 `MUSIC_TAGGER_COVER_PX=1400x1400` 覆盖，但先确认小的能显示。

确认文件本身没问题：

```bash
ffprobe -v error -show_streams -of json "你的文件.m4a" | grep -c attached_pic   # 输出 1 就是对
```

### 5. 缓存导致改了文件名也不刷新

```bash
rm -rf ~/.cache/music-tagger
```

缓存按「歌名+歌手」存，改了文件名但没清缓存会命中旧结果。

---

## 十一、技术细节

| 项 | 说明 |
|---|---|
| 歌词数据源 | [LRCLIB](https://lrclib.net) 开放接口，同时取 `plainLyrics` 和 `syncedLyrics` |
| 封面数据源 | iTunes Search API，`artworkUrl100` 替换尺寸后缀取大图 |
| 匹配算法 | 歌名/歌手归一化相似度打分 + 时长比对（±5 秒内加分）+ 负关键词扣分（live/remix/instrumental/演唱会等） |
| 缓存 | `~/.cache/music-tagger/`，按「歌名+歌手」哈希，含封面二进制 |
| 限流 | iTunes 全局串行 + 1.2 秒间隔；LRCLIB 失败重试 4 次，指数退避 |
| 标签写入 | mp3 → ID3v2 (`USLT` + `APIC`)；m4a → `©lyr` + `covr`；flac → Vorbis `LYRICS` + `Picture`；wav → ID3 chunk (`USLT` + `APIC`) |
| 音频流 | 不重新编码，只改容器元数据，音质零损失 |

---

## 十二、English Quick Start

```bash
# Install
python3 -m pip install mutagen

# Dry run on 5 files (no writes)
python3 music_tagger.py "/path/to/music" --dry-run --limit 5

# Process everything
python3 music_tagger.py "/path/to/music"
# Output: /path/to/music/_tagged/  (originals untouched)

# Manual mode — when the track isn't in any online database
python3 music_tagger.py "rare-track.mp3" \
  --cover-file cover.jpg --lrc-file lyrics.lrc \
  --title "Title" --artist "Artist"
```

Fetches lyrics from LRCLIB and artwork from the iTunes Search API, then embeds both into each audio file (mp3 / m4a / flac / wav). Also writes a sidecar `.lrc` with line-synced lyrics for third-party players. Scored matching with duration verification and negative-keyword filtering; low-confidence matches are flagged in `report.csv`. Manual mode (`--cover-file` / `--lyrics-file` / `--lrc-file`) bypasses the network entirely.

Note: iOS's built-in Music app **does not support scrolling lyrics for local files** (Apple limitation). Use One Player, Flacbox, or Vinyls for synced LRC playback.
