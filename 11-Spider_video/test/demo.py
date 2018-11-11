import requests
import urllib.request

proxy_host = 'proxy.abuyun.com'
proxy_port = '9020'

# 代理隧道验证信息
proxy_user = '****************'
proxy_pass = '****************'

proxy_meta = 'http://%(user)s:%(pass)s@%(host)s:%(port)s' % {
    'host': proxy_host,
    'port': proxy_port,
    'user': proxy_user,
    'pass': proxy_pass,
}

proxies = {
    'http': proxy_meta,
    'https': proxy_meta,
}

url = 'https://acs.youku.com/h5/mtop.youku.play.ups.appinfo.get/1.1/?jsv=2.4.16&appKey=24679788&t=1541864356733&sign=49a6a18c01ab030e8fc40fac9f79693e&api=mtop.youku.play.ups.appinfo.get&v=1.1&timeout=20000&YKPid=20160317PLF000211&YKLoginRequest=true&AntiFlood=true&AntiCreep=true&type=jsonp&dataType=jsonp&callback=mtopjsonp1&data=%7B%22steal_params%22%3A%22%7B%5C%22ccode%5C%22%3A%5C%220502%5C%22%2C%5C%22client_ip%5C%22%3A%5C%22192.168.1.1%5C%22%2C%5C%22utid%5C%22%3A%5C%22HehtFLGYuHUCAXWEwwmLxoR3%5C%22%2C%5C%22client_ts%5C%22%3A1541864356%2C%5C%22version%5C%22%3A%5C%220.5.87%5C%22%2C%5C%22ckey%5C%22%3A%5C%22DIl58SLFxFNndSV1GFNnMQVYkx1PP5tKe1siZu%2F86PR1u%2FWh1Ptd%2BWOZsHHWxysSfAOhNJpdVWsdVJNsfJ8Sxd8WKVvNfAS8aS8fAOzYARzPyPc3JvtnPHjTdKfESTdnuTW6ZPvk2pNDh4uFzotgdMEFkzQ5wZVXl2Pf1%2FY6hLK0OnCNxBj3%2Bnb0v72gZ6b0td%2BWOZsHHWxysSo%2F0y9D2K42SaB8Y%2F%2BaD2K42SaB8Y%2F%2BahU%2BWOZsHcrxysooUeND%5C%22%7D%22%2C%22biz_params%22%3A%22%7B%5C%22vid%5C%22%3A%5C%22XMzgzOTgyMzc4MA%3D%3D%5C%22%2C%5C%22current_showid%5C%22%3A%5C%22333822%5C%22%7D%22%2C%22ad_params%22%3A%22%7B%5C%22site%5C%22%3A1%2C%5C%22wintype%5C%22%3A%5C%22interior%5C%22%2C%5C%22p%5C%22%3A1%2C%5C%22fu%5C%22%3A0%2C%5C%22vs%5C%22%3A%5C%221.0%5C%22%2C%5C%22rst%5C%22%3A%5C%22mp4%5C%22%2C%5C%22dq%5C%22%3A%5C%22hd2%5C%22%2C%5C%22os%5C%22%3A%5C%22win%5C%22%2C%5C%22osv%5C%22%3A%5C%22%5C%22%2C%5C%22d%5C%22%3A%5C%220%5C%22%2C%5C%22bt%5C%22%3A%5C%22pc%5C%22%2C%5C%22aw%5C%22%3A%5C%22w%5C%22%2C%5C%22needbf%5C%22%3A1%2C%5C%22atm%5C%22%3A%5C%22%5C%22%7D%22%7D'
url = urllib.request.unquote(url)
headers = {
        'Cookies': '__ysuid=1541863963961Pnd; __ayft=1541863963967; __aysid=1541863963968CdA; __ayscnt=1; cna=HehtFLGYuHUCAXWEwwmLxoR3; juid=01crv4222p231h; seid=01crv4222u1fb4; referhost=; _m_h5_tk=341917efc8550b8b8f637c723453dbbb_1541867928722; _m_h5_tk_enc=e999526875a5d12c0587ac6d0dc80765; yseid=15418639690294EDlPq; yseidcount=1; ycid=0; P_pck_rm=xtDs9hH3k2RbhCJSmyglUrUJJz0qDE7qRfa%2FgyFarM2vezaFLD2eCFpaMZ0%2Fu%2FiVJuLL85bhNimg5iJaMa5%2BuFNbeCx%2FUUS17tj2a%2FZPwoogpwOYlArj9hOLD%2F%2FQwphUjaZoI4m7VF9sW4KWecbidQ%3D%3D; P_j_scl=hasCheckLogin; P_gck=NA%7CCu39mPjfMlXLrTg2JFqIWQ%3D%3D%7CNA%7C1541863998507; premium_cps=1971634953__2%7C427%7C83653%7C4498__; ykss=56fae65b0fe085de1a5c0119; ypvid=1541864062919x5LuHQ; ysestep=3; yseidtimeout=1541871262922; ystep=3; P_sck.sig=irWJiULgzy2sCrRDDngwjq_JQ9_k1iRCk_t5QUp5uNU; P_sck=BGkp%2FWD2omAxvOUy4AFH3Wm%2Bfe78bxaASn%2BJGmrzJGZ0EL73N2GEJLmrg8NIbZrjaGiZK%2BXf7ZGgS5WWHGcGJT6xmpMC0Nw9qNC10mMZFm5oy9v1AHzildE7WaSFozRESz6NrqcnHhz4RG65ULXv8A%3D%3D; __ayvstp=13; __aysvstp=13; isg=BI-P3yD2CGCWoQyca-LTkaCcHiNZHMgBTAQMWaGcK_4FcK9yqYRzJo1hduDrCLtO; __arpvid=1541864347034O5bAs4-1541864347067; __arycid=dz-3-00; __arcms=dz-3-00; __aypstp=5; __ayspstp=5; seidtimeout=1541866153726',
        'Host': 'acs.youku.com',
        'Referer': 'https://v.youku.com/v_show/id_XMzgzOTgyMzc4MA==.html?spm=a2hww.20027244.m_250379.5~5~1~3!2~A',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}
response = requests.get(url, headers=headers, verify=False, proxies=proxies)
print(response.text)
