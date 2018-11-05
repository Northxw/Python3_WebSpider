# -*- coding:utf-8 -*-
"""
Created at 15:49 on Sep 24,2018
@title: Spider Maoyan Top100
@author: Northxw
"""

import requests
import re
import json
from requests.exceptions import RequestException
import time

def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'Cookie': '__mta=246739515.1536592649404.1537714713955.1537771862699.20; uuid_n_v=v1; uuid=A14181E0B50C11E8931C43FA953517EDB7F927FACF434352868294D23195FD68; _lxsdk_cuid=165c40f1bb3c8-0cd1f04a8c6994-5701631-100200-165c40f1bb31d; _lxsdk=A14181E0B50C11E8931C43FA953517EDB7F927FACF434352868294D23195FD68; _csrf=052f202ba24c2eae0c8782b859666f0bef5730a61c8778468ac00cc6a85046ec; _lxsdk_s=1660a5878c9-d20-188-29d%7C%7C2',
        }
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
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

def main(offset):
    url = 'http://maoyan.com/board/4?offset={}'.format(str(offset))
    html = get_one_page(url)
    for item in parse_one_page(html):
        write_to_file(item)

if __name__ == '__main__':
    for i in range(10):
        main(offset=i*10)
        time.sleep(1)