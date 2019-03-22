# -*- coding: utf-8 -*-

import json
import scrapy
import time
from ..sendemail import *
from urllib.parse import urlencode
from scrapy import Request
from ..items import VczhItem

class VcSpider(scrapy.Spider):
    start = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    name = 'vc'
    allowed_domains = ['www.zhihu.com']
    base_url = 'https://www.zhihu.com/api/v4/members/excited-vczh/followees?'

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
        EmailSenderClient = EmailSender()
        receive_list = ['northxw@gmail.com', 'northxw@qq.com']
        fnished = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        subject = "爬虫状态报告!"
        body = "爬虫名称: {}\n\n, 开始时间: {}\n 请求成功总量：{}\n 数据库存储总量：{}\n 下载头像总量：{}\n 结束时间  : {}\n".format(
            '知乎轮子哥粉丝爬虫',
            str(self.start),
            str(COUNT_SUCCESS_REQUEST['Request_Success']),
            str(COUNT_SUCCESS_DB['Storage_Success']),
            str(RESPONSE_STATUS['Download_Success']),
            str(str(fnished)),
        )
        EmailSenderClient.sendEmail(receive_list, subject, body)


    def error_back(self, e):
        _ = self
        self.logger.debug('Request Error: {}'.format(e))