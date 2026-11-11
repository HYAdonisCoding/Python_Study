# IvyDad Mac 本地媒体工具

包含两个独立脚本：

- `ivydad_batch_download.py`：读取已保存的课程视频接口 JSON/JSONL 响应，整理元数据并下载响应中明确给出的 MP4 与 SRT，生成 `课程清单.csv`。默认按每个 JSON 文件名在根目录下单独建文件夹。
- `mp4_batch_to_audio.py`：使用 FFmpeg 批量提取视频音轨，默认输出 M4A/AAC（源音轨是 AAC 时无损直拷），也可切 MP3；顺带把同名 SRT 转成 LRC 歌词。
- `series.json`：可选的命名覆盖表，按视频 id 手工指定文件名与所属集；按集分组的 JSON 不需要它，见第 2、3 节。

## 1. 环境准备

建议 macOS 使用 Homebrew 安装 FFmpeg：

```bash
brew install ffmpeg
ffmpeg -version
```

两个脚本均只使用 Python 标准库，不需要 `pip install`。

## 2. 准备课程 JSON

在 Proxyman 中找到 `GET /api/m-course/course/video`，复制/导出**响应正文 JSON**，保存为 `.json` 文件。可把多个 JSON 放在同一个目录，也支持 `.jsonl`（每行一个 JSON 对象）。示例见 `examples/video_api_response.example.json`。

请勿把含有 `token`、Cookie、Authorization、`member_uuid` 或 `device_id` 的完整请求 URL/请求头放进共享文件；本工具只需要响应 JSON 中的媒体 URL、标题、ID 等字段。

### 推荐格式：按集分组（不用维护 `series.json`）

把同一集的动画和精讲放在同一个 key 下，key 就是集名：

```json
{
  "第1集-十二生肖": [
    {"id": 85703, "title": "三、日常生活-第1集-十二生肖-动画",
     "url": "https://.../a.mp4", "subtitle": "https://.../a.srt", "duration": "124.14"},
    {"id": 85695, "title": "22.The Chinese Zodiac 十二生肖",
     "url": "https://.../b.mp4", "subtitle": "", "duration": "1247.89"}
  ],
  "第2集-筷子": [ ... ]
}
```

脚本据此自动生成文件名：

| 分组键 | 原 title | 生成文件名 |
|---|---|---|
| 第1集-十二生肖 | 三、日常生活-第1集-十二生肖-动画 | `第1集-十二生肖-动画.mp4` + `.srt` |
| 第1集-十二生肖 | 22.The Chinese Zodiac 十二生肖 | `第1集-十二生肖-精讲-The Chinese Zodiac 十二生肖.mp4` |
| 第2集-筷子 | 三、日常生活-第2集-筷子-动画 | `第2集-筷子-动画.mp4` + `.srt` |
| 第2集-筷子 | 23.Chopsticks and Table Manners 筷子与餐桌礼仪 | `第2集-筷子-精讲-Chopsticks and Table Manners 筷子与餐桌礼仪.mp4` |

规则：

- 顶层 key 匹配 `第N集` 就是集名，同时也是 `--layout by-episode` 的文件夹名。
- `title` 含「动画」→ `{集名}-动画`；其余一律按精讲处理 → `{集名}-精讲-{标题}`，标题开头的 `22.` / `23.` 这类序号自动去掉。
- 元素顺序不限，按内容判断角色；字幕与视频同名同目录。加新集只要加一个 key，不用改脚本。
- 单对象、顶层数组、嵌套 `{"data": {"list": [...]}}`、`.jsonl` 仍兼容；只是没有分组键时会回退到 `title` 命名。多行 JSONL 误存成 `.json` 后缀也能识别，坏文件只报错不中断其它文件。

## 3. 整理并批量下载

### 输出目录规则（按 JSON 文件名自动分目录）

`ivydad_batch_download.py` 顶部这两行控制落盘位置：

```python
DEFAULT_OUTPUT_DIR = '/Users/adam/Downloads/常青藤爸爸/'   # 只写根目录
PER_FILE_SUBDIR = True                                    # 按 JSON 文件名建子目录
```

`DEFAULT_OUTPUT_DIR` 是**根目录**，脚本拿 `./api_json/` 下每个 JSON 的**文件名（去扩展名）**当子目录名：

```text
api_json/三、日常生活.json
  → /Users/adam/Downloads/常青藤爸爸/三、日常生活/
       ├── 第1集-十二生肖-动画.mp4 / .srt
       ├── 第1集-十二生肖-精讲-The Chinese Zodiac 十二生肖.mp4
       ├── 第2集-筷子-动画.mp4 / .srt
       ├── 第2集-筷子-精讲-Chopsticks and Table Manners 筷子与餐桌礼仪.mp4
       └── 课程清单.csv
```

多个 JSON 各自一个文件夹、各自一份 `课程清单.csv`，互不干扰。先预览再下，输出会按目录分组打印：

```bash
python3 ivydad_batch_download.py -i ./api_json --dry-run
```

`-o` 换的是**根目录**，仍按文件名分组；`--no-per-file-dir` 回到旧行为（全部平铺到根目录、只出一份总清单）：

```bash
python3 ivydad_batch_download.py -i ./api_json -o /Users/adam/Movies/IvyDad
python3 ivydad_batch_download.py -i ./api_json --no-per-file-dir
```

规则补充：

- 同名 stem 的多个文件（如 `.json` 与 `.jsonl`）合并进同一个文件夹和同一份清单。
- 同一视频出现在多个 JSON 里时按 `(id, url)` 全局去重，只归第一个文件夹，日志打印 `[去重]`。
- 文件名撞名判断按文件夹独立计算，不同文件夹里同名互不干扰。
- `--layout by-episode` / `per-video` 是在各自文件夹**内部**再分层。
- `--dry-run` 不联网、不建目录、不写文件。

默认布局 `single`：每个文件夹内的 MP4 与 SRT 平铺在一起，视频和字幕共享同一个文件名主体，IINA / VLC 等播放器会自动挂载字幕。同一文件夹内标题重名时自动追加 `[id]` 后缀；想「每个视频一个子文件夹」加 `--layout per-video`。每个文件夹各生成一份 `课程清单.csv`，记录 ID、stem、集名、时长、来源 URL、本地路径和下载状态。脚本支持中断后重跑：已存在且非空的文件会跳过；下载中的 `.part` 文件可续传（服务器支持 Range 时）。

如果服务器返回 401/403，说明该地址当前不允许直接访问或需要官方授权会话；脚本不会尝试模拟登录或绕过访问控制。请使用 IvyDad 官方下载/离线功能或服务方允许的导出方式。

### SSL: CERTIFICATE_VERIFY_FAILED（self-signed certificate in certificate chain）

这个报错有两个独立来源，脚本现在都自动兜住，**直接重跑即可**：

1. **换了 Python 解释器**：`/usr/local/bin/python3`（python.org 官方包 3.13.9）的 `ssl.get_default_verify_paths().cafile` 是 `None`，没配内置根证书，直连真证书也验不过。脚本检测到后自动补 `/private/etc/ssl/cert.pem`（或 Homebrew 的 `openssl@3/cert.pem`）。
2. **抓包代理重签证书**：Proxyman / Charles 用自签 CA 重签 `*.ivydad.com`，Python 不读 macOS 钥匙串，不认这张 CA。脚本自动导出钥匙串里**已信任**的 Proxyman / Charles 根证书并追加到信任链，全程不关闭 TLS 校验。

每次运行会打印一行诊断，能看出用的是哪个 Python、有没有补 CA：

```text
[网络] Python 3.13.9 | 代理: 直连 | 根证书: 内置缺失→自动补 /private/etc/ssl/cert.pem | 抓包 CA: Proxyman CA, Charles Proxy CA
```

脚本默认直连 CDN、不走代理，同时保留完整的 TLS 校验：

```bash
python3 ivydad_batch_download.py -i ./api_json
```

如果网络必须走代理：

```bash
# 1) 走代理，自动信任本机抓包 CA（推荐）
python3 ivydad_batch_download.py -i ./api_json --use-proxy

# 2) 手动指定 CA
security find-certificate -a -c "Proxyman CA" -p > /tmp/proxyman-ca.pem
python3 ivydad_batch_download.py -i ./api_json --use-proxy --ca-bundle /tmp/proxyman-ca.pem

# 3) 兜底：跳过校验，仅在确认代理是自己开的时用
python3 ivydad_batch_download.py -i ./api_json --use-proxy --insecure
```

`--no-auto-proxy-ca` 可关掉自动追加抓包 CA；`--insecure` 会关掉证书校验，别在陌生网络里用。也可改脚本顶部的 `DEFAULT_USE_PROXY` 改变默认行为。

### 命名优先级

按集分组的 JSON 会自动命名，不用再往表里加条目。完整优先级：

1. 视频对象里的 `local_stem` / `episode` 字段
2. `series.json` 中按 id 的映射（可选，用来手工覆盖自动推导）
3. 分组键自动推导（第 2 节的推荐格式）
4. API 原 `title`

`series.json` 保留给旧批次或想改名的个别视频，以 `_` 开头的键是注释，会被忽略：

```json
{
  "85695": {"stem": "第1集-十二生肖-精讲-生肖故事", "episode": "第1集-十二生肖"}
}
```

`stem` 是文件名（不含扩展名），字幕自动同名同目录；`episode` 用于按集分文件夹。也可以把这两个字段直接并进响应 JSON 的对象里（其余字段原样保留）：

```json
{"local_stem": "第1集-十二生肖-动画", "episode": "第1集-十二生肖"}
```

想彻底回到旧行为（只用表 / title）加 `--no-auto-naming`。

```bash
# 预览命名，不联网、不改文件
python3 ivydad_batch_download.py -i ./api_json --dry-run

# 按集分文件夹
python3 ivydad_batch_download.py -i ./api_json --layout by-episode --dry-run

# 把已经下好的旧命名文件改名复用，跳过重复下载
python3 ivydad_batch_download.py -i ./api_json --adopt
```

`--adopt` 只改名，不删文件；配合 `--dry-run` 可以先看清单。运行日志和 `课程清单.csv` 都改用 `stem` 显示，清单含 `stem`、`episode` 两列。

## 4. MP4 批量转音频 + 歌词

脚本本来就递归批量转，20 个 mp4 一次跑完。默认输出 M4A/AAC：

```bash
python3 mp4_batch_to_audio.py \
  -i "/Users/adam/Downloads/常青藤爸爸/三、日常生活" \
  -o "/Users/adam/Downloads/常青藤爸爸/Audio"
```

不写 `-o` 时输出到输入目录**父目录**下的 `Audio/`，容易放偏，建议写全路径。

### 为什么默认 M4A 而不是 MP3

这批 MP4 的音轨本来就是 **AAC 128k**（ffprobe 实测）。输出 M4A 时脚本直接把这条 AAC 流换个容器复制出来，不解码再编码，音质零损失；输出 MP3 必须重新编码，是有损转有损。加上 macOS / iPhone / Apple 音乐 / AirPods 原生吃 AAC，元数据、封面、章节支持也更完整，所以默认选 M4A。

同一集动画（111.3 秒）实测：

| 做法 | 体积 | 耗时 | 说明 |
|---|---|---|---|
| M4A 无损复制（现在默认） | 1.72 MB | 0.19 s | 原样保留 AAC 128k |
| M4A 重编码 192k | 2.60 MB | 1.57 s | 码率虚高，音质不升反有二次损失 |
| MP3 192k | 2.55 MB | 1.56 s | 多一次有损，体积还更大 |
| MP3 128k | 1.70 MB | 1.33 s | 体积相当，仍有一次有损 |

**该用 MP3 的场景**：点读笔、早教机、老车载、只认 `.mp3` 的播放器或老人机——这些设备不认 M4A。

改默认只改 `mp4_batch_to_audio.py` 顶部一行：

```python
DEFAULT_FORMAT = 'mp3'
```

临时切格式用命令行，优先级更高：

```bash
python3 mp4_batch_to_audio.py \
  -i "/Users/adam/Downloads/常青藤爸爸/三、日常生活" \
  -o "/Users/adam/Downloads/常青藤爸爸/Audio" -f mp3 --bitrate 128k
```

源音轨是 128k，MP3 写 192k 只是把文件撑大，不会变好听，建议对齐到 128k。`--reencode` 可强制 M4A 重编码（例如要统一码率）；源音轨不是 AAC（mkv/opus 等）时会自动重编码，不会硬拷出错。已经生成过的重编码 M4A 不会被自动替换，想换成无损版加 `--overwrite`。

转音频时会顺带处理同名 `.srt`：

- 生成同名 `.lrc`，每条字幕按起始时间打 `[mm:ss.xx]` 时间戳，双语默认合并成一行（`The Spring Festival / 春节`）。
- 复制一份同名 `.srt` 到音频旁，供 VLC / IINA / mpv 加载外挂字幕。
- 只留一种语言：`--lyrics-lang zh` 或 `--lyrics-lang en`。
- 不要歌词：`--no-lyrics`。
- 音频已转过、只想补歌词：`--lyrics-only`，不重新编码。

```bash
# 只补歌词，跳过转码
python3 mp4_batch_to_audio.py \
  -i "/Users/adam/Downloads/常青藤爸爸/三、日常生活" \
  -o "/Users/adam/Downloads/常青藤爸爸/Audio" --lyrics-only
```

即使目标音频已存在被跳过，歌词文件仍会重新生成，不用加 `--overwrite` 重编码。精讲视频没有配套 `.srt`，会记「无字幕」跳过。

### 播放时能不能同步显示

| 方式 | 效果 |
|---|---|
| 音频 + 同名 `.srt`，VLC / IINA / mpv 加载字幕 | **逐行同步，最可靠** |
| 同名 `.lrc`，支持 LRC 的音乐播放器 | 逐行滚动；Apple 音乐 / QuickTime 不支持 |
| 内嵌歌词元数据 | Apple 音乐 / iOS 音乐能看到文字，不保证滚动 |

VLC 官方字幕格式列表里没有 LRC，所以脚本默认同时留一份 `.srt`，别只生成 `.lrc`。本脚本不做元数据内嵌。默认跳过已存在的目标音频；`--overwrite` 重新编码。原视频不会删除，输出保留输入目录结构和文件名。

## 5. 注意

- 仅处理你有权访问并获准下载/转换的课程媒体；不要用于绕过 DRM、付费墙或其他访问控制。
- 视频 URL 可能失效或受服务器策略限制。下载失败时先用浏览器验证该 URL 当前是否仍可访问。
- 音频格式按播放端选：Apple 设备用 M4A（默认，源 AAC 可无损直拷）；只认 MP3 的老设备用 `-f mp3 --bitrate 128k`。音频提取不包含画面；歌词以同名 `.lrc` / `.srt` 外挂文件提供，不内嵌进音频。
