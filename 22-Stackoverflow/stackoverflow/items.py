# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class StackoverflowItem(Item):
    table = 'stackoverflow'
    link = Field()
    title = Field()
    votes = Field()
    body = Field()
    tags = Field()


