# IvyDad Mac 本地媒体工具

包含两个独立脚本：

- `ivydad_batch_download.py`：读取已保存的课程视频接口 JSON/JSONL 响应，整理元数据并下载响应中明确给出的 MP4 与 SRT，生成 `课程清单.csv`。默认所有媒体平铺到同一个文件夹。
- `mp4_batch_to_audio.py`：使用 FFmpeg 批量提取视频音轨，默认输出 M4A/AAC（源音轨是 AAC 时无损直拷），也可切 MP3；顺带把同名 SRT 转成 LRC 歌词。
- `series.json`：系列命名表，按视频 id 指定文件名与所属集，见第 3 节。

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

## 3. 整理并批量下载

### 改下载位置（改脚本文件）

打开 `ivydad_batch_download.py`，文件顶部这两行就是要改的地方：

```python
DEFAULT_OUTPUT_DIR = 'IvyDad_Downloads'
DEFAULT_LAYOUT = 'single'
```

把第一行换成目标目录，写绝对路径最稳妥：

```python
DEFAULT_OUTPUT_DIR = '/Users/adam/Movies/IvyDad'
```

命令行 `-o` 优先级更高，临时换位置不用改文件。改完先预览，确认路径再真下：

```bash
python3 ivydad_batch_download.py -i ./api_json --dry-run
```

`--dry-run` 不联网、不建目录、不写文件，只打印每个文件会落到哪里。

单个 JSON：

```bash
python3 ivydad_batch_download.py -i ./api_json/one_video.json -o ./IvyDad_Downloads
```

批量目录：

```bash
python3 ivydad_batch_download.py -i ./api_json -o ./IvyDad_Downloads --workers 3
```

默认布局 `single`：所有 MP4 与 SRT 直接平铺在输出目录下，视频和字幕共享同一个文件名主体，IINA / VLC 等播放器会自动挂载字幕。标题重名时自动追加 `[id]` 后缀，避免互相覆盖。想恢复「每个视频一个子文件夹」，加 `--layout per-video`。输出目录根部生成 `课程清单.csv`，记录 ID、标题、时长、来源 URL、本地路径和下载状态。脚本支持中断后重跑：已存在且非空的文件会跳过；下载中的 `.part` 文件可续传（服务器支持 Range 时）。

如果服务器返回 401/403，说明该地址当前不允许直接访问或需要官方授权会话；脚本不会尝试模拟登录或绕过访问控制。请使用 IvyDad 官方下载/离线功能或服务方允许的导出方式。

### SSL: CERTIFICATE_VERIFY_FAILED（self-signed certificate in certificate chain）

机器上开着 Proxyman / Charles 时，系统代理会用自签 CA 重签 `*.ivydad.com` 的证书。curl 和浏览器读 macOS 钥匙串，校验能过；Python 用 OpenSSL 的证书文件（`/private/etc/ssl/cert.pem`），不认那张新装的根证书，于是三个下载任务全挂在 TLS 握手阶段。

脚本默认直连 CDN、不走代理，同时保留完整的 TLS 校验，直接重跑即可：

```bash
python3 ivydad_batch_download.py -i ./api_json
```

如果网络必须走代理，两个办法：

```bash
# 1) 导出抓包根证书，追加到 Python 的信任链（推荐）
security find-certificate -a -c "Proxyman CA" -p > /tmp/proxyman-ca.pem
python3 ivydad_batch_download.py -i ./api_json --use-proxy --ca-bundle /tmp/proxyman-ca.pem

# 2) 兜底：跳过校验，仅在确认代理是自己开的时用
python3 ivydad_batch_download.py -i ./api_json --use-proxy --insecure
```

`--insecure` 会关掉证书校验，别在陌生网络里用。也可改脚本顶部的 `DEFAULT_USE_PROXY` 改变默认行为。

### 按系列命名与分集

API 返回的 `title` 不带「第N集 / 精讲」这类系列信息，`1. Spring Festival 春节` 也没法靠正则推出「精讲」，所以命名规则放在脚本同目录的 `series.json`，按视频 id 映射：

```json
{
  "83860": {"stem": "第1集-春节-动画", "episode": "第1集-春节"},
  "83792": {"stem": "第1集-春节-精讲-Spring Festival 春节", "episode": "第1集-春节"}
}
```

`stem` 是文件名（不含扩展名），字幕自动跟视频同名同目录；`episode` 用于按集分文件夹。以 `_` 开头的键是注释，会被忽略。未列出的 id 回退到原来的 `title`，行为不变。

不想维护单独的表，也可以把这两个字段并进响应 JSON 的对应对象里（其余字段原样保留），优先级高于 `series.json`：

```json
{
  "local_stem": "第1集-春节-动画",
  "episode": "第1集-春节"
}
```

```bash
# 预览新命名，不联网、不改文件
python3 ivydad_batch_download.py -i ./api_json --dry-run

# 把已经下好的旧命名文件改名复用，跳过重复下载
python3 ivydad_batch_download.py -i ./api_json --adopt

# 按集分文件夹
python3 ivydad_batch_download.py -i ./api_json --layout by-episode
```

`--adopt` 只改名，不删文件；配合 `--dry-run` 可以先看清单。运行日志和 `课程清单.csv` 都改用 `stem` 显示，清单新增 `stem`、`episode` 两列。

## 4. MP4 批量转音频 + 歌词

脚本本来就递归批量转，20 个 mp4 一次跑完。默认输出 M4A/AAC：

```bash
python3 mp4_batch_to_audio.py \
  -i "/Users/adam/Downloads/常青藤爸爸/传统节日与节气" \
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
  -i "/Users/adam/Downloads/常青藤爸爸/传统节日与节气" \
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
  -i "/Users/adam/Downloads/常青藤爸爸/传统节日与节气" \
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
