# -*- coding: utf-8 -*-

"""
Created at 22:08 at March 13,2019
@title: 爬取优酷《我不是药神仙》弹幕数据并制作词云
@author: Northxw
"""

from fake_useragent import UserAgent
from requests.exceptions import RequestException
from tqdm import tqdm
import requests
import time
import os
import re

def get_data(mat):
    """
    循环遍历爬取弹幕数据
    :param mat: 偏移量
    :return: list
    """
    # 请求链接
    url = 'https://service.danmu.youku.com/list?jsoncallback=jQuery111207035726936412456_1552483671572&mat={}&mcount=1&ct=1001&iid=959955945&aid=333822&cid=96&lid=0&ouid=0'.format(mat)
    # headers
    headers = {
        'Referer': 'https://v.youku.com/v_show/id_XMzgzOTgyMzc4MA==.html?spm=a2h0k.11417342.soresults.dplaybutton&s=c6c62a475a5d4a14ab48',
        'User-Agent': UserAgent().random
    }
    """
    # 参数
    params = {
        'jsoncallback': 'jQuery11120003560802190473389_1552479833762',
        'mat': mat,
        'mcount': '1',
        'ct': '1001',
        'id': '959955945',
        'aid': '333822',
        'cid': '96',
        'lid': '0',
        'ouid': '0'
        # '_': '1552479833815'  提示：类似时间戳,去掉后不影响数据的获取
    }
    """
    # 获取弹幕
    try:
        response = requests.get(url, headers=headers)
        print(response)
        if response.status_code == 200:
            html = response.text
            # 正则解析（结果为list类型）
            results = re.findall(',\"content\":\"(.*?)\",', html, re.S)
            # 文本存储
            save_dir = './utils/danmu.txt'
            if not os.path.exists(save_dir):  # Determine whether storage path exists, no creation
                os.mkdir(save_dir)
            with open(save_dir, 'a', encoding='utf-8') as f:
                f.write(str(results))
            return results
        return None
    except RequestException as e:
        print('Error: ', e.args)
        return None

if __name__ == '__main__':
    for i in tqdm(range(10), desc='Progress'):
        time.sleep(1)
        get_data(str(i))
