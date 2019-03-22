# -*- coding:utf-8 -*-

from .sendemail import *
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
import pymysql

class MysqlPipeline(object):
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DB'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT')
        )

    def open_spider(self, spider):
        self.db = pymysql.connect(self.host, self.user, self.password, self.database, self.port)
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        data = dict(item)
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = "INSERT INTO %s (%s) VALUES (%s)" % (item.table, keys, values)
        try:
            self.cursor.execute(sql, tuple(data.values()))
            self.db.commit()
            # 统计存储成功的数据量
            COUNT_SUCCESS_DB['Storage_Success'] = COUNT_SUCCESS_DB['Storage_Success'] + 1
        except:
            # 存储失败,数据回滚(相当于什么都没发生)
            self.db.rollback()
        return item

    def close_spider(self, spider):
        self.db.close()


class ImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        url = request.url
        file_name = url.split('/')[-1]
        return file_name

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('Image Downloaded Failed')
        else:
            # 统计下载成功的图片总数量
            RESPONSE_STATUS['Download_Success'] = RESPONSE_STATUS['Download_Success'] + 1
        return item

    def get_media_requests(self, item, info):
        yield Request(item['avatar_url'])