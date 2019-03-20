# -*- coding:utf-8 -*-

"""
Crated at 07:34 at March 20,2019
@title: 使用Appium + Mitmdump 自动化爬取抖音视频
@author: Northxw
"""

import requests
import os

def response(flow):
    """
    爬取抖音短视频
    """
    urls = list()
    # 抖音短视频接口
    nums = [1,3,6,9]
    for num in nums:
        url_first = 'http://v{}-dy.ixigua.com/'.format(str(num))
        url_second = 'http://v{}-dy-x.ixigua.com'.format(str(num))
        url_third = 'http://v{}-dy-z.ixigua.com'.format(str(num))
        url_fouth = 'http://v{}-dy-y.ixigua.com'.format(str(num))
        urls.extend([url_first, url_second, url_third, url_fouth])

    for url in urls:
        if flow.request.url.startswith(url):
            # 取URL中取值唯一的部分作为文件名称
            video_name = flow.request.url.split('/')[3]
            # 获取视频的二进制内容
            content = requests.get(flow.request.url, stream=True).content
            # 判断文件路径是否存在
            save_dir = './video'
            if not os.path.exists(save_dir):
                os.mkdir(save_dir)
            # 视频存储路径
            save_dir = '{}/{}.mp4'.format(save_dir, video_name)

            # 存储
            with open(save_dir, 'wb') as f:
                f.write(content)