# -*- coding: utf-8 -*-

# Scrapy settings for vczh project

import time

BOT_NAME = 'vczh'

SPIDER_MODULES = ['vczh.spiders']
NEWSPIDER_MODULE = 'vczh.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# 设置延时0.3秒
DOWNLOAD_DELAY = 0.3

#SPIDER_MIDDLEWARES = {
#    'vczh.middlewares.VczhSpiderMiddleware': 543,
#}

DOWNLOADER_MIDDLEWARES = {
    'vczh.middlewares.DownloadRetryMiddleware': 100,
    'vczh.middlewares.UAMiddleware': 543,
    'vczh.middlewares.ProxyMiddleware': 544,
}

ITEM_PIPELINES = {
    'vczh.pipelines.ImagePipeline': 300,
    # 'vczh.pipelines.MongoPipeline': 301,
    'vczh.pipelines.MysqlPipeline': 303,
}

# 爬取最大页码
MAX_PAGE = 155

# MYSQL SEETINGS
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = '0513'
MYSQL_DB = 'vczh'
MYSQL_PORT = 3306

# 代理服务器
PROXY_SERVER = "http://http-dyn.abuyun.com:9020"
# 代理服务器隧道验证信息
PROXY_USER = "HR827T805WJ4667D"
PROXY_PASS = "124D18494FF76D09"

# 图片存储位置
IMAGES_STORE = './images'

# LOG名称: 加入时间可以保证每次生成的报告不会重叠，也能清楚的知道报告生成时间
LOG_FILE = './logs/{}.log'.format(str(time.strftime("%Y-%m-%d %H_%M_%S")))
# LOG编码
# LOG_ENCODING = 'utf-8'
# LOG级别: DEBUG级别最低，如果设置DEBUG,所有的log都会记录，不利于查错
LOG_LEVEL = 'WARNING'

# 邮件发送者
MAIL_FROM = 'northxw@163.com'
# 邮件服务器
MAIL_HOST = 'smtp.163.com'
# 端口
MAIL_PORT = 25
# 发送者
MAIL_USER = 'northxw@163.com'
# 授权码
MAIL_PASS = 'authcode'

# 邮件接收者列表
RECEIVE_LIST = ['northxw@gmail.com', 'northxw@qq.com', 'northxw@sina.com']
# 邮件主题
SUBJECT = '爬虫状态报告'