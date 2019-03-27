# -*- coding: utf-8 -*-

from scrapy import Item, Field

class VczhItem(Item):
    table = 'followig'
    id = Field()
    avatar_url = Field()
    name = Field()
    gender = Field()
    headline = Field()
    person_url = Field()
    follower_count = Field()
    answer_count = Field()
    articles_count = Field()