# -*- coding: utf-8 -*-

import json
import scrapy
import time
import logging
from urllib.parse import urlencode
from scrapy import Request
from ..items import VczhItem
from scrapy.mail import MailSender
from ..pipelines import COUNT_IMAGES_NUMS

class VcSpider(scrapy.Spider):
    start = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    name = 'vc'
    allowed_domains = ['www.zhihu.com']
    base_url = 'https://www.zhihu.com/api/v4/members/excited-vczh/followees?'
    logger = logging.getLogger(__name__)

    def start_requests(self):
        data = {
            'include': 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics',
            'limit': 20
        }
        for page in range(1, self.settings.get('MAX_PAGE') + 1):
            data['offset'] = page * 20
            params = urlencode(data)
            url = self.base_url + params
            yield Request(url, callback=self.parse, errback=self.error_back)

    def parse(self, response):
        result = json.loads(response.text)
        for data_ in result.get('data'):
            item = VczhItem()
            item['id'] = data_.get('id')
            item['avatar_url'] = data_.get('avatar_url').replace('_is', '')
            item['name'] = data_.get('name')
            item['gender'] = data_.get('gender')
            item['headline'] = data_.get('headline')
            item['person_url'] = data_.get('url'),
            item['follower_count'] = data_.get('follower_count')
            item['answer_count'] = data_.get('answer_count')
            item['articles_count'] = data_.get('articles_count')
            yield item


    def closed(self, reason):
        """
        爬虫关闭发送通知邮件
        """
        # 爬虫完成时间
        fnished = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        # 创建邮件发送对象
        mail = MailSender.from_settings(self.settings)
        # 邮件内容
        body = "爬虫名称: {}\n\n 开始时间: {}\n\n 请求成功总量：{}\n 图片下载总量：{}\n 数据库存储总量：{}\n\n 结束时间  : {}\n".format(
            '知乎轮子哥粉丝爬虫',
            str(self.start),
            str(self.crawler.stats.get_value("normal_response")),
            str(COUNT_IMAGES_NUMS['IMAGES_NUMS']),
            str(self.crawler.stats.get_value("success_insertdb")),
            str(str(fnished)))
        # 发送邮件
        mail.send(to=self.settings.get('RECEIVE_LIST'), subject=self.settings.get('SUBJECT'), body=body)

    def error_back(self, e):
        _ = self
        # 打印错误信息到日志
        self.logger.error('Error: {}'.format(e.reason))