# -*- coding:utf-8 -*-
"""
Created at 21:27 at Sep 17,2018
@author: Northxw
"""

import requests
import os

# 全英雄列表请求链接
herolist_url = 'https://pvp.qq.com/web201605/js/herolist.json'
# 获取数据
response = requests.get(herolist_url).json()

# 根据英雄的皮肤链接，分析并下载英雄的皮肤
save_dir = "E:\Python\Spider\Ex\\01-Spider_Glory_of_Kings\hero_list\\"  # 指定下载位置
if not os.path.exists(save_dir):
    os.mkdir(save_dir)

for i in range(len(response)):
    # 获取英雄皮肤列表
    skin_names = response[i]['skin_name'].split('|')
    for cnt in range(len(skin_names)):
        # 下载当前英雄的所有皮肤
        hero_num = response[i]['ename']     # 英雄序号
        hero_name = response[i]['cname']    # 英雄名称
        skin_name = skin_names[cnt]         # 皮肤名称

        save_file_name = save_dir + str(hero_num) + '-' + hero_name + '-' + skin_name + '.jpg'
        skin_url = 'http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/{}/{}-bigskin-{}.jpg'.format(hero_num, hero_num, str(cnt+1))
        # 获取图片的位数据(二进制流数据)
        response_skin_content = requests.get(skin_url).content
        # 保存图片
        with open(save_file_name, 'wb') as f:
            f.write(response_skin_content)
