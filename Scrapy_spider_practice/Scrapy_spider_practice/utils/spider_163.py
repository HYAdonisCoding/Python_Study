# -*- coding: utf-8 -*-

import json
import os
import random
import re
from fake_useragent import UserAgent
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def getUA():
    uaList = [
        'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15',
        'Mozilla/5.0 (Linux; Android) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.109 Safari/537.36 CrKey/1.54.248666',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    ]
    User_Agent = random.choice(uaList)
    return User_Agent
    
def get_headers():
    ua = UserAgent().random
    headers = {
        'User-Agent': ua if ua else getUA(),
        "Referer": "https://www.listennotes.com/",
    }
    return headers
def download_mp3():
    url = 'https://m10.music.126.net/20240703095220/81526e2dbb55fce1c6447c62ee099fcf/yyaac/obj/wonDkMOGw6XDiTHCmMOi/3945547514/6c7d/4fb4/2def/e560cfe0e71e462bec4ef8efcdfadb5c.m4a'
    url = 'https://m704.music.126.net/20240703113450/2934cb24662cf52001f84e93f61cee1a/jdyyaac/obj/w5rDlsOJwrLDjj7CmsOj/17266711921/1541/393f/f4ff/86d26c68acbc6e8c02892334ce8b2274.m4a?authSecret=000001907691e07002170a3b1db51782'
    res = requests.get(url, headers=get_headers(), verify=False, timeout=15)
    with open('诛仙我回来-任贤齐.mp3', 'wb') as f:
        f.write(res.content)
# 函数：下载文件
import os
import re
import requests
from enum import Enum

# 定义支持的文件扩展名
class FileExtension(Enum):
    MP3 = '.mp3'
    MP4 = '.mp4'
    M4A = '.m4a'

# 定义下载函数
def download_file(url, filename, default_extension=FileExtension.MP3):
    try:

        # 1. 首先去除系统非法字符
        sanitized_filename = re.sub(r'[\\/*?:"<>|]', '', filename)

        # 2. 判断是否包含中文字符
        # 如果包含中文，则执行去除空格的操作
        if re.search(r'[\u4e00-\u9fa5]', sanitized_filename):
            sanitized_filename = sanitized_filename.replace(' ', '')
        
        # 检查并自动添加扩展名
        ext = os.path.splitext(sanitized_filename)[1].lower()  # 提取扩展名
        if ext not in [e.value for e in FileExtension]:
            # 如果没有有效扩展名，添加默认扩展名
            sanitized_filename += default_extension.value
        
        # 下载文件
        response = requests.get(
            url,
            stream=True,
            timeout=15,
            headers=get_headers(),
            verify=False
        )
        response.raise_for_status()  # 如果状态码不是 2xx，抛出异常
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0

        with open(sanitized_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)

        # 校验文件完整性
        if total_size != 0 and downloaded != total_size:
            print(f"❌ 文件下载不完整: {sanitized_filename}")
            print(f"期望: {total_size} 字节, 实际: {downloaded} 字节")
        else:
            print(f"✅ 下载完成: {sanitized_filename} ({downloaded/1024/1024:.2f} MB)")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {filename}: {e}")
    except Exception as e:
        print(f"Unknown error occurred for {filename}: {e}")
def download_mp4():
    url = 'https://vodkgeyttp8.vod.126.net/cloudmusic/NTA5MTI0OTQ=/a7a08ad10ff1fb471e1deaf0c39d1c6f/a687d1e8d5b8666442e3a838aae044a8.mp4?wsSecret=07339ea812d0917da488ee99f8c8f854&wsTime=1719971177'
    res = requests.get(url, headers=get_headers(), verify=False, timeout=15)
    with open('诛仙我回来-任贤齐.mp4', 'wb') as f:
        f.write(res.content)

text = '''
0:00:00  -- 第01回除异己定乾坤 隋王代周终称帝

0:19:09  -- 第02回 征突厥灭陈国 杨坚父子统九州

0:39:10  -- 第03回 移都城凿运河 新帝杨广施韬略

1:01:29  -- 第04回 征民夫召五军屡败屡战高句丽

1:21:41  -- 第05次回频征战群众瓦岗起义天下震动

1:41:17  -- 第06回 翟诛让弑炀帝 乱世豪杰常悲叹

1:57:57  -- 第07回 谋举兵立傀儡 李渊受禅唐开国

2:16:42  -- 第08回 定西北平中原 群雄逐鹿归一统

2:35:47  -- 第09回 争皇位祸阋墙兄弟相残武门

2:53:11  -- 第10回 集良策推改革 君臣共创贞观治

3:10:43  -- 第11回 灭突厥亲吐西北边患终平定

3:33:33  -- 第十二回统西域征辽东 太宗身死志未偿

3:55:17  -- 第13回 废太子立储君 李治逆袭登大位

4:12:56  -- 第14回 剪羽翼破突厥 中亚各部皆归降

4:31:08  -- 第15回 助新罗灭百济 仁贵终降高句丽

4:54:58  -- 第16回封昭仪肃劲敌二圣临朝坟墓

5:13:54  -- 第17回 袭西域伐番茄 唐番茄和亲方止战

5:32:39  -- 第18回 翻手立覆手废武后谋权逆乾坤

5:52:57  -- 第19回 屠宗室亡武周 是非成败转头空

6:13:13  -- 第20回 亲贤臣显荣光 开元盛世时不常

6:33:57  -- 第21回 宠贵妃登宰辅 两征南诏皆败北

6:53:30  -- 第22回 阿巴斯高仙芝 唐军铩羽怛罗斯

7:14:28  -- 第23回设藩镇坟墓起兵反唐安禄山

7:36:47  -- 第24回 卷陷洛阳 玄宗降旨斩河北忠良

7:55:23  -- 第25回 战败叛军 祭侄子后河北世传

8:17:40  -- 第26回 弃长安兵哗变 宛转蛾眉马前死

8:38:29  -- 第27回 敌内乱谋反攻 肃宗徐图复两京

8:59:32  -- 第28回 复两京迎玄宗 能伸能屈史思明

9:18:09  -- 第29回 招兵士秣战马二度叛唐战河阳

9:37:35  -- 第30回 陷怀州子弑父 后宦干政立新君

9:57:11  -- 第31回 诛辅国倚权宦 大败伪燕掠河南

10:17:06  -- 第32回 史逆亡天下殇 藩镇覆大唐

10:39:59  -- 第33回 长安陷仆固反力挽狂澜郭子仪

11:01:21  -- 第34回 继位谋中兴 德宗改革引兵变

11:22:05  -- 第35回 唐蕃战平凉案 永贞革新亦枉然

11:42:03  -- 第36回 藩镇袭蔡州 平藩大业多患

12:03:15  -- 第37回 穆宗昏敬宗庸 密诛宦官终失算

12:24:35  -- 第38回 宦官足以甘露变牛李党争两败残

12:43:00  -- 第39回 武宗继君臣和回鹘抗唐反被亡

13:00:17  -- 第40回 藩镇患武宗断 平定泽潞终除患

13:19:30  -- 第41回灭佛教唐中兴归义军功张议潮

13:43:26  -- 第42回 施苛政引民变黄巢北伐破潼关

14:03:01  -- 第43回 潼关陷僖宗逃 锦绣长安监狱火烧

14:22:05  -- 第44回 沙陀兵勤王军 黄巢兵败长安焚

14:40:54  -- 第45回 小混混投黄巢 叛齐降唐朱全忠

14:59:17  -- 第46回 围蔡州舂人肉 朱李讨逆黄巢亡

15:21:09  -- 第47回 伐晋王除复恭空有大志唐昭宗

15:40:12  -- 第48回 伐岐王谋政变昭宗夫妇砧板肉

16:01:39  -- 第49回 昭宗死唐覆亡 五代十国终登场

16:22:59  -- 第50回 晋军强梁军防 朱李相争誓称皇

16:45:11  -- 第51回 子弑父弟杀兄 内迷宫唐灭梁

17:05:46  -- 第52回 乱世相皆称王后唐兴兵天下平

17:26:36  -- 第53回 宠宦官喜优伶 邺都兵变攻洛阳

17:47:26  -- 第54回 存勖亡嗣源皇励精图治中兴唐

18:09:45  -- 第55回 愿割地称儿皇 被逼造反石敬瑭

18:30:40  -- 第56回 助刘汉惨遭猜忌起兵反汉郭文仲

18:50:08  -- 第57回 伐北汉征南唐 后周江山归赵宋

19:09:22  -- 第58回 后蜀荆南降 西南一角适时凉

19:30:36  -- 第59回 唐灭楚吴越王不起刀兵为典范

19:53:02  -- 第60回 杨吴灭立南唐 攻闽顽抗终灭亡

20:14:52  -- 第61回 征南汉伐北汉五代十国归一统
'''
import re
import subprocess
# 切分文件
def file_slicing():
    input_file = "/Users/adam/Documents/Developer/MyGithub/Python_Study/隋唐五代.m4a"
    output_dir = os.path.join(os.path.dirname(input_file), "隋唐五代")
    os.makedirs(output_dir, exist_ok=True)
    pattern = r'(\d+:\d{2}:\d{2})\s+--\s+(.*)'

    matches = re.findall(pattern, text)

    def format_time(t):
        parts = t.split(':')
        if len(parts[0]) == 1:
            return '0' + t
        return t

    for i in range(len(matches)):
        start_time = format_time(matches[i][0])
        title = matches[i][1].strip()
        title = re.sub(r'[\\/*?:"<>|]', '', title)[:50]

        if i < len(matches) - 1:
            end_time = format_time(matches[i + 1][0])
        else:
            end_time = None

        output = os.path.join(output_dir, f"{i+1:02d}_{title}.m4a")

        if end_time:
            cmd = [
                "ffmpeg",
                "-y",
                "-ss", start_time,
                "-to", end_time,
                "-i", input_file,
                "-c", "copy",
                "-avoid_negative_ts", "1",
                output
            ]
        else:
            cmd = [
                "ffmpeg",
                "-y",
                "-ss", start_time,
                "-i", input_file,
                "-c", "copy",
                "-avoid_negative_ts", "1",
                output
            ]

        print(f"正在切割：{i+1}/{len(matches)} - {title}")
        result = subprocess.run(cmd)

        need_reencode = False

        # 1. 如果命令失败
        if result.returncode != 0:
            need_reencode = True

        # 2. 如果输出文件不存在或为0KB（你当前主要问题）
        if not os.path.exists(output) or os.path.getsize(output) == 0:
            need_reencode = True

        if need_reencode:
            print(f"⚠️ copy失败或空文件，强制重编码: {title}")

            if end_time:
                cmd_reencode = [
                    "ffmpeg",
                    "-y",
                    "-ss", start_time,
                    "-to", end_time,
                    "-i", input_file,
                    "-vn",
                    "-acodec", "aac",
                    "-b:a", "128k",
                    "-fflags", "+genpts",
                    "-err_detect", "ignore_err",
                    output
                ]
            else:
                cmd_reencode = [
                    "ffmpeg",
                    "-y",
                    "-ss", start_time,
                    "-i", input_file,
                    "-vn",
                    "-acodec", "aac",
                    "-b:a", "128k",
                    "-fflags", "+genpts",
                    "-err_detect", "ignore_err",
                    output
                ]

            subprocess.run(cmd_reencode)

            # 再次校验
            if not os.path.exists(output) or os.path.getsize(output) == 0:
                print(f"❌ 最终仍失败: {title}")
if __name__ == '__main__':
    # download_mp3()
    # headers = get_headers()
    # download_mp4()
    # url = 'https://m804.music.126.net/20240703113706/367059ade90c59363d993c850c07a4db/jdyyaac/obj/w5rDlsOJwrLDjj7CmsOj/12360274338/3350/04dc/06d2/43db43480ec8778ccf618f492a0cf856.m4a?authSecret=000001907693f45807130a3b192fbfde'
    # filename =  '北京雨燕.mp3'
    
    # QQ音乐
    # 数据数组
    data_array = [
        {
            'url': 'https://d3ctxlq1ktw2nl.cloudfront.net/production/exports/9d0fd0c8/53953853/f6822bc87e262d6583287413240aaec8.m4a',
            'filename': '隋唐五代'
        },

    ]

    # 遍历数组并下载文件
    # for item in data_array:
    #     download_file(item['url'], item['filename'], default_extension=FileExtension.M4A)
    file_slicing()
    print('All Download successfully')