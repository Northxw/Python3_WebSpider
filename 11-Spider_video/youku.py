# -*- coding:utf-8 -*-

import requests
import json
import os
from tqdm import tqdm
from time import sleep
from requests.exceptions import RequestException

# 代理服务器
proxy_host = 'proxy.abuyun.com'
proxy_port = '9020'

# 代理隧道验证信息
proxy_user = 'H6548Q175X734TVD'
proxy_pass = '58C80217BA96BE32'

proxy_meta = 'http://%(user)s:%(pass)s@%(host)s:%(port)s' % {
    'host': proxy_host,
    'port': proxy_port,
    'user': proxy_user,
    'pass': proxy_pass,
}

# 代理参数
proxies = {
    'http': proxy_meta,
    'https': proxy_meta,
}

def get_data(url):
    """
    获取JSON数据
    :param url: 请求JSON数据的URL
    :return: response
    """
    # 请求头
    headers = {
        'Cookie': 'juid=01cj8htt1h1lvi; __ysuid=15325168289795LT; cna=AzDeEyVuqmMCAXUg2DO6oFt3; __aysid=1541674466021cjs; __ayft=1541764263557; __ayscnt=1; ycid=0; __utmarea=; referhost=http%3A%2F%2Fwww.youku.com; yseid=1541853246802W4hJ2Z; yseidcount=74; P_ck_ctr=C66CDA141C0BD97FE4F31B1483CD04B3; global_csrf_token=e6ea7dcf-6f3e-4fc8-85aa-5f594e30a917; csrfToken=MpL_DJ7zjt00pi13DPbmTUvj; P_j_scl=hasCheckLogin; P_pck_rm=xtDs9hH3k2RbhCJSmyglUqIFCMpWucVMnWIeQZZcsvmNwwCG4AdYd9z%2BNZpRO3KYlqC5gzzXs4GKEq7dSs1jfWSX2nKdaBS6iN9WbqLuUu5DfvDrUBaHX0Pe%2Bre1%2FAdoRezTc3eZ8C4j7YfvUvCRjw%3D%3D; P_gck=NA%7CCu39mPjfMlXLrTg2JFqIWQ%3D%3D%7CNA%7C1541853386451; ykss=ced0e65be32026011d7ae222; P_ck_ctl=74FD3B6779FC47ACB742C135370E2381; premium_cps=1965086768_2%7C550%7C85148%7C72_2%7C427%7C83653%7C4498__; rpvid=1541853612209YWjM9p-1541853617813; _m_h5_tk=827868f6fb0e50cea21d91d9f6306aa4_1541859257057; _m_h5_tk_enc=2d563efff97971355878c942a620e283; isg=BMXFN8_QMqLQnhbAbj4PBFR81AE_Kni98jq2-8cvPPw7XurQiNAo5Zd3bMINHpHM; seid=01cruuhf1e16am; ypvid=15418581837844Aor6O; ysestep=4; yseidtimeout=1541865383786; ystep=262; __ayvstp=449; __aysvstp=536; P_sck=BGkp/WD2omAxvOUy4AFH3Zx0e3iSPetM5FYhxOEAmEvanaiENjuD2sYS2r8la4xdTTpnHp2wXgmjwTPEAre7biKd5pSN+jGLDEV8GORcPRtaDI86yEUMid+Kyu9FnZ8EsGN7EziKbhg+JNTIb2gwIw==; P_sck.sig=dwyLI0SYvP3d4YWb5DSv2GoM-TQo8JGwY01g7yUwlwo; __arpvid=1541858188528hF23Bv-1541858188551; __arycid=dz-3-00; __arcms=dz-3-00; __aypstp=51; __ayspstp=54; seidtimeout=1541859998012',
        'Host': 'acs.youku.com',
        'Referer': 'https://v.youku.com/v_show/id_XMzgzOTgyMzc4MA==.html?spm=a2hww.20027244.m_250379.5~5~1~3!2~A',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }
    # 获取数据
    try:
        response = requests.get(url, headers=headers, verify=False,  proxies=proxies)
        # 判断状态码
        if response.status_code == 200:
            return response
    except RequestException:
        print('Something Wrong!')
        return None

def handle_data(response):
    """
    处理JSON数据
    :param response: 获取的JSON数据
    :return: 视频播放地址组成的列表
    """
    # 存放视频播放地址
    urls = []
    # 将获取的response处理为JSON对象
    data = json.loads(response.text)
    # 获取包含视频信息的字段
    stream = data.get('data').get('data').get('stream')[2].get('segs')  # 获取第三个字段是因为视频的清晰度最高！
    # 获取URL列表
    for i in len(range(stream)):
        urls.append(stream[i].get('cdn_url'))
    return urls

def download(urls):
    """
    下载视频
    :param urls: 视频播放地址组成的列表
    :return: None
    """
    save_dir = './video/我不是药神.mp4'
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    print('正在下载我不是药神：')
    for i in tqdm(range(len(urls)), desc='下载进度', ncols=100):    # 显示进度条
        response = requests.get(urls[i])
        with open(save_dir, 'ab') as f:
            f.write(response.content)
        sleep(0.5)

def main():
    """
    主函数
    :return:
    """
    # 真实请求
    url = 'https://acs.youku.com/h5/mtop.youku.play.ups.appinfo.get/1.1/?jsv=2.4.16&appKey=24679788&t=1541858200813&sign=0615dd3052bafd676ce87fcd328bf2a4&api=mtop.youku.play.ups.appinfo.get&v=1.1&timeout=20000&YKPid=20160317PLF000211&YKLoginRequest=true&AntiFlood=true&AntiCreep=true&type=jsonp&dataType=jsonp&callback=mtopjsonp1&data=%7B%22steal_params%22%3A%22%7B%5C%22ccode%5C%22%3A%5C%220502%5C%22%2C%5C%22client_ip%5C%22%3A%5C%22192.168.1.1%5C%22%2C%5C%22utid%5C%22%3A%5C%22AzDeEyVuqmMCAXUg2DO6oFt3%5C%22%2C%5C%22client_ts%5C%22%3A1541858200%2C%5C%22version%5C%22%3A%5C%220.5.87%5C%22%2C%5C%22ckey%5C%22%3A%5C%22DIl58SLFxFNndSV1GFNnMQVYkx1PP5tKe1siZu%2F86PR1u%2FWh1Ptd%2BWOZsHHWxysSfAOhNJpdVWsdVJNsfJ8Sxd8WKVvNfAS8aS8fAOzYARzPyPc3JvtnPHjTdKfESTdnuTW6ZPvk2pNDh4uFzotgdMEFkzQ5wZVXl2Pf1%2FY6hLK0OnCNxBj3%2Bnb0v72gZ6b0td%2BWOZsHHWxysSo%2F0y9D2K42SaB8Y%2F%2BaD2K42SaB8Y%2F%2BahU%2BWOZsHcrxysooUeND%5C%22%7D%22%2C%22biz_params%22%3A%22%7B%5C%22vid%5C%22%3A%5C%22XMzgzOTgyMzc4MA%3D%3D%5C%22%2C%5C%22current_showid%5C%22%3A%5C%22333822%5C%22%7D%22%2C%22ad_params%22%3A%22%7B%5C%22site%5C%22%3A1%2C%5C%22wintype%5C%22%3A%5C%22interior%5C%22%2C%5C%22p%5C%22%3A1%2C%5C%22fu%5C%22%3A0%2C%5C%22vs%5C%22%3A%5C%221.0%5C%22%2C%5C%22rst%5C%22%3A%5C%22mp4%5C%22%2C%5C%22dq%5C%22%3A%5C%22hd2%5C%22%2C%5C%22os%5C%22%3A%5C%22win%5C%22%2C%5C%22osv%5C%22%3A%5C%22%5C%22%2C%5C%22d%5C%22%3A%5C%220%5C%22%2C%5C%22bt%5C%22%3A%5C%22pc%5C%22%2C%5C%22aw%5C%22%3A%5C%22w%5C%22%2C%5C%22needbf%5C%22%3A1%2C%5C%22atm%5C%22%3A%5C%22%5C%22%7D%22%7D'
    response = get_data(url)
    urls = handle_data(response)
    download(urls)

if __name__ == '__main__':
    main()