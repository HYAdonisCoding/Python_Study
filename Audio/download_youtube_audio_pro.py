from __future__ import annotations

from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Iterable
from urllib.parse import parse_qs, urlparse

import yt_dlp
from yt_dlp.utils import sanitize_filename

# ============================================================
# 基础配置
# ============================================================

BASE_OUTPUT_DIR = Path.home() / "Downloads" / "youtube_audio"
BASE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 已知、确认过的播放列表或单视频 URL。
# 这些任务优先级最高，直接下载，不经过搜索猜测。
DOWNLOAD_URLS = [
    # "https://www.youtube.com/watch?v=Zutmi_PmuPA&list=PLC5JP36mbqAG_B0DgqHRwFi9Tl1OcaKI7",  # 老梁故事汇58
    # "https://www.youtube.com/watch?v=UYjJh3Mx7L0&list=PLC5JP36mbqAFFkA6KcUK_xXf3GcZRTXSP",  # 老梁故事汇 精选352
    # "https://www.youtube.com/watch?v=Z0yLnwcgpdE&list=PLC5JP36mbqAFvC_a0at8g2N1bMxNHyY-B",  # 老梁观世界143
    # "https://www.youtube.com/watch?v=hU39wfkIHRQ&list=PLlD7SeKBB31cI78XeR5k535TDjRRK-oAv",  # 王立群读史记251
    # "https://www.youtube.com/watch?v=DNThQu4x2vQ&list=PLlD7SeKBB31f8Uh7-cfgCJnhZ4hyp7z3J",  # 资治通鉴
]

# 关键词系列：
# Pro 版不会“搜到第一个就下载”，而是：
# 1. 搜索多个候选视频
# 2. 对候选做标题相似度 + 频道可信度评分
# 3. 找出最匹配的候选视频
# 4. 若候选视频自身来自播放列表，则优先下载对应播放列表
# 5. 如果拿不到可靠播放列表，则按关键词建立“搜索合集”文件夹，下载高匹配视频
SERIES_KEYWORDS = [
    # "王立群读《史记》系列",
    # "王立群读史记 秦始皇",
    "资治通鉴",
    # "女皇武则天",
    # "老梁故事汇 历史合集",
    # "老梁观世界 历史 战争",
]

# 搜索结果数量
SEARCH_CANDIDATE_COUNT = 20

# 关键词搜索时，如果最终无法识别真实 playlist，
# 最多下载多少个高匹配视频到“搜索合集”文件夹。
SEARCH_COLLECTION_MAX_ITEMS = 40

# 最低候选评分。
# 太低说明搜索结果不靠谱，直接跳过。
MIN_SEARCH_SCORE = 0.42

# 可信频道/标题加分词。
# 这里只用于排序，不代表绝对可信。
TRUSTED_HINTS = [
    "cctv",
    "央视",
    "百家讲坛",
    "china history",
    "老梁",
    "梁宏达",
    "袁腾飞",
    "王立群",
    "蒙曼",
]

# 若为会员专享 / Private / unavailable，跳过并继续。
IGNORE_UNAVAILABLE = True


# ============================================================
# 数据结构
# ============================================================


@dataclass
class SearchCandidate:
    url: str
    video_id: str
    title: str
    channel: str
    score: float


# ============================================================
# 通用工具
# ============================================================


def normalize_text(text: str) -> str:
    return (
        (text or "")
        .lower()
        .replace("《", "")
        .replace("》", "")
        .replace("·", " ")
        .replace("：", " ")
        .replace(":", " ")
        .replace("-", " ")
        .replace("_", " ")
    )


def text_similarity(a: str, b: str) -> float:
    a_norm = normalize_text(a)
    b_norm = normalize_text(b)

    if not a_norm or not b_norm:
        return 0.0

    ratio = SequenceMatcher(
        None,
        a_norm,
        b_norm,
    ).ratio()

    a_tokens = set(a_norm.split())
    b_tokens = set(b_norm.split())

    if a_tokens and b_tokens:
        overlap = len(a_tokens & b_tokens) / max(1, len(a_tokens))
    else:
        overlap = 0.0

    return ratio * 0.65 + overlap * 0.35


def sanitize_dir_name(
    name: str,
    fallback: str,
) -> str:

    safe = sanitize_filename(
        name or fallback,
        restricted=False,
    ).strip()

    return safe or fallback


def get_query_params(
    url: str,
) -> dict[str, list[str]]:

    return parse_qs(urlparse(url).query)


def get_playlist_id(
    url: str,
) -> str | None:

    values = get_query_params(url).get("list")

    return values[0] if values else None


def get_video_id(
    url: str,
) -> str | None:

    parsed = urlparse(url)

    if parsed.netloc in {
        "youtu.be",
        "www.youtu.be",
    }:
        return parsed.path.strip("/") or None

    values = get_query_params(url).get("v")

    return values[0] if values else None


def canonical_playlist_url(
    playlist_id: str,
) -> str:

    return "https://www.youtube.com/" f"playlist?list={playlist_id}"


def canonical_video_url(
    video_id: str,
) -> str:

    return "https://www.youtube.com/" f"watch?v={video_id}"


def common_metadata_options() -> dict:

    return {
        "quiet": True,
        "no_warnings": True,
        # 使用当前 Chrome 登录态
        "cookiesfrombrowser": ("chrome",),
        "skip_download": True,
        "extract_flat": False,
        "retries": 5,
        "extractor_retries": 3,
    }


# ============================================================
# playlist / video 元数据
# ============================================================


def fetch_playlist_info(
    url: str,
) -> dict | None:

    playlist_id = get_playlist_id(url)

    if not playlist_id:
        return None

    playlist_url = canonical_playlist_url(playlist_id)

    options = {
        **common_metadata_options(),
        # playlist 元数据阶段使用 flat，
        # 避免把所有视频完整解析一遍。
        "extract_flat": True,
    }

    with yt_dlp.YoutubeDL(options) as ydl:

        return ydl.extract_info(
            playlist_url,
            download=False,
        )


def fetch_video_info(
    url: str,
) -> dict | None:

    options = common_metadata_options()

    with yt_dlp.YoutubeDL(options) as ydl:

        return ydl.extract_info(
            url,
            download=False,
        )


# ============================================================
# 搜索与评分
# ============================================================


def candidate_score(
    keyword: str,
    title: str,
    channel: str,
) -> float:
    """
    对搜索候选进行更适合中文标题的评分。

    评分优先级：
    1. 标题完整包含关键词：最强信号
    2. 关键词包含标题：强信号
    3. SequenceMatcher 字符相似度
    4. 中文字符覆盖率
    5. 可信频道/人物加分
    6. 系列/全集等形态加分

    最终分数限制在 0~1。
    """

    keyword_norm = normalize_text(keyword).strip()
    title_norm = normalize_text(title).strip()
    channel_norm = normalize_text(channel).strip()

    if not keyword_norm or not title_norm:
        return 0.0

    combined = f"{title_norm} {channel_norm}"

    # 去掉空格，中文匹配更稳定。
    keyword_compact = "".join(keyword_norm.split())
    title_compact = "".join(title_norm.split())
    combined_compact = "".join(combined.split())

    # --------------------------------------------------------
    # 1. SequenceMatcher 字符相似度
    # --------------------------------------------------------

    sequence_ratio = SequenceMatcher(
        None,
        keyword_compact,
        title_compact,
    ).ratio()

    # --------------------------------------------------------
    # 2. 字符覆盖率
    #
    # 例如：
    # keyword = 资治通鉴
    # title   = 姜鹏品读资治通鉴1司马光的另类史记
    #
    # 关键词字符全部出现，coverage = 1.0
    # --------------------------------------------------------

    keyword_chars = set(keyword_compact)
    title_chars = set(title_compact)

    if keyword_chars:
        char_coverage = len(keyword_chars & title_chars) / len(keyword_chars)
    else:
        char_coverage = 0.0

    # --------------------------------------------------------
    # 3. 包含关系
    # --------------------------------------------------------

    if keyword_compact == title_compact:

        score = 0.95

    elif keyword_compact in title_compact:

        # 最典型：
        #
        # keyword:
        # 资治通鉴
        #
        # title:
        # 姜鹏品读资治通鉴 1 司马光的另类史记
        #
        # 这种应该直接判定为高度相关。
        score = 0.78

    elif title_compact in keyword_compact:

        score = 0.70

    else:

        # 模糊匹配
        score = sequence_ratio * 0.55 + char_coverage * 0.35

    # --------------------------------------------------------
    # 4. 可信来源加分
    # --------------------------------------------------------

    trusted_bonus = 0.0

    for hint in TRUSTED_HINTS:

        hint_norm = "".join(normalize_text(hint).split())

        if hint_norm and hint_norm in combined_compact:
            trusted_bonus += 0.06

    # 防止：
    # CCTV + 央视 + 百家讲坛 + 王立群……
    # 一口气把分数堆满。
    trusted_bonus = min(
        trusted_bonus,
        0.18,
    )

    score += trusted_bonus

    # --------------------------------------------------------
    # 5. 系列节目形态加分
    # --------------------------------------------------------

    series_bonus = 0.0

    for hint in (
        "完整版",
        "全集",
        "系列",
        "合集",
        "第一部",
        "第二部",
        "第三部",
        "第1集",
        "第01集",
        "playlist",
    ):

        if hint in combined:
            series_bonus += 0.025

    score += min(
        series_bonus,
        0.10,
    )

    # --------------------------------------------------------
    # 6. 集数格式加分
    #
    # 比如：
    #
    # 姜鹏品读《资治通鉴》 1 ...
    # 第01集
    # EP01
    #
    # 通常意味着它属于连续系列。
    # --------------------------------------------------------

    series_number_hints = (
        " 1 ",
        " 01 ",
        "第1",
        "第01",
        "ep1",
        "ep01",
    )

    if any(hint in f" {combined} " for hint in series_number_hints):
        score += 0.03

    # --------------------------------------------------------
    # 7. 明显不符合“完整历史系列”的结果扣分
    # --------------------------------------------------------

    penalty = 0.0

    for hint in (
        "快速了解",
        "一分钟",
        "几分钟",
        "shorts",
        "short",
        "速看",
        "快速看懂",
    ):

        if hint in combined:
            penalty += 0.05

    score -= min(
        penalty,
        0.15,
    )

    # --------------------------------------------------------
    # 8. 最终限制在 0 ~ 1
    # --------------------------------------------------------

    return max(
        0.0,
        min(score, 1.0),
    )


def search_video_candidates(
    keyword: str,
) -> list[SearchCandidate]:

    print()
    print(f"搜索系列关键词：{keyword}")

    options = {
        **common_metadata_options(),
        "extract_flat": True,
    }

    search_query = f"ytsearch" f"{SEARCH_CANDIDATE_COUNT}:" f"{keyword}"

    with yt_dlp.YoutubeDL(options) as ydl:

        result = ydl.extract_info(
            search_query,
            download=False,
        )

    entries = result.get("entries") or []

    candidates: list[SearchCandidate] = []

    for entry in entries:

        if not entry:
            continue

        video_id = entry.get("id")

        if not video_id:
            continue

        title = entry.get("title") or ""

        channel = (
            entry.get("channel")
            or entry.get("uploader")
            or entry.get("channel_id")
            or ""
        )

        score = candidate_score(
            keyword,
            title,
            channel,
        )

        candidates.append(
            SearchCandidate(
                url=canonical_video_url(video_id),
                video_id=video_id,
                title=title,
                channel=channel,
                score=score,
            )
        )

    candidates.sort(
        key=lambda x: x.score,
        reverse=True,
    )

    return candidates


def print_top_candidates(
    keyword: str,
    candidates: list[SearchCandidate],
    limit: int = 5,
) -> None:

    print()

    print(f"“{keyword}”候选 Top " f"{min(limit, len(candidates))}：")

    for index, item in enumerate(
        candidates[:limit],
        start=1,
    ):

        print(
            f"  {index}. "
            f"score={item.score:.3f} | "
            f"{item.title} | "
            f"{item.channel or '未知频道'} | "
            f"{item.video_id}"
        )


def discover_playlist_from_candidate(
    candidate: SearchCandidate,
) -> tuple[
    str | None,
    str | None,
]:
    """
    对高分候选视频做完整元数据读取。

    如果元数据里能得到 playlist_id，
    返回：

    playlist URL
    playlist title
    """

    try:

        info = fetch_video_info(candidate.url)

    except Exception as e:

        print("读取候选详情失败：" f"{candidate.video_id}")

        print(e)

        return None, None

    if not info:
        return None, None

    playlist_id = info.get("playlist_id")

    playlist_title = info.get("playlist_title")

    if playlist_id:

        return (
            canonical_playlist_url(playlist_id),
            playlist_title,
        )

    return None, None


# ============================================================
# 下载目标解析
# ============================================================


def resolve_direct_url(
    url: str,
) -> tuple[
    str,
    Path,
    bool,
]:

    playlist_id = get_playlist_id(url)

    # --------------------------------------------------------
    # playlist
    # --------------------------------------------------------

    if playlist_id:

        playlist_url = canonical_playlist_url(playlist_id)

        info = fetch_playlist_info(playlist_url) or {}

        title = info.get("title") or playlist_id

        safe_title = sanitize_dir_name(
            title,
            playlist_id,
        )

        output_dir = BASE_OUTPUT_DIR / safe_title

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        return (
            playlist_url,
            output_dir,
            True,
        )

    # --------------------------------------------------------
    # 单视频
    # --------------------------------------------------------

    video_id = get_video_id(url) or "single_video"

    try:

        info = fetch_video_info(url) or {}

        title = info.get("title") or video_id

    except Exception:

        title = video_id

    return (
        url,
        BASE_OUTPUT_DIR,
        False,
    )


def resolve_keyword_task(
    keyword: str,
) -> tuple[
    str | list[str] | None,
    Path | None,
    bool,
]:

    candidates = search_video_candidates(keyword)

    if not candidates:

        print("没有搜索到任何候选：" f"{keyword}")

        return (
            None,
            None,
            False,
        )

    print_top_candidates(
        keyword,
        candidates,
    )

    best = candidates[0]

    # --------------------------------------------------------
    # 评分过低
    # --------------------------------------------------------

    if best.score < MIN_SEARCH_SCORE:

        print()

        print(
            f"跳过关键词“{keyword}”："
            f"最高评分只有 "
            f"{best.score:.3f}，"
            f"低于阈值 "
            f"{MIN_SEARCH_SCORE:.2f}。"
        )

        return (
            None,
            None,
            False,
        )

    # --------------------------------------------------------
    # 从前 5 个高分视频尝试发现真正的 playlist
    # --------------------------------------------------------

    for candidate in candidates[:5]:

        if candidate.score < MIN_SEARCH_SCORE:
            continue

        (
            playlist_url,
            playlist_title,
        ) = discover_playlist_from_candidate(candidate)

        if playlist_url:

            playlist_id = get_playlist_id(playlist_url) or "playlist"

            safe_title = sanitize_dir_name(
                playlist_title or keyword,
                playlist_id,
            )

            output_dir = BASE_OUTPUT_DIR / safe_title

            output_dir.mkdir(
                parents=True,
                exist_ok=True,
            )

            print()

            print(f"关键词“{keyword}”" "识别到播放列表：")

            print("  " f"{playlist_title or safe_title}")

            print(f"  {playlist_url}")

            return (
                playlist_url,
                output_dir,
                True,
            )

    # --------------------------------------------------------
    # 找不到可靠 playlist
    #
    # 不乱猜。
    #
    # 将高匹配视频建立成“搜索合集”
    # --------------------------------------------------------

    selected = [
        candidate.url
        for candidate in candidates
        if (candidate.score >= MIN_SEARCH_SCORE)
    ][:SEARCH_COLLECTION_MAX_ITEMS]

    if not selected:

        return (
            None,
            None,
            False,
        )

    folder_name = sanitize_dir_name(
        f"搜索合集 - {keyword}",
        "search_collection",
    )

    output_dir = BASE_OUTPUT_DIR / folder_name

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    print()

    print("没有发现可靠的真实播放列表，" "改为建立搜索合集：")

    print(f"  {output_dir}")

    print(f"将下载 " f"{len(selected)} " "个高匹配公开视频。")

    return (
        selected,
        output_dir,
        False,
    )


# ============================================================
# yt-dlp 下载参数
# ============================================================


def build_download_options(
    output_dir: Path,
    is_playlist: bool,
    *,
    collection_mode: bool = False,
) -> dict:

    archive_file = output_dir / "downloaded.txt"

    failed_file = output_dir / "failed.txt"

    # --------------------------------------------------------
    # 输出文件名
    # --------------------------------------------------------

    if is_playlist:

        outtmpl = output_dir / (
            "%(playlist_index)03d - " "%(title)s " "[%(id)s].%(ext)s"
        )

    else:

        outtmpl = output_dir / ("%(title)s " "[%(id)s].%(ext)s")

    # --------------------------------------------------------
    # 失败记录
    # --------------------------------------------------------

    def error_hook(
        data: dict,
    ) -> None:

        if data.get("status") != "error":
            return

        info = data.get("info_dict") or {}

        video_id = info.get("id") or "unknown"

        title = info.get("title") or "unknown"

        with failed_file.open(
            "a",
            encoding="utf-8",
        ) as f:

            f.write(f"{video_id}\t" f"{title}\n")

    # --------------------------------------------------------
    # yt-dlp options
    # --------------------------------------------------------

    return {
        # 最佳音频优先
        "format": "bestaudio/best",
        # playlist 时允许展开
        "noplaylist": not is_playlist,
        "outtmpl": str(outtmpl),
        # ----------------------------------------------------
        # 转 MP3
        # ----------------------------------------------------
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        # ----------------------------------------------------
        # 下载归档
        # ----------------------------------------------------
        "download_archive": str(archive_file),
        # ----------------------------------------------------
        # 无权限视频跳过
        # ----------------------------------------------------
        "ignoreerrors": (IGNORE_UNAVAILABLE),
        # ----------------------------------------------------
        # 文件名兼容
        # ----------------------------------------------------
        "windowsfilenames": True,
        # ----------------------------------------------------
        # 日志
        # ----------------------------------------------------
        "quiet": False,
        "no_warnings": False,
        # ----------------------------------------------------
        # 网络重试
        # ----------------------------------------------------
        "retries": 10,
        "fragment_retries": 10,
        "extractor_retries": 5,
        # ----------------------------------------------------
        # 断点续传
        # ----------------------------------------------------
        "continuedl": True,
        # ----------------------------------------------------
        # Chrome Cookies
        # ----------------------------------------------------
        "cookiesfrombrowser": ("chrome",),
        # ----------------------------------------------------
        # FFmpeg
        # ----------------------------------------------------
        "postprocessor_args": {
            "ffmpeg": [
                "-hide_banner",
            ],
        },
        # ----------------------------------------------------
        # 下载 hook
        # ----------------------------------------------------
        "progress_hooks": [
            error_hook,
        ],
    }


# ============================================================
# 下载执行
# ============================================================


def run_download(
    urls: str | Iterable[str],
    output_dir: Path,
    is_playlist: bool,
    *,
    label: str,
    collection_mode: bool = False,
) -> int:

    if isinstance(
        urls,
        str,
    ):

        download_urls = [urls]

    else:

        download_urls = list(urls)

    print()
    print("=" * 78)

    print(f"任务：{label}")

    print("类型：" + ("播放列表" if is_playlist else "单视频 / 搜索合集"))

    print(f"保存目录：{output_dir}")

    print("下载记录：" f"{output_dir / 'downloaded.txt'}")

    print("失败记录：" f"{output_dir / 'failed.txt'}")

    print("会员专享 / Private / " "Video unavailable 会跳过，" "其余继续。")

    print("=" * 78)
    print()

    options = build_download_options(
        output_dir,
        is_playlist,
        collection_mode=(collection_mode),
    )

    with yt_dlp.YoutubeDL(options) as ydl:

        return ydl.download(download_urls)


def dedupe_direct_urls(
    urls: Iterable[str],
) -> list[str]:

    unique: list[str] = []
    seen: set[str] = set()

    for url in urls:

        playlist_id = get_playlist_id(url)

        if playlist_id:

            key = f"playlist:" f"{playlist_id}"

        else:

            video_id = get_video_id(url)

            key = f"video:{video_id}" if video_id else url

        if key in seen:

            print(f"跳过重复任务：{url}")

            continue

        seen.add(key)

        unique.append(url)

    return unique


# ============================================================
# 主程序
# ============================================================


def main() -> None:

    print()
    print("=" * 78)

    print("YouTube 音频下载器 Pro")

    print("格式：MP3 192kbps")

    print("Chrome Cookies：开启")

    print("断点续传：开启")

    print("下载归档：开启")

    print(f"手工 URL：" f"{len(DOWNLOAD_URLS)} 个")

    print(f"系列关键词：" f"{len(SERIES_KEYWORDS)} 个")

    print(f"总目录：" f"{BASE_OUTPUT_DIR}")

    print("=" * 78)

    try:

        # ====================================================
        # 1. 已确认 URL
        # ====================================================

        for url in dedupe_direct_urls(DOWNLOAD_URLS):

            try:

                (
                    download_url,
                    output_dir,
                    is_playlist,
                ) = resolve_direct_url(url)

                run_download(
                    download_url,
                    output_dir,
                    is_playlist,
                    label=url,
                )

            except Exception as e:

                print()

                print("[手工 URL 任务失败] " f"{url}")

                print(e)

        # ====================================================
        # 2. 关键词系列
        # ====================================================

        for keyword in SERIES_KEYWORDS:

            try:

                (
                    resolved,
                    output_dir,
                    is_playlist,
                ) = resolve_keyword_task(keyword)

                if not resolved or output_dir is None:
                    continue

                collection_mode = isinstance(
                    resolved,
                    list,
                )

                run_download(
                    resolved,
                    output_dir,
                    is_playlist,
                    label=keyword,
                    collection_mode=(collection_mode),
                )

            except Exception as e:

                print()

                print("[关键词任务失败] " f"{keyword}")

                print(e)

        print()
        print("=" * 78)

        print("全部任务处理结束。")

        print(f"总目录：" f"{BASE_OUTPUT_DIR}")

        print("=" * 78)

    except KeyboardInterrupt:

        print()

        print("下载已停止。")

        print("下次运行会根据 " "downloaded.txt " "继续跳过已完成条目。")


if __name__ == "__main__":
    main()
