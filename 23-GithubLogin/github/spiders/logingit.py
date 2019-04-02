# -*- coding: utf-8 -*-
import scrapy
import requests

class LogingitSpider(scrapy.Spider):
    name = 'logingit'
    allowed_domains = ['github.com']
    # 登陆界面的URL
    login_url = 'https://github.com/login'
    # POST表单数据的URL
    post_url = 'https://github.com/session'
    # 登陆后URL
    logined_url = 'https://github.com/settings/profile'

    def start_requests(self):
        """
        获取登陆页面源码
        """
        return [scrapy.Request(url=self.login_url,
                              callback=self.login,
                              headers=self.settings.get('DEFAULT_REQUEST_HEADERS'))]

    def login(self, response):
        """
        使用FromRequest模拟登陆Github
        """
        # 提取POST验证参数 authenticity_token
        authcode = response.xpath('//*[@id="login"]/form/input[2]/@value').extract_first()
        if authcode:
            self.logger.debug("Auth Token: %s" %authcode)
            post_data = {
                'commit': 'Sign in',
                'utf8': '✓',
                'authenticity_token': authcode,
                'login': self.settings.get('ACCOUNT'),
                'password': self.settings.get('PASSWORD')
            }
            return [scrapy.FormRequest(url=self.post_url,
                                      formdata=post_data,
                                      headers=self.settings.get('DEFAULT_REQUEST_HEADERS'),
                                      callback=self.check)]
        else:
            return [scrapy.Request(url=self.login_url, callback=self.login)]

    def check(self, response):
        """
        验证登陆是否成功
        """
        avatar = response.css('#user-links > li:nth-child(3) > details > summary > img::attr(src)').extract_first()
        if avatar:
            content = requests.get(url=avatar.split('?')[0]).content
            with open('./utils/acatar.jpg', 'wb') as f:
                f.write(content)
            print('Successfully Login!')
        pass


    def parse(self, response):
        pass