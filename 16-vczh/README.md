# Project Name
&emsp; 爬取知乎轮子哥(vczh)的粉丝和关注者信息。

# Sort
&emsp; **Scrapy** - **Scrapy框架的应用**。

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
```
from fake_useragent import UserAgent

class UAMiddleware(object):
    def __init__(self):
        self.user_agent = UserAgent().random

    def process_request(self, request, spider):
        request.headers['User-Agent'] = self.user_agent
```

## 3. ProxyMiddleware
&emsp; 同理UA中间件，为防止反爬，设置代理( [阿布云](https://www.abuyun.com/) )。代码如下：
```
import base64

class ProxyMiddleware(object):
    def __init__(self, proxy_server, proxy_user, proxy_pass):
        self.proxy_server = proxy_server
        self.proxy_user = proxy_user
        self.proxy_pass = proxy_pass
        self.proxy_auth = "Basic " + base64.urlsafe_b64encode(bytes((self.proxy_user + ":" + self.proxy_pass), "ascii")).decode("utf8")

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
        # 统计状态码正常的请求总数量
        if response.status not in [500, 502, 503, 504, 522, 524, 408]:
            COUNT_SUCCESS_REQUEST['Request_Success'] = COUNT_SUCCESS_REQUEST['Request_Success'] + 1
        return response

    def process_exception(self, request, exception, spider):
        pass
```

## 4. DownloadRetryMiddleware
&emsp; 测试期间，发现图片的下载总量少于爬取总量，所以设置Retry中间件，在下载失败后，将图片的下载链接重新载入下载队列，最大程度保证数据的份额。代码继承RetryMiddleware, 仅作微小调动。如下：
```
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
```
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
            # 统计下载成功的图片总数量
            RESPONSE_STATUS['Download_Success'] = RESPONSE_STATUS['Download_Success'] + 1
        return item

    def get_media_requests(self, item, info):
        yield Request(item['avatar_url'])
```

#### 7.爬虫状态报告
&emsp; 由于未实现分布式，爬取时间较长，不可能守在屏幕前两个小时。所以实现了爬虫程序运行结束后，自动发送邮件报告爬虫状态（参考：[CSDN-Kosmoo](https://blog.csdn.net/zwq912318834/article/details/78014762?utm_source=blogxgwz5))。代码如下：
```
import smtplib
from email.mime.text import MIMEText

class EmailSender(object):
    def __init__(self):
        # 发送方smtp服务器
        self.smtp_host = 'smtp.163.com'
        # 发送方邮箱(同于登录smtp服务器)
        self.smtp_user = 'northxw@163.com'
        # 授权码
        self.smtp_authcode = 'XiYou0513'
        # smtp服务器默认端口465
        self.smtp_port = 465
        # 发送方邮箱
        self.sender = 'northxw@163.com'

    def sendEmail(self, recipient_list, email_subject, body):
        """
        发送邮件
        :param recipient_list: 收件人列表
        :param email_subject: 邮件主题
        :param body: 邮件内容
        :return: None
        """
        # 邮件内容、格式、编码
        message = MIMEText(_text=body, _subtype='plain', _charset='utf-8')
        # 发件人
        message['From'] = self.sender
        # 收件人
        message['To'] = ', '.join(recipient_list)
        # 主题
        message['Subject'] = email_subject
        try:
            # 实例化SMTP_SSL对象
            smtpSSLClient = smtplib.SMTP_SSL(self.smtp_host,self.smtp_port)
            # 登录
            loginResult = smtpSSLClient.login(self.smtp_user, self.smtp_authcode)
            # loginRes = (235, b'Authentication successful')
            print("Login Result：LoginRes = {}".format(loginResult))

            if loginResult and loginResult[0] == 235:
                print("Successful login, Code = {}".format(loginResult[0]))
                smtpSSLClient.sendmail(self.sender, recipient_list, message.as_string())
                print("Successful delivery. Message:{}".format(message.as_string()))
            else:
                print("Login failed, Code = {}".format(str(loginResult[0])))

        except Exception as e:
            print("Failed to send, Exception: e={}".format(e))
```

&emsp; 使用的发送邮箱是网易163邮箱。前提：你必须开启STMP服务，开启方法请自行搜索。爬虫状态报告邮件如图：
![email](https://github.com/Northxw/Python3_WebSpider/blob/master/16-vczh/vczh/utils/email.png)

#### 8. 其他问题
&emsp; 尝试运行代码过程中出现任何Bug，欢迎提交issue，或者通过邮箱(**northxw@163.com**)直接与我联系。

# Other
&emsp; 代码不足之处没有实现断点续传。后期更新吧。

# Demo
&emsp; **Downlaod Avatar**

![avatar](https://github.com/Northxw/Python3_WebSpider/blob/master/16-vczh/vczh/utils/followers.png)

&emsp; **DB Screenshot**

![db](https://github.com/Northxw/Python3_WebSpider/blob/master/16-vczh/vczh/utils/db_follower.png)
