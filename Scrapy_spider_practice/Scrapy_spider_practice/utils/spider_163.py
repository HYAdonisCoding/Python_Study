
import random
from fake_useragent import UserAgent
import requests

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
        'User-Agent': ua if ua else getUA()
    }
    return headers
def download_mp3():
    url = 'https://m10.music.126.net/20240703095220/81526e2dbb55fce1c6447c62ee099fcf/yyaac/obj/wonDkMOGw6XDiTHCmMOi/3945547514/6c7d/4fb4/2def/e560cfe0e71e462bec4ef8efcdfadb5c.m4a'
    url = 'https://m704.music.126.net/20240703113450/2934cb24662cf52001f84e93f61cee1a/jdyyaac/obj/w5rDlsOJwrLDjj7CmsOj/17266711921/1541/393f/f4ff/86d26c68acbc6e8c02892334ce8b2274.m4a?authSecret=000001907691e07002170a3b1db51782'
    res = requests.get(url, headers=get_headers())
    with open('诛仙我回来-任贤齐.mp3', 'wb') as f:
        f.write(res.content)
def download_file(url, filename):
    res = requests.get(url, headers=get_headers())
    with open(filename, 'wb') as f:
        f.write(res.content)
def download_mp4():
    url = 'https://vodkgeyttp8.vod.126.net/cloudmusic/NTA5MTI0OTQ=/a7a08ad10ff1fb471e1deaf0c39d1c6f/a687d1e8d5b8666442e3a838aae044a8.mp4?wsSecret=07339ea812d0917da488ee99f8c8f854&wsTime=1719971177'
    res = requests.get(url, headers=get_headers())
    with open('诛仙我回来-任贤齐.mp4', 'wb') as f:
        f.write(res.content)
if __name__ == '__main__':
    # download_mp3()
    # headers = get_headers()
    # download_mp4()
    # url = 'https://m804.music.126.net/20240703113706/367059ade90c59363d993c850c07a4db/jdyyaac/obj/w5rDlsOJwrLDjj7CmsOj/12360274338/3350/04dc/06d2/43db43480ec8778ccf618f492a0cf856.m4a?authSecret=000001907693f45807130a3b192fbfde'
    # filename =  '北京雨燕.mp3'
    url = 'https://m704.music.126.net/20240703143642/22333b46d8828b725e0af59dc156e99f/jdyyaac/obj/w5rDlsOJwrLDjj7CmsOj/29313221871/2a79/69e6/ba3b/62b896c54fe7a7111d69654d8ef08b85.m4a?authSecret=00000190773864d906cf0a3b1883140f'
    filename =  '孤勇者-陈奕迅.mp3'
    download_file(url, filename)
    print('download successfully')