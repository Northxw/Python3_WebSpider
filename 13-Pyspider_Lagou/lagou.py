#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-11-16 11:48:05
# Project: Lagou

from pyspider.libs.base_handler import *
from pymongo import MongoClient
import time


class Mongo(object):
    def __init__(self):
        # 初始化数据库
        self.client = MongoClient()
        self.db = self.client['lagou']
        self.collection = self.db['python']

    def insert(self, data):
        # 将字典数据插入到数据库
        if data:
            self.collection.insert(data)

    def __del__(self):
        # 关闭数据库连接
        self.client.close()


class Agent_abuyun(object):
    def __init__(self):
        self.proxyHost = "proxy.abuyun.com"
        self.proxyPort = "9010"
        self.proxyUser = "H72RXH024162Y0VD"
        self.proxyPass = "E8A5838333933FFE"

    def ip_port(self):
        # 代理隧道验证信息
        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": self.proxyHost,
            "port": self.proxyPort,
            "user": self.proxyUser,
            "pass": self.proxyPass,
        }
        proxies = {
            "http": proxyMeta,
            "https": proxyMeta,
        }
        return proxies


class Handler(BaseHandler):
    crawl_config = {
        'headers': {
            'Host': 'www.lagou.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
        },
        'proxy': Agent_abuyun().ip_port(),
        'mongo': Mongo(),
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://www.lagou.com/zhaopin/Python/', callback=self.index_page, validate_cert=False,
                   params={'labelWords': 'label'})

    # 设置任务有效期为两个小时(因为一般为30个页面左右)
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

    def on_result(self, data):
        self.crawl_config['mongo'].insert(data)