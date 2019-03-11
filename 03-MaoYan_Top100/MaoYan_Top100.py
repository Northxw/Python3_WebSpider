# -*- coding:utf-8 -*-
"""
Updated at 14:33 on March 11,2019
@title: Spider Maoyan Top100
@author: Northxw
"""

import requests
import re
import json
from requests.exceptions import RequestException
from pymongo import MongoClient
import time

# 创建数据库连接
client = MongoClient('mongodb://localhost:27017/')
db = client.maoyan
collection = db.rank

def get_one_page(url):
    """
    获取每页的网页源代码
    :param url: 请求链接
    :return: 网页的文本内容
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        }
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    """
    使用正则表达式解析网页数据
    :param html: 网页的文本内容
    :return: 字典
    """
    pattern = re.compile(
        r'<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.'
        r'*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>',
        re.S
    )
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1].split('@')[0],
            'title': item[2].strip(),
            'actor': item[3].strip()[3:] if len(item[3]) > 3 else '',
            'time': item[4].strip()[5:] if len(item[4]) > 5 else '',
            'score': item[5].strip() + item[6].strip()
        }

def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')

def save_to_mongo(item):
    """
    将数据存储到MongoDB
    :param dict: 字典类型的数据
    :return: None
    """
    collection.insert(item)

def main(offset):
    url = 'http://maoyan.com/board/4?offset={}'.format(str(offset))
    html = get_one_page(url)
    for item in parse_one_page(html):
        write_to_file(item)
        save_to_mongo(item)

if __name__ == '__main__':
    for i in range(10):
        main(offset=i*10)
        time.sleep(1)