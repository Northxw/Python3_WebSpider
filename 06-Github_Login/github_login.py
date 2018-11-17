# -*- coding:utf-8 -*-

import requests
from lxml import etree

class Login(object):
    def __init__(self):
        self.headers = {
            'Host': 'github.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'Referer': 'https://github.com'
        }
        self.login_url = 'https://github.com/login'
        self.post_url = 'https://github.com/session'
        self.logined_url = 'https://github.com/settings/profile'
        self.session = requests.Session()   # 维持会话，处理Cookies, 使得我们不同担心Cookies的问题

    def token(self):
        response = self.session.get(self.login_url, headers=self.headers)
        selector = etree.HTML(response.text)
        token = selector.xpath('//*[@id="login"]/form/input[2]/@value')     # 获取authenticity_token的值
        return token


    def login(self, email, password):
        post_data = {
            'commit': 'Sign in',
            'utf8': '✓',                            # ✓ 可在"xpath('//*[@id="login"]/form/input[1]/@value')" 位置复制粘贴
            'authenticity_token': self.token(),     # 获取隐藏在源码中的authenticity_token值.
            'login': email,
            'password': password
        }
        response = self.session.post(self.post_url, data=post_data, headers=self.headers)
        if response.status_code == 200:
            self.dynamics(response.text)

        response = self.session.get(self.logined_url, headers=self.headers)
        if response.status_code == 200:
            self.profile(response.text)

    def dynamics(self, html):
        selector = etree.HTML(html)
        dynamics = selector.xpath('//div[contains(@class, "news")]/div')  # 获取动态信息的div标签(需要处理)
        print(len(dynamics))
        div_class_values = ['watch_started', 'fork', 'follow', 'repo']      # 所有动态信息的class属性值
        for item in dynamics:
            value = item.xpath('./@class')      # 获取标签的class属性值, 如果没在列表, 则不做处理
            print(value)
            if value in div_class_values:
                text = item.xpath('.//div[contains(@class, "flex-items-baseline")]//text()').strip()
                print(text)

    def profile(self, html):
        selector = etree.HTML(html)
        name = selector.xpath('//input[@id="user_profile_name"]/@value')    # 获取用户名称
        email = selector.xpath('//select[@id="user_profile_email"]/option[@value!=""]/text()')
        print(name, email)

if __name__ == "__main__":
    login = Login()
    login.login(email="northxw@163.com", password='your_password')
