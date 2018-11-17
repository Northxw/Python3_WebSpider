# -*- coding:utf-8 -*-

"""
Updated at 23:57 at Nov 17,2018
@title: 使用urllib库爬取博客园文章并存储至MongoDB
@author: Northxw
"""

from urllib import request, error, parse
from pyquery import PyQuery as pq
from tqdm import tqdm
from colorama import init, Fore
import pymongo
import time

init(autoreset=True)

# 创建数据库链接
client = pymongo.MongoClient('localhost')
db = client['cnblogs']
collection = db['home']

def get_data(url, page):
    """
    获取博客园文章信息
    :return: HTTPResponse
    """
    global _request
    if page:
        # 设置请求头
        headers = {
            'origin': 'https://www.cnblogs.com',
            'referer': 'https://www.cnblogs.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

        # 设置请求参数
        payload = {
            'CategoryId': 808,
            'CategoryType': "SiteHome",
            'ItemListActionName': "PostList",
            'PageIndex': page,
            'ParentCategoryId': 0,
            'TotalPostCount': 4000,
        }
        # 编码
        data = bytes(parse.urlencode(payload), encoding='utf-8')
        # 构建Request类
        _request = request.Request(url=url, headers=headers, data=data, method='POST')
    else:
        _request = request.Request(url=url)

    try:
        response = request.urlopen(_request)
        if response.status == 200:
            return response
    except error.HTTPError as e:
        print(e.reason, e.code, sep='\n')
        return None
    except error.URLError as e:
        print(e.reason)
        return None

def parse_data(response):
    """
    解析数据
    :param response: HTTPResponse
    :return: None
    """
    # 获取网页源代码
    html = response.read().decode('utf-8')
    doc = pq(html)
    # 获取包含文章信息的div节点
    divs = doc('.post_item').items()
    # 存储列表
    data = []
    for div in divs:
        _data = {
            # 文章标题
            'title': div.find('.titlelnk').text(),
            # 文章详情页链接
            'url': div.find('.titlelnk').attr('href'),
            # 文章简介
            'short': div.find('.post_item_summary').text(),
            # 博主
            'author': div.find('.post_item_foot .lightblue').text(),
            # 博主的主页链接
            'author_url': div.find('.post_item_foot .lightblue').attr('href'),
            # 发布时间
            'create_time': div.find('.post_item_foot').text().split()[2] + ' ' + div.find('.post_item_foot').text().split()[3],
            # 评论数
            'comment_counts': div.find('.article_comment .gray').text(),
            # 阅读量
            'read_counts': div.find('.article_view .gray').text(),
        }
        data.append(_data)
    return data

def save_data(data):
    """
    存储数据至MongoDB
    :param data: 解析的数据
    :return: None
    """
    collection.insert(data)

def main(url, page=''):
    """
    主函数
    :param url: 访问链接
    :return: None
    """
    # 获取数据
    response = get_data(url, page)
    # 解析数据
    data = parse_data(response)
    # 存储数据
    save_data(data)

if __name__ == '__main__':
    print(Fore.RED + '提示：本次抓取范围仅限博客园最新文章, 测试仅抓取前10页数据！\n')
    global url
    for i in tqdm(range(10), desc='抓取进度', ncols=100):
        if i == 0:
            url = 'https://www.cnblogs.com/'
            main(url)
        else:
            url = 'https://www.cnblogs.com/mvc/AggSite/PostList.aspx'
            main(url, i+1)
        time.sleep(1)