# -*- coding: utf-8 -*-
import scrapy
from ..items import QuoteItem
from traceback import format_exc, print_exc

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        global next
        quotes = response.css('.quote')
        for quote in quotes:
            item = QuoteItem()
            item['text'] = quote.css('.text::text').extract_first()
            item['author'] = quote.css('.author::text').extract_first()
            item['tags'] = quote.css('.tags .tag::text').extract()
            yield item
        try:
            next = response.css('.pager .next a:attr(href)').extract_first()
        except Exception as e:
            _ = e   # 接收异常
            next = None
        if next:
            url = response.urljoin(next)
            yield scrapy.Request(url=url, callback=self.parse)
