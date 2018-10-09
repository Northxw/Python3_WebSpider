# -*- coding:utf-8 -*-
"""
Created at 17:55 on Oct 9,2018
@title: Spider Cnblogs
@author: Northxw
"""
import requests
from requests.exceptions import RequestException
from fake_useragent import UserAgent
from tqdm import tqdm
import re
import json
import time
from colorama import init, Fore     # Init is initialization, Fore is font color
from numba import jit

init(autoreset=True)    # initialization

def get_one_page(url):
    """Crawl a page of data"""
    try:
        headers = {
            'cookie': '_ga=GA1.2.2123979422.1532526623; sc_is_visitor_unique=rx9614694.1536243635.58D4766D9BB84FF016DB9E8CB39B14B3.1.1.1.1.1.1.1.1.1; UM_distinctid=165b39bf157a77-0ee7c86ae52855-9393265-100200-165b39bf15815b; CNZZDATA3347352=cnzz_eid%3D1097075551-1536313719-%26ntime%3D1536313719; CNZZDATA2075317=cnzz_eid%3D1691069303-1536667395-https%253A%252F%252Fwww.baidu.com%252F%26ntime%3D1536667395; .CNBlogsCookie=5249527B2050D4918BB0BAD4CDEBF68C1B944FA901250F9E0E4B59680B7B2453D94AAB797394B864F4C3DD6F1999BBC5F6533FE4CBF0F9687A9BDCA7C0AB9CBD0EFA40C83F68505313CFB124162477EF3448E321; .Cnblogs.AspNetCore.Cookies=CfDJ8J0rgDI0eRtJkfTEZKR_e81ZoupkFn_MiCU_ybwtb5e0z3MKoSnFruRc-zmuj9RAQu0yeGJvY_69FiCZaLPs7g4h6ER1Nf23tSUkkM2lYmlC3mkA44WqKm8UL_R3pawnmkudFIDDKwlrgIONNKp589YUBdRgAzpDdStfYLM5xedqeBrwPv1dCBsIpE3l598o2stLS-AnNtDjCI2RoJyeqgcFA1Ga_rMw8vHG-f9rzTAuGktD5MhLPjfsjRlP7_dC5PQzap0qRhWEfqwBH8VViVji36rxOIgnqTCWykyimDOKKLjCCDfqfD9sTqZjPi5TPA; _gid=GA1.2.181860646.1537774593',
            'User-Agent': UserAgent().random
        }
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html, key):
    """Parse the data of the current page"""
    pattern = ''
    if key == '首页' or key == '精华':
        pattern = re.compile(r'.*?post_item_body.*?<h3>.*?titlelnk.*?href="(.*?)".*?_blank.*?>(.*?)</a>'
                             r'.*?post_item_summary.*?</a>(.*?)</p>'
                             r'.*?post_item_foot.*?href="(.*?)".*?lightblue.*?>(.*?)</a>(.*?)<span'
                             r'.*?article_comment.*?gray.*?>(.*?)</a>.*?article_view.*?gray.*?>(.*?)</a>',
                             re.S)
    if key == '新闻':
        pattern = re.compile(r'.*?post_item_body.*?<h3>.*?titlelnk.*?href="(.*?)".*?_blank.*?>(.*?)</a>'
                             r'.*?post_item_summary.*?</a>(.*?)</p>'
                             r'.*?post_item_foot.*?href="(.*?)".*?_blank.*?>(.*?)</a>(.*?)<span'
                             r'.*?article_comment.*?_blank.*?>(.*?)</a>.*?article_view.*?_blank.*?>(.*?)</a>',
                             re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'article_title': item[1],
            'title_link': item[0] or html.unescape(item[0]),  # Handling HTML entities
            'article_Introduction': item[2].strip() if len(item[2]) < 500 else 'Please check out {}'.format(item[0]),
            'release_time': item[5].strip()[4:],
            'blogger': item[4].strip(),
            'blogger_homepage': item[3],
            'comments': item[6].strip(),
            'reading_volume': item[7].strip()
        }


def write_to_file(content, key):
    """Write a single piece of data to a file"""
    save_file_name = ''
    if key == '首页':
        save_file_name = './Cnblog_HomePage.txt'    # Default Storage path
    if key == '精华':
        save_file_name = './Cnblog_Essence.txt'
    if key == '新闻':
        save_file_name = './Cnblog_News.txt'
    with open(save_file_name, 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n\n')

@jit
def main(offset, key):
    """Main function"""
    url = ''
    if key == '首页':
        url = 'https://www.cnblogs.com/#p{}'.format(str(offset))    # Default crawl page
    if key == '精华':
        url = 'https://www.cnblogs.com/pick/#p{}'.format(str(offset))
    if key == '新闻':
        url = 'https://www.cnblogs.com/news/#p{}'.format(str(offset))
    response = get_one_page(url)
    for item in parse_one_page(response, key):
        write_to_file(item, key=key)

if __name__ == '__main__':
    print(Fore.RED + "本次爬取的简讯包含首页,精华页,新闻页！(每个标题默认爬取50页)\n")
    keys = ['首页', '精华', '新闻']
    for key in keys:
        print(Fore.GREEN + "{}页面爬取进度: ".format(key))
        for i in tqdm(range(50), desc='Spider_Cnblogs_{}'.format(key), ncols=100):
            main(i+1, key=key)
            time.sleep(0.1)