# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
import logging

class UAMiddleware(object):
    def __init__(self):
        # 添加UA
        self.ua_list = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 ',
            '(KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
            'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
            'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
        ]

    def process_request(self, request, spider):
        user_agent = random.choices(self.ua_list)
        request.headers['User-Agent'] = user_agent
        # 通过打印日志查看随机User-Agent
        # logging.info(request.url)
        # logging.info(request.headers['User-Agent'])

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass