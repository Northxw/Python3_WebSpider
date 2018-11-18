# -*- coding: utf-8 -*-

import scrapy
from scrapy import Spider, Request
from urllib.parse import urlencode
from ..items import Images360Item
import json

class ImagesSpider(scrapy.Spider):
    name = 'images'
    allowed_domains = ['image.so.com']

    def start_requests(self):
        # GET请求参数
        data = {
            'ch': 'photography',
            'listtype': 'new',
        }
        base_url = 'https://image.so.com/zj?'
        for page in range(1, self.settings.get('MAX_PAGE') + 1):
            # 偏移量参数
            data['sn'] = page * 30
            params = urlencode(data)
            # 完整请求链接
            url = base_url + params
            yield Request(url, self.parse)

    def parse(self, response):
        result = json.loads(response.text)
        for image in result.get('list'):
            item = Images360Item()
            item['id'] = image.get('imageid')
            item['url'] = image.get('qhimg_url')
            item['title'] = image.get('group_title')
            item['thumb'] = image.get('qhimg_thumb_url')
            yield item
