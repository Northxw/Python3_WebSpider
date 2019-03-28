# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from urllib.parse import urlencode
from stackoverflow.items import StackoverflowItem

class StackSpider(scrapy.Spider):
    name = 'stack'
    allowed_domains = ['stackoverflow.com/']
    base_url = 'https://stackoverflow.com/questions?'
    """
     cookie = {
        'prov':'a6f380fa-f8f0-7f6e-d854-38c41af03031',
        '__qca':'P0-1677417766-1551849099087',
        '_ga':'GA1.2.1470158957.1551849098',
        'notice-ctt':'4%3B1551880057341',
        '_gid':'GA1.2.890881421.1553787042',
    }
    """

    def start_requests(self):
        """
        构建请求链接
        """
        for i in range(1, self.settings.get('MAX_PAGES') + 1):
            params = {'sort': 'votes', 'page': i}
            url = self.base_url + urlencode(params)
            yield Request(url, callback=self.parse_quetion_list, errback=self.error_back)

    def parse_quetion_list(self, response):
        """
        获取每页的问题链接
        """
        for href in response.xpath('//*[@class="summary"]/h3/a/@href'):
            url = response.urljoin(href.extract())
            yield Request(url, callback=self.parse_question, errback=self.error_back, dont_filter=True)

    def parse_question(self, response):
        """
        获取问题详情页的数据
        """
        self.logger.debug('Already into Pipeline!')
        item = StackoverflowItem()
        item['link'] = response.url
        item['title'] = response.xpath('//*[@id="question-header"]/h1/a/text()').extract_first()
        item['votes'] = response.xpath('//*[@id="question"]/div/div[1]/div/div/text()').extract_first()
        item['body'] = response.css('.post-text').xpath('.//*[contains(@class, "prettyprint")]').extract()
        item['tags'] = response.css('.question .post-tag::text').extract()
        yield item

    def error_back(self, e):
        _ = self
        self.logger.debug('Error: {}'.format(e))
