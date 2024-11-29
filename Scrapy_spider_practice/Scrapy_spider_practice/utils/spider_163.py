# -*- coding: utf-8 -*-

import json
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
    
    # QQ音乐
    # url = 'https://ws6.stream.qqmusic.qq.com/C400002AhhRq1B6sR3.m4a?guid=1586826375&vkey=29EE638B2C41D490E60057C0775DDA216618E355F07C3FAEC0417D1B7A15C7A70F268B5AB1379A015DF4B2B1D3C85DDF7F109D0555A6B179&uin=1152921505264228331&fromtag=120032&src=C400000JNijK0FW2sT.m4a'#C400002AhhRq1B6sR3.m4a
    # filename = 'Sesta-flofilz.mp3'
    # url = 'https://ws6.stream.qqmusic.qq.com/RS02060Afqdh3G6e8R.m4a?guid=8750392535&vkey=C2109BA962B8C1A034A87761F838CC8FBF7BE70C13E81C20ACB5CED2E8B29E0F18C2BAECCD4A92D6EAB9C00FCC86801C616DFAFB26E2B206&uin=1152921505264228331&fromtag=120032'
    # filename = 'Fantasy-vip.mp3'
    # url = 'https://ws6.stream.qqmusic.qq.com/RS0206224SUq4c4kJu.mp3?guid=8605391836&vkey=DCDA62587C50C42502CC2A438E07700F2BE0317F1D5234D4143222664760CEE17109DA7DE4FA07712459F3CB9C8EEF53BEA8556A3E69942C&uin=1152921505264228331&fromtag=120052'
    # url = 'https://ws6.stream.qqmusic.qq.com/C4000046u4mc4DcPSK.m4a?guid=7045259520&vkey=620E34962DB74E15E4E0BC81CDA4C1BBC79A58C30BE92033AAC03380E37D66DEEA81FB6C13F00A41C583E56AE1C344D55AD65BF2D13B8223&uin=1152921505264228331&fromtag=120032'
    # filename = '一路向北.mp3'
    url = 'https://m804.music.126.net/20241129174149/45376fd8f991a90431ffedf0ed125e4e/jdyyaac/obj/w5rDlsOJwrLDjj7CmsOj/44631684291/b6f6/10ec/ab6b/5607b14f444cd3d65ec9627725eb1f90.m4a?authSecret=0000019377356b2c06760a3084c01c10'
    filename = '交城山-阎维文.mp3'
    download_file(url, filename)
    print('download successfully')
    '''
    {"code":0,"ts":1719991802324,"start_ts":1719991802206,"traceid":"55b3c3f924be74e6","req_1":{"code":0,"data":{"songID":5002695,"songName":"","songType":0,"singerName":"","qrc":0,"crypt":0,"lyric":"W3RpOuWFs+W/huWMl10KW2FyOuWui+WGrOmHjl0KW2FsOuWuieWSjOahpeWMl10KW2J5Ol0KW29mZnNldDowXQpbMDA6MDAuMDBd5YWz5b+G5YyXIC0g5a6L5Yas6YeOIChEb255ZS5TKQpbMDA6MDAuNTJd6K+N77ya5a6L5Yas6YeOClswMDowMS4wNF3mm7LvvJrlrovlhqzph44KWzAwOjAxLjU2XeW9k+S9oOWGjeasoeWSjOaIkeivtOi1twpbMDA6MDUuMTJd6Z2S5pil5pe255qE5pWF5LqLClswMDowOC44Ml3miJHmraPlnKjkuIvnnYDpm6jnmoTml6DplKEKWzAwOjEyLjA2XeS5nuiuqOedgOeUn+a0u+eahOadg+WIqQpbMDA6MTguMTNdClswMDoxOC43NV3liY3kuIDlpKnml6nmmajmiJHnnYHlvIDnnLzlt7LmmK/msZ/ljZcKWzAwOjI2LjAwXeS7luS7rOivtOaflOi9r+eahOWcsOaWuQpbMDA6MzAuNTBd5oC75Lya5Y+R55Sf5p+U6L2v55qE5LqLClswMDozNS4wMF0KWzAwOjM2LjE5XemCo+W5tOeahOiInuWPsOS4igpbMDA6MzkuMDBd6K+06LCO55qE5Lq65LiA55u05q2M5ZSxClswMDo0NC4xOV0KWzAwOjQ0Ljg3XeWkp+S4jeWIl+mioOeahOW5v+WcuuS4igpbMDA6NDcuNjld5pyJ5rKh5pyJ6bi95a2Q6aOe57+UClswMDo1Mi42M10KWzAwOjUzLjUwXemdkuaYpeWSjOeejuWtkOS4gOi1t+WPmOaIkOS6huWTkeW3tApbMDE6MDEuNTBd5LuK5aSp5omv5bmz5LqG5oiR5Lus55qE5b2T5bm0ClswMTowNi4wMF3liIbpo5/kuobnkIbmg7MKWzAxOjA5LjUwXQpbMDE6MTIuNzVd5L2g5Y+v55+l6YGT5L2g55qE5ZCN5a2XClswMToxNi40M13op6Pph4rkuobmiJHnmoTkuIDnlJ8KWzAxOjIxLjI2XeeijuS6hua7oeWkqeeahOW+gOS6i+WmgueDn+S4juS4luaXoOS6iQpbMDE6MzAuMDZd5b2T5L2g6KOF5ruh6KGM5p2O5Zue5Yiw5pWF5LmhClswMTozNy41Ml3miJHnmoTkvZnnlJ8g5Y205YaN5Lmf5rKh5pyJ5YyX5pa5ClswMTo0Ny4xMl3lk4gKWzAxOjUxLjE5XeWTiApbMDI6MDQuMzhd5ZOIClswMjowOC4xOF3ljJfmlrkKWzAyOjEzLjA0XeWTiApbMDI6MjEuODNd5ZOIClswMjozMC41OV3lk4gKWzAyOjM5LjMyXeWTiApbMDI6NDMuMDhd5YyX5pa5ClswMjo0OC4wMl3lk4gKWzAzOjAxLjU4XeacieS4gOWkqeaIkeWPiOaipuingQpbMDM6MDQuODdd6YKj5Liq6KOF5ruh5LmQ5Zmo55qE5pWZ5a6kClswMzowOS4yN13kvaDov5jnq5nlnKjpl6jlj6MKWzAzOjEzLjU0XeS4gOiEuOe+nua2qeeahOihqOaDhQpbMDM6MTguMDZd5L2g6K+06L+Z5LmI5aSa5bm05L2g6L+Y5rKh5om+5YiwClswMzoyMi4yN13orqnkvaDlv4PliqjnmoTnlLfkuroKWzAzOjI2LjY4XeaIkeivtOWOuyoqKueIseaDhQpbMDM6MzAuOTld6YO95piv6L+H55y85LqR54Of55qE5Lic6KW/ClswMzozOC42OF3kvaDlj6/nn6XpgZPkvaDnmoTlkI3lrZcKWzAzOjQyLjUyXeino+mHiuS6huaIkeeahOS4gOeUnwpbMDM6NDcuMzld56KO5LqG5ruh5aSp55qE5b6A5LqL5aaC54OfIOS4juS4luaXoOS6iQpbMDM6NTYuMTJd5b2T5L2g6KOF5ruh6KGM5p2OIOWbnuWIsOaVheS5oQpbMDQ6MDMuODFd5oiR55qE5L2Z55SfIOWNtOWGjeS5n+ayoeacieWMl+aWuQpbMDQ6MTUuMDdd5L2g55+l6YGT5L2g55qE5ZCN5a2XClswNDoxOS4wNl3op6Pph4rkuobmiJHnmoTkuIDnlJ8KWzA0OjIzLjgxXeeijuS6hua7oeWkqeeahOW+gOS6i+S4juS4luaXoOS6iQpbMDQ6MzIuNDhd5b2T5L2g6KOF5ruh6KGM5p2O5Zue5Yiw5pWF5LmhClswNDo0MC4xN13miJHnmoTkvZnnlJ/lho3kuZ/msqHmnInljJfmlrk=","trans":"","roma":"","lrc_t":1583931935,"qrc_t":0,"trans_t":0,"roma_t":0,"lyric_style":0,"classical":0,"introduceTitle":"","introduceText":[{"title":"566A5LuL","content":""},{"title":"6IOM5pmv","content":""}],"vecSongID":null,"track":{"id":0,"type":0,"mid":"","name":"","title":"","subtitle":"","singer":null,"album":{"id":0,"mid":"","name":"","title":"","subtitle":"","time_public":"","pmid":""},"mv":{"id":0,"vid":"","name":"","title":"","vt":0},"interval":0,"isonly":0,"language":0,"genre":0,"index_cd":0,"index_album":0,"time_public":"","status":0,"fnote":0,"file":{"media_mid":"","size_24aac":0,"size_48aac":0,"size_96aac":0,"size_192ogg":0,"size_192aac":0,"size_128mp3":0,"size_320mp3":0,"size_ape":0,"size_flac":0,"size_dts":0,"size_try":0,"try_begin":0,"try_end":0,"url":"","size_hires":0,"hires_sample":0,"hires_bitdepth":0,"b_30s":0,"e_30s":0,"size_96ogg":0,"size_360ra":null,"size_dolby":0,"size_new":null},"pay":{"pay_month":0,"price_track":0,"price_album":0,"pay_play":0,"pay_down":0,"pay_status":0,"time_free":0},"action":{"switch":0,"msgid":0,"alert":0,"icons":0,"msgshare":0,"msgfav":0,"msgdown":0,"msgpay":0,"switch2":0,"icon2":0},"ksong":{"id":0,"mid":""},"volume":{"gain":0,"peak":0,"lra":0},"label":"","url":"","bpm":0,"version":0,"trace":"","data_type":0,"modify_stamp":0,"pingpong":"","aid":0,"ppurl":"","tid":0,"ov":0,"sa":0,"es":"","vs":null,"vi":null,"ktag":"","vf":null},"startTs":1564,"transSource":0}},"req_2":{"code":0,"data":{ "response_list": [ { "biz_id": "5002695", "biz_sub_type": 0, "biz_type": 1, "count": 8383 } ] }},"req_3":{"code":0,"data":{"basicInfo":{"albumMid":"002VeS6r4L5fLZ","albumName":"安和桥北","tranName":"","publishDate":"2013-08-26","desc":"2013宋冬野首张个人专辑《安和桥北》\n\n一个城市漫游者的安和桥北\n\n他\n在蓉城的祠堂敲打耳钟的空灵，\n在太湖樵头尝过醉人的雨。\n在筑城折下腊梅看尽风尘把酒，\n在金陵的阅江楼巅览望江淮。\n在西湖岸边撑起一把纸伞，\n在凤凰城中贺兰山下轻嗅刺玫。\n在商都品笑白居不易，\n在浏阳河映出的星光里记起奶奶的微笑。\n在金城的河床里荡起黄河谣\n也在这里点燃一只兰州。\n有一天，他还是回到了安河桥，也许就忘掉了混凝土的过错，在桥下寻觅着那些安澜平和。\n第一张专辑定名为《安和桥北》，也献给已经和安和桥一起去了天上的，深爱的奶奶。并将未来所有可能得到的成就，归功于她的冥冥之中的庇佑。\n\n一个胖子的城市生活总结\n\n今天的“安河桥”原为“安和桥”，取“安澜、平和”之意，原本一个看到名字就想生活一辈子的世外桃源活生生的改成了一架没灵魂的钢筋水泥桥。宋冬野在安和桥下学会弹吉他，在安和桥下走过肆无忌惮的童年和乱七八糟的青春，在安和桥下遇见刻骨铭心的爱情，在安和桥下吃奶奶做的饭，也在安和桥下历经成长。环境变迁使他将所有美好的记忆深藏心底，流于指间，弹于心弦。那些过往的人、事、物转化成了更真实深刻的情感，也成就了宋冬野的音乐理念。然而宋冬野从不把自己的音乐归于哪一类，只知道他的歌词里有他的全部情感与灵魂。\n倾听之余，让我们在面对现在这个无可奈何的居住着的愈发冷漠的城市中，也更深刻的体会着宋冬野的歌曲中带来的简单，真诚，随意流淌着的超越平实的诗意表达，也很容易随之陷入一种情绪里。\n\n六扇门里太龌龊，不如六根弦上取磊落\n\n所有有价值的梦想一开始都会被认为是不切实际的、叛逆的，但最终总会被认可。实现的过程总是饱富激情，新鲜和挑战的。\n这张专辑从去年年底就已经开始筹备制作，宋冬野一直全身心的投入每一个音符不断的修改编排里，每天坚定着音乐梦想，每天为之克服所有艰难，每天也更享受着音乐带来的一切美好。历时一年，这张由旅行团乐队韦伟精心操刀制作，孔阳担任平面设计，宋冬野及尧十三，李琪弦乐团等众多良师益友联合倾力打造的专辑，共收录了12首歌曲。马头琴，手鼓，弦乐等配器的尝试赋予了这些歌曲崭新的灵魂，还原了它们本就与生俱来相貌，使它们和心灵更加接近！","genre":"","language":"国语","albumType":"录音室专辑","genreURL":"","lanURL":"http://y.qq.com/m/client/categoryzone/detail.html?categoryId=1\u0026showType=2\u0026isParent=1\u0026_hidehd=1\u0026groupId=6","albumTag3":0,"recordNum":"","albumID":436025,"pmid":"002VeS6r4L5fLZ_1","type":10002,"modifyTime":1688971759,"color":10485760,"fpaymid":"","topListContent":"","topListSchema":"","adStatus":0,"encourageVideoStatus":0,"wikiurl":"","awards":[{"id":113,"name":"第3届阿比鹿音乐奖","url":"","icon":"https://y.gtimg.cn/music/photo_new/T035M000002rtWJN34Ychv.jpg","detailAward":"年度民谣唱片/年度民谣单曲","sessionID":716}],"LanRenBookUrl":"","adJson":"{\"bu_data_str1\":\"\",\"bu_data_str2\":\"\"}","vid":"","operateStatus":0,"genres":[{"name":"","url":"qqmusic://qq.com/ui/similarSongs?p=%7B%22songid%22%3A%220%22%2C%22tagid%22%3A%220%22%2C%22tagName%22%3A%22%22%7D"}],"album_right":2097152,"adTag":0,"headVideoVid":"","headVideoFrame":"","headMediaList":null,"brand":{"id":0,"name":"","url":""}},"company":{"ID":53,"name":"摩登天空","headPic":"http://y.gtimg.cn/music/common/upload/t_company_picture/37384.jpg","isShow":1,"brief":""},"singer":{"singerList":[{"mid":"004KKLWZ4320g1","name":"宋冬野","transName":"Donye.S","role":"singer","instrument":"无乐器","singerID":61620,"type":1,"singerType":0,"pmid":"004KKLWZ4320g1_2","indentity":0}]}}},"req_4":{"code":0,"data":{"uin":"","retcode":0,"verify_type":0,"login_key":"","msg":"223.104.40.254","sip":["http://ws.stream.qqmusic.qq.com/","http://isure.stream.qqmusic.qq.com/"],"thirdip":["",""],"testfile2g":"C400003mAan70zUy5O.m4a?guid=7045259520\u0026vkey=3C5634C503373DA158E66F5A743D431E644FC1AFDC1D63B47F70A585628F07C609D1723428DA9AD2A560454DF33399CA64127C447C140093\u0026uin=\u0026fromtag=3","testfilewifi":"C400003mAan70zUy5O.m4a?guid=7045259520\u0026vkey=3C5634C503373DA158E66F5A743D431E644FC1AFDC1D63B47F70A585628F07C609D1723428DA9AD2A560454DF33399CA64127C447C140093\u0026uin=\u0026fromtag=3","midurlinfo":[{"songmid":"001wpSDz2m33r4","filename":"C4000046u4mc4DcPSK.m4a","purl":"C4000046u4mc4DcPSK.m4a?guid=7045259520\u0026vkey=620E34962DB74E15E4E0BC81CDA4C1BBC79A58C30BE92033AAC03380E37D66DEEA81FB6C13F00A41C583E56AE1C344D55AD65BF2D13B8223\u0026uin=1152921505264228331\u0026fromtag=120032","errtype":"","p2pfromtag":0,"qmdlfromtag":0,"common_downfromtag":0,"vip_downfromtag":0,"pdl":0,"premain":0,"hisdown":0,"hisbuy":0,"uiAlert":0,"isbuy":0,"pneedbuy":0,"pneed":0,"isonly":0,"onecan":0,"result":0,"tips":"","opi48kurl":"","opi96kurl":"","opi192kurl":"","opiflackurl":"","opi128kurl":"","opi192koggurl":"","wififromtag":"","flowfromtag":"","wifiurl":"","flowurl":"","vkey":"620E34962DB74E15E4E0BC81CDA4C1BBC79A58C30BE92033AAC03380E37D66DEEA81FB6C13F00A41C583E56AE1C344D55AD65BF2D13B8223","opi30surl":"","ekey":"","auth_switch":16824067,"subcode":0,"opi96koggurl":"","auth_switch2":917504}],"servercheck":"1d3e9649bf5af47abffbae6ae6315976","expiration":80400}}}
    https://stat6.y.qq.com/sdk/fcgi-bin/sdk.fcg
    
    '''
    # url = 'https://stat6.y.qq.com/sdk/fcgi-bin/sdk.fcg'
    # data = {"common":{"_appid":"qqmusic","_uid":"1152921505264228331","_platform":24,"_account_source":"2","_os_version":"","_app_version":"123.0.0.0","_channelid":"","_os":"mac","_app":"chrome","_opertime":"1719993463","_network_type":"unknown","adtag":"","fqm_id":"7642c64d-5680-42a8-b8be-b2a114021486"},"items":[{"_key":"webcs","id":"1649-12-9","url":"/n/ryqq/player","rate":1,"webview":0,"fcp":786,"fmp":786,"tti":1606},{"_key":"web_time","id":"1649-12-9","point":"1649-12-9-21","rate":1,"time":786},{"_key":"web_time","id":"1649-12-9","point":"1649-12-9-22","rate":1,"time":786},{"_key":"web_time","id":"1649-12-9","point":"1649-12-9-23","rate":1,"time":1606}]}
    # headers=get_headers()
    # headers['Referer']='https://y.qq.com/'
    # res = requests.post(url = url, data=data, headers=headers)
    # print(json.loads(res.content) )