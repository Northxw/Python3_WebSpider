# -*- coding:utf-8 -*-

import requests
import os
from requests.exceptions import RequestException

def get_url(url, start):
    """
    下载TED视频
    :param url: 视频的下载地址
    :param start：请求参数
    :return:
    """
    headers = {
        'Referer': 'http://open.163.com/movie/2018/4/5/D/MDDI6OSHV_MDDI7DH5D.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'X-Requested-With': 'ShockwaveFlash/31.0.0.122'
    }
    parms = {'start': start}     # get请求的额外参数
    try:
        response = requests.get(url, headers=headers, params=parms)
        if response.status_code == 200:
            return response
    except RequestException:
        return None

def get_video(response):
    """
    下载TED演讲视频
    """
    save_dir = './video'
    name = '我与蚊子的爱恨情仇'
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    with open('{}/{}.mp4'.format(save_dir, name), 'wb') as f:
        f.write(response.content)

def main(url, start):
    """
    主函数
    :return:
    """
    response = get_url(url=url, start=start)
    get_video(response)

if __name__ == '__main__':
    url = 'http://mov.bn.netease.com/open-movie/nos/flv/2018/04/04/SDDK37STE_hd.flv?'
    start = 365352
    # 将url与参数分开方便扩展
    main(url, start)
