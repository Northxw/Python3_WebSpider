# -*- coding: utf-8 -*-

import scrapy
from scrapy import Request
from traceback import format_exc
from ..items import City58XiaoQu, City58ItemChuZuInfo
from ..utils.parse import parse_xiaoqu, parse_xiaoqu_detail, \
    get_ershoufang_list_page, get_chuzu_detail_page_list_url, get_chuzu_house_info

class A58Spider(scrapy.Spider):
    name = '58'
    allowed_domains = ['58.com']
    base_url = 'https://{}.58.com/xiaoqu/{}/'

    def start_requests(self):
        # 根据HOST和CODE构造各行政区的小区页面的URL
        for host in self.settings.get('HOST'):
            for code in self.settings.get('AREA_CODE'):
                url = self.base_url.format(host, code)
                self.logger.debug(url)
                yield Request(url=url, callback=self.parse)

    def parse(self, response):
        # 提取小区列表页的URL
        xiaoqu_url_list = parse_xiaoqu(response)
        for xiaoqu_url in xiaoqu_url_list:
            yield Request(xiaoqu_url, callback=self.xiaoqu_detail_page, errback=self.error_back)

    def xiaoqu_detail_page(self, response):
        # 提取小区详情页的数据
        xiaoqu_detail_data = parse_xiaoqu_detail(response)
        item = City58XiaoQu()
        item.update(xiaoqu_detail_data)
        item['id'] = response.url
        self.logger.debug(item)
        yield item

        # 二手房页面
        ershoufang_url = self.base_url.format(self.settings.get('HOST'), item['id']) + 'ershoufang'     # 二手房页面的完整请求链接
        yield Request(url=ershoufang_url, callback=self.ershoufang_list_page,
                      errback=self.error_back, meta={'id': item['id']})

        # 出租房页面
        chuzufang_url = self.base_url.format(self.settings.get('HOST'), item['id']) + 'chuzu'           # 出租房页面的完整请求链接
        yield Request(url=chuzufang_url, callback=self.chuzufang_detail_page,
                      errback=self.error_back, meta={'id': item['id']})

    def ershoufang_list_page(self, response):
        # 保持编码规则,在self不使用的情况下接收它
        _ = self
        # 提取二手房页面的所有房价
        price_list = get_ershoufang_list_page(response)
        yield {'id': response.item['id'], 'price_list': price_list}     # 仅计算该小区的平均房价,不做存储及其他处理

        # 翻页

    def chuzufang_detail_page_url_list(self, response):
        # 保持编码规则,在self不使用的情况下接收它
        _ = self
        # 提取出租房页面的所有详情页链接
        chuzufang_detail_url = get_chuzu_detail_page_list_url(response)
        for url in chuzufang_detail_url:
            yield Request(url=url, callback=self.chuzufang_detail_page,
                          errback=self.error_back, meta={'id': response.item['id']})

        # 翻页

    def chuzufang_detail_page(self, response):
        # 保持编码规则,在self不使用的情况下接收它
        _ = self
        # 提取出租房页面的详细数据(注意：当前时间-2018/11/24,目前了解至少从2018年9月份开始该页面已添加字体反爬, 爬取的数据已经做反反爬处理)
        chuzufang_data = get_chuzu_house_info(response)
        item = City58ItemChuZuInfo()
        item.update(chuzufang_data)
        item['id'] = response.meta['id']
        item['url'] = response.url
        yield item

    def error_back(self, e):
        _ = e
        # 打印堆栈的错误信息
        self.logger.debug(format_exc())
        pass