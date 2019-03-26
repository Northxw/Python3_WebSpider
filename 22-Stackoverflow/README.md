# Spider Stackoverflow
&emsp; 爬取 **Stackoverflow** 前1000的问题。

# Sort
&emsp; **Scrapy** - 爬取外网数据。

# Explain
## 1. 设置 "ROBOTSTXT_OBEY = True"
&emsp; 如果你没有某墙软件，建议遵循爬虫协议，否则可能会被强制切断请求。在此基础上，设置 **DOWNLOAD_DELAY** 爬取时间间隔, 访问不要过于频繁。

## 2. 建议设置"佛跳墙"
&emsp; 经测，设置代理(某墙)后，可以在不设爬取时延的情况下，更快更高效的获取数据。如果直接用的客户端软件，在requests长时间没有响应后切换节点便可继续获取数据。

## 3. UAMiddleware、ProxyMiddleware
&emsp; 在前两点的基础上，添加随机UA中间件以及代理中间件(由于本机有佛跳墙的客户端软件，所以没有开启代理中间件)。
```Python
from fake_useragent import UserAgent

class UAMiddleware(object):
    def __init__(self):
        self.user_agent = UserAgent().random

    def process_request(self, request, spider):
        request.headers['User-Agent'] = self.user_agent
```

## 4.爬取思路
- **start_requests()** 初始化前100页链接
- 爬取每页问题的详情页链接
- 爬取问题详情页的标题、投票数、正文、标签等信息
- 管道清洗校验后存入MonogoDB

&emsp; 注意：Reqeust过程产生的所有异常，都由error_back()函数接收并打印在控制台打印错误信息；爬取问题详情页由于部分问题没有code，所以返回None。数据库
管道如下：
```Python
import pymongo

class MongoPipeline(object):
    def __init__(self, mongo_url, mongo_db):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_url=crawler.settings.get('MONGO_INIT_URL'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        self.db[item.table].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()
```

# Other
&emsp; ？？？

# Result

![db](https://github.com/Northxw/Python3_WebSpider/tree/master/22-Stackoverflow/stackoverflow/utils/db.png)
