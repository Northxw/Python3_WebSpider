# -*- coding:utf-8 -*-

"""
Created at 21:04 at March 12,2019
@title: 爬取36kr的最新文章信息并保存至Mysql数据库
@author: Northxw
"""

from tqdm import tqdm
from colorama import init, Fore
from icon.word import show
from fake_useragent import UserAgent
from requests.exceptions import RequestException
import requests
import pymysql
import time
import re

init(autoreset=True)

def connect_db():
    """
    连接Mysql数据库
    :return: db
    """
    db = pymysql.connect(host='localhost', user='root', password='******', port=3306, db='36kr')
    # print('数据库连接成功!')
    return db

def get_one_page(page):
    """
    获取一页的最新文章JSON数据
    :param page: 页码
    :return: json
    """
    # 真实请求
    url = 'https://36kr.com/api/search-column/mainsite?per_page=20&page={}'.format(str(page))
    # 设置Headers
    headers = {
        'User-Agent': UserAgent().random,
        'Referer': 'https://36kr.com/',
        'Host': '36kr.com'
    }
    # 获取网页源代码
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            items = response.json()['data']['items']
            return items
        return None
    except RequestException:
        return None

def parse_one_page(items):
    """
    解析获取的JSON数据
    :param items: 获取的JSON数据段items
    :return: dict
    """
    # 存储单页总数据
    datas = list()
    for item in items:
        data= {
            # 文章ID
            'id': str(item['id']),
            # 标题
            'title': item['title'],
            # 类别
            'column_name': item['column_name'],
            # id
            'column_id': item['column_id'],
            # 封面图片链接
            'cover': item['cover'],
            # 发布时间
            'publish_time': item['published_at'] ,
            # 文章总结
            'summary': item['summary']
        }
        # 处理时间
        data['publish_time'] = re.search('(.*?)T(.*?)\+.*', data['publish_time']).group(1) + ' ' + re.search('(.*?)T(.*?)\+.*', data['publish_time']).group(2)
        # 存储
        datas.append(data)
        # 将标题写入文件.制作中文词云
        with open('./icon/36kr.txt', 'a', encoding='utf-8') as f:
            f.write(data['title'])
    return datas

def save_to_mysql(datas):
    """
    将解析数据存储到Mysql数据库
   :param item: 获取的单页有效数据
    :return: None
    """
    # 连接数据库
    db = connect_db()
    # 获得Mysql操作指针
    cursor = db.cursor()
    # sql
    sql = "INSERT INTO kr(id, article_title, colum_name, colum_id, cover, publish_time, summary) " \
          "VALUES(%s, %s, %s, %s, %s, %s, %s)"
    for _item in datas:
        try:
            # 插入数据
            cursor.execute(sql, (_item['id'], _item['title'], _item['column_name'],
                                 _item['column_id'], _item['cover'], _item['publish_time'], _item['summary']))
            # 提交
            db.commit()
            # print('数据插入成功!')
        except Exception as e:
            # print('数据插入失败!',e)
            db.rollback()
    # 关闭数据库连接
    db.close()

def main():
    """
    主函数
    :return: None
    """
    print(Fore.RED + '提示：截止目前的总数据量是77998条, 测试仅抓取前10页的共200条数据!\n')
    for i in tqdm(range(10),  desc='抓取进度'):
        # 获取
        items = get_one_page(i+1)
        # 解析
        data = parse_one_page(items)
        # 保存
        save_to_mysql(data)
        time.sleep(1)

if __name__ == '__main__':
    main()
