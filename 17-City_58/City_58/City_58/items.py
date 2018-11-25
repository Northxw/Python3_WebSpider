# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class City58XiaoQu(scrapy.Item):
    """
    小区详情页数据
    """
    id = scrapy.Field()
    name = scrapy.Field()
    location = scrapy.Field()
    price = scrapy.Field()
    address = scrapy.Field()
    times = scrapy.Field()

class City58ItemChuZuInfo(scrapy.Item):
    """
    小区出租房页数据
    """
    id = scrapy.Field()                 # 关联小区信息
    name = scrapy.Field()
    zu_price = scrapy.Field()
    mianji = scrapy.Field()
    type = scrapy.Field()
    chuzu_price_pre = scrapy.Field()    # 每平米的房价
    url = scrapy.Field()                # 出租房页面的唯一ID
    price_pre = scrapy.Field()          # 存储每个出租房的每平米房价