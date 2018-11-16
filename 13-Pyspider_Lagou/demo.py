#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-11-16 11:48:05
# Project: Lagou

from pyspider.libs.base_handler import *
import time

class Handler(BaseHandler):
    crawl_config = {
        'headers': {
            'Host': 'www.lagou.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
        },
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://www.lagou.com/zhaopin/Python/', callback=self.index_page, validate_cert=False,
                   params={'labelWords': 'label'})

    @config(age=2 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('.position_link').items():
            self.crawl(each.attr.href, callback=self.detail_page, validate_cert=False)
            time.sleep(1)
        # 获取下一页链接
        next = response.doc('.item_con_pager a:last-child').attr.href
        self.crawl(next, callback=self.index_page, validate_cert=False)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "company": response.doc('.job-name > .company').text(),
            "job": response.doc('.job-name > .name').text(),
            "salary": response.doc('.salary').text(),
            "other": response.doc('.job_request span').text().split('/')[1:-1],
            "labels": response.doc('.job_request li').text(),
            "publish_time": "".join(response.doc('.publish_time').text().split()),
            "job_advantage": response.doc('.job-advantage > p').text(),
            "job_description": response.doc('.job_bt p').text(),
            "work_address": response.doc('.work_addr').text().replace('查看地图', '')
        }