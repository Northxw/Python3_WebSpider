# -*- coding: utf-8 -*-

from fake_useragent import UserAgent
import base64

class UAMiddleware(object):
    def __init__(self):
        self.user_agent = UserAgent().random

    def process_request(self, request, spider):
        request.headers['User-Agent'] = self.user_agent

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
            return response

    def process_exception(self, request, exception, spider):
        pass