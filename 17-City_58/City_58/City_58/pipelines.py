# -*- coding:utf-8 -*-

from scrapy.exceptions import DropItem
from pymongo import MongoClient
from scrapy.conf import settings
from pymongo.errors import DuplicateKeyError
from traceback import format_exc
from .items import City58XiaoQu, City58ItemChuZuInfo


class City58Pipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.client = None
        self.db = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGODB_URI'),
            mongo_db=settings.get('MONGODB_DATABASE', 'items')
        )

    def open_spider(self, spider):
        _ = spider
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db['city58_info'].ensure_index('id', unique=True)          # 在表 city58_info 中建立索引，并保证索引的唯一性
        self.db['city58_chuzu_info'].ensure_index('url', unique=True)   # 在表 city58_chuzu_info 中建立索引，并保证索引的唯一性

    def close_spider(self, spider):
        _ = spider
        self.client.close()

    def process_item(self, item, spider):
        try:
            if isinstance(item, City58XiaoQu):    # 判断是否是小区的item
                self.db['city58_info'].update({'id': item['id']}, {'$set': item}, upsert=True)   # 通过id判断，有就更新，没有就插入
            elif isinstance(item, City58ItemChuZuInfo): # 判断是否是小区出租信息的item
                try:
                    fangjia = HandleFangjiaPipline.price_per_square_meter_dict[item['id']]  # 把HandleFangjiaPipline管道的字典price_per_square_meter_dict中每平米平均价格赋值给fangjia
                    # del HandleFangjiaPipline.price_per_square_meter_dict[item['id']]
                    item['price_pre'] = fangjia

                    self.db['city58_chuzu_info'].update({'url': item['url']}, {'$set': item}, upsert=True)   # 通过url判断，有就更新，没有就插入
                except Exception as e:
                    print(e)

        except DuplicateKeyError:
            spider.logger.debug(' duplicate key error collection')  # 唯一键冲突报错
        except Exception as e:
            _ = e
            spider.logger.error(format_exc())
        return item


class HandleZuFangPipline(object):

    def process_item(self, item, spider):
        _ = spider, self
        # self.db[self.collection_name].insert_one(dict(item))
        # 判断进来的item是否是City58ItemXiaoChuZuQuInfo，是否含有面积参数
        if isinstance(item, City58ItemChuZuInfo) and 'mianji' in item:
            item['chuzu_price_pre'] = int(item['zu_price']) / int(item['mianji'])   # 租金除以面积得到平均价格
        return item


class HandleFangjiaPipline(object):

    price_per_square_meter_dict = dict()

    def process_item(self, item, spider):
        _ = spider

        # 判断传进来的item是否是个字典，并且是否含有price_list
        if isinstance(item, dict) and 'price_list' in item:
            item['price_list'] = [int(i) for i in item['price_list']]
            if item['price_list']:
                self.price_per_square_meter_dict[item['id']] = sum(item['price_list']) / len(item['price_list'])  # 得到每个小区的平均价格
            else:
                self.price_per_square_meter_dict[item['id']] = 0
            raise DropItem()
        return item