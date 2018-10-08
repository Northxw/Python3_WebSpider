# -*- coding:utf-8 -*-
"""
Created on Mon Sep 17 21:27:00 2018
@author: Northxw
"""
import requests
import os

# Get the list of all heroes
herolist_url = 'https://pvp.qq.com/web201605/js/herolist.json'
response = requests.get(herolist_url).json()    # Returns the JSON data that contains all the heroes.

# According to the hero's skin link, analyze and download the hero's skin.
save_dir = "E:\Python\Spider\Ex\\01-Spider_Glory_of_Kings\hero_list\\"  # Specify download location
if not os.path.exists(save_dir):    # Determine whether storage path exists, no creation
    os.mkdir(save_dir)

for i in range(len(response)):
    # Get hero skin list
    skin_names = response[i]['skin_name'].split('|')
    for cnt in range(len(skin_names)):
        # Download all skin of current hero
        hero_num = response[i]['ename']     # hero num
        hero_name = response[i]['cname']    # hero name
        skin_name = skin_names[cnt]         # skin name

        save_file_name = save_dir + str(hero_num) + '-' + hero_name + '-' + skin_name + '.jpg'  # save_dir
        skin_url = 'http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/{}/{}-bigskin-{}.jpg'.format(hero_num, hero_num, str(cnt+1))
        response_skin_content = requests.get(skin_url).content      # Get the bit data of the picture

        with open(save_file_name, 'wb') as f:
            f.write(response_skin_content)