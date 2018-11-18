# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class Images360Item(Item):
    # MongoDB、Mysql存储的表格名称
    collection = table = 'images'
    # ID
    id = Field()
    # 链接
    url = Field()
    # 标题
    title = Field()
    # 缩略图
    thumb = Field()
