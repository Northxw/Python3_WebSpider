# -*- coding:utf-8 -*-

"""
Updated at 9:45 at March 18, 2019
@title: 爬取得到APP电子书信息并将数据存储至MongoDB
@author: Northxw
"""

import time
import json
# import pymongo
from mitmproxy import ctx

"""
class DedaoMongo(object):
    def __init__(self):
        # set client
        self.client = pymongo.MongoClient('localhst', 27017)
        # db
        self.db = self.client['dedao']
        # set
        self.collection = self.db['ebook']

    def update_book(self, book_info):
        self.collection.insert_one(book_info)

"""

def response(flow):
    """
    抓取得到APP电子书信息, 包含书本ID、书名、封面图片、推荐语、发布时间、当前时间、当前价格、内容简介等。
    """
    # data_ = DedaoMongo()
    url = 'https://entree.igetget.com/ebook2/v1/ebook/list'
    if flow.request.url.startswith(url):
        text = flow.response.text
        data = json.loads(text)
        info = ctx.log.info
        books = data.get('c').get('list')

        ebooks = list()
        # 获取电子书信息
        for book in books:
            ebook_data = {
                # ID
                'id': str(book['id']),
                # 书名
                'name': book['operating_title'],
                # 封面
                'ico': book['cover'],
                # 推荐语
                'share_summary': book['other_share_summary'],
                # 发布时间
                'publish_time': book['datetime'],
                # 当前价格
                'current_price': book['current_price'],
                # 内容简介
                'book_intro': book['book_intro'],
            }
            # data_.update_book(ebook_data)

            # 终端显示已获取到的信息
            info('ID：' + ebook_data['id'])
            info('书名：' + ebook_data['name'])
            info('推荐语：' + ebook_data['share_summary'])
            info('发布时间：' + ebook_data['publish_time'])
            info('当前价格：' + '¥{}'.format(ebook_data['current_price']))
            info('封面：' + ebook_data['ico'])
            info('内容简介：' + ebook_data['book_intro'])
            info('-' * 80)

            # 存储为JSON格式
            with open('./dedao.json', 'a', encoding='utf-8') as f:
                f.write(json.dumps(ebook_data, indent=2, ensure_ascii=False))
                f.write(', \n')