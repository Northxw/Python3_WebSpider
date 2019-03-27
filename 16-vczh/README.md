# Spider Vczh
&emsp; 爬取知乎轮子哥(vczh)的粉丝和关注者信息。

# Sort
&emsp; **Scrapy** - **使用Scrapy的功能模块**。

# Install
**1.Scrapy** - 需提前安装依赖库( **lxml, pyOpenSSL, Twisted, pyWin32** )。
```
pip3 install Scrapy
```

**2.pymysql**
```
pip3 install pymysql
```

# Process analysis
## 1. 粉丝数据量
&emsp; 由于轮子哥的粉丝数量接近80万，所以仅爬取前10万的数据并下载用户头像。经测试，耗时2个小时左右。

## 2. UAMiddleware
&emsp; 本次获取的数据量较大，在优先爬取效率情况下，设置随机UA信息，防止反爬。代码如下：
```Python
from fake_useragent import UserAgent

class UAMiddleware(object):
    def __init__(self):
        self.user_agent = UserAgent().random

    def process_request(self, request, spider):
        request.headers['User-Agent'] = self.user_agent
```

## 3. ProxyMiddleware
&emsp; 同理UA中间件，为防止反爬，设置代理( [阿布云](https://www.abuyun.com/) )。代码如下：
```Python
import base64

class ProxyMiddleware(object):
    def __init__(self, proxy_server, proxy_user, proxy_pass):
        self.proxy_server = proxy_server
        self.proxy_user = proxy_user
        self.proxy_pass = proxy_pass
        self.proxy_auth = "Basic " + base64.urlsafe_b64encode(bytes((self.proxy_user + ":" + self.proxy_pass), "ascii")).decode("utf8")
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            proxy_server = crawler.settings.get('PROXY_SERVER'),
            proxy_user = crawler.settings.get('PROXY_USER'),
            proxy_pass = crawler.settings.get('PROXY_PASS')
        )

    def process_request(self, request, spider):
        request.meta["proxy"] = self.proxy_server
        request.headers["Proxy-Authorization"] = self.proxy_auth

    def process_response(self, request, response, spider):
        try:
            spider.crawler.stats.inc_value('normal_response')
        except Exception as e:
            self.logger.error('Response Error: {}'.format(e.args))
        return response

    def process_exception(self, request, exception, spider):
        pass
```

## 4. DownloadRetryMiddleware
&emsp; 测试期间，发现图片的下载总量少于爬取总量，所以设置Retry中间件，在下载失败后，将图片的下载链接重新载入下载队列，最大程度保证数据的份额。代码继承RetryMiddleware, 仅作微小调动。如下：
```Python
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message

class DownloadRetryMiddleware(RetryMiddleware):
    def process_response(self, request, response, spider):
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) \
                and not request.meta.get('dont_retry', False):
            return self._retry(request, exception, spider)
```

## 5.MysqlPipeline
&emsp; 数据库管道，主要是数据的清洗校验等。将爬取的粉丝信息全部存储至Mysql(代码请查看: [pipeline.py](https://github.com/Northxw/Python3_WebSpider/blob/master/16-vczh/vczh/pipelines.py))。


## 6. ImagePipeline
&emsp; 图片下载管道，继承ImagesPipeline。修改了提取图片下载链接的方式，设置存储位置，代码如下：
```Python
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline

class ImagePipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None):
        url = request.url
        file_name = url.split('/')[-1]
        return file_name

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('Image Downloaded Failed')
        else:
            COUNT_IMAGES_NUMS['IMAGES_NUMS'] += 1
            return item

    def get_media_requests(self, item, info):
        yield Request(item['avatar_url'])
```


## 7. LOG日志
&emsp; 一般情况下，我们会调用scrapy内置logger打印日志到控制台，可是你真的能找到log吗？      

![huaji]()

&emsp; 你可能不知道Python的logging模块提供了丰富的方法让我们打印log。接下来就将错误信息打印到log文件吧。但前提是你必须在settings.py中做一些设置。
```Python
LOG_FILE = './logs/{}.log'.format(str(time.strftime("%Y-%m-%d %H_%M_%S")))
LOG_LEVEL = 'WARNING'
```
&emsp; **LOG_FILE** 是日志名称，在文件名中加入当前时间可以保证每次生成的log日志不重叠。**LOG_LEVEL** 是错误级别，这里设置为"WARNING", 方便查看日志信息。更多的用法可以查看官方文档。     

![log]()


## 8.爬虫状态报告
&emsp; 由于未实现分布式，爬取时间较长，不可能守在屏幕前两个小时。还好Scrapy内置了邮件模块，需要在settings.py中做一些参数设置，就可以使用。如下：
```Python
# 邮件发送者
MAIL_FROM = 'northxw@163.com'
# 邮件服务器
MAIL_HOST = 'smtp.163.com'
# 端口
MAIL_PORT = 25
# 发送者
MAIL_USER = 'northxw@163.com'
# 授权码(需要在邮箱开启SMTP服务并生成授权码)
MAIL_PASS = 'authcode'
```
&emsp; 接下来在Spider中重写 **closed()** ，爬虫程序结束后，便会自动发送邮件到你指定的邮箱。
```Python
def closed(self, reason):
    # 爬虫完成时间
    fnished = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    # 创建邮件发送对象
    mail = MailSender.from_settings(self.settings)
    # 邮件内容
    body = "爬虫名称: {}\n\n 开始时间: {}\n\n 请求成功总量：{}\n 图片下载总量：{}\n 数据库存储总量：{}\n\n 结束时间  : {}\n".format(
        '知乎轮子哥粉丝爬虫',
        str(self.start),
        str(self.crawler.stats.get_value("normal_response")),
        str(COUNT_IMAGES_NUMS['IMAGES_NUMS']),
        str(self.crawler.stats.get_value("success_insertdb")),
        str(str(fnished)))
    # 发送邮件
    mail.send(to=self.settings.get('RECEIVE_LIST'), subject=self.settings.get('SUBJECT'), body=body)
```

&emsp; 使用的发送邮箱是网易163邮箱。前提：你必须开启STMP服务，开启方法请自行搜索。爬虫状态报告邮件如图：

![email](https://github.com/Northxw/Python3_WebSpider/blob/master/16-vczh/vczh/utils/email.png)

## 9. Crawl API
&emsp; Scrapy提供了方便的收集数据的机制。数据以key/value方式存储，值大多是计数值。 该机制叫做数据收集器(Stats Collector)，可以通过 Crawler API 的属性 stats 来使用。[摘自百度]， 用法也超级简单。

&emsp; 在Middleware、Pipeline中：
```Python
spider.crawler.stats.inc_value('normal_response')
```

&emsp; 在spider中：
```Python
self.crawler.stats.get_value("normal_response")
```
&emsp; **inc_value('normal_response')** 用来设置一个名称为normal_response的key，并对value自增1。**get_value("normal_response")** 获取key为normal_response的值。如此，我们可以很方便的计算数据库存储总量或请求成功总量。

## 10. 其他问题
&emsp; 尝试运行代码过程中出现任何Bug，欢迎提交issue，或者通过邮箱(**northxw@163.com**)直接与我联系。

# Other
&emsp; 代码不足之处没有实现断点续传。后期更新吧。

# Demo
&emsp; **Downlaod Avatar**

![avatar](https://github.com/Northxw/Python3_WebSpider/blob/master/16-vczh/vczh/utils/followers.png)

&emsp; **DB Screenshot**

![db](https://github.com/Northxw/Python3_WebSpider/blob/master/16-vczh/vczh/utils/db_follower.png)
