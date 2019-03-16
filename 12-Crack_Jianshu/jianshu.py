#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Updated at 22:48 at March 16, 2019
@title: 模拟登录简书并识别点触验证码
@author: Northxw
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from PIL import Image
from io import BytesIO
from utils.chaojiying import Chaojiying_Client
from utils.config import *

class Crack_Jianshu(object):
    def __init__(self):
        """
        初始化
        """
        self.url = URL
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, TIME_OUT)
        # 简书登录账号、密码
        self.email = EMAIL
        self.password = PASSWORD
        # 创建超级鹰Client对象
        self.chaojiying = Chaojiying_Client(CHAIJIYING_USERNAME, CHAOJIYING_PASSWORD, CHAIJIYING_SOFT_ID)

    def __del__(self):
        """
        gc机制关闭浏览器
        """
        self.browser.close()

    def open(self):
        """
        打开简书网页版登录界面输入邮箱账号、密码
        :return: None
        """
        self.browser.get(self.url)
        # 邮箱
        email = self.wait.until(EC.presence_of_element_located((By.ID, 'session_email_or_mobile_number')))
        # 密码
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'session_password')))
        # 输入邮箱
        email.clear()
        email.send_keys(self.email)
        sleep(2)
        # 输入密码
        password.clear()
        password.send_keys(self.password)
        sleep(2)

    def get_submit_btn(self):
        """
        获取登录按钮
        :return: button
        """
        button = self.wait.until(EC.element_to_be_clickable((By.ID, 'sign-in-form-submit-btn')))
        return button

    def get_touclick_element(self):
        """
        获取验证码图片对象
        :return: 图片对象
        """
        element = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_item_img')))
        return element

    def get_code_position(self):
        """
        获取验证码位置
        :return: 验证码位置列表
        """
        element = self.get_touclick_element()
        sleep(3)
        # 相对位置
        location = element.location
        # 宽高度
        size = element.size
        # 坐标值
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size['width']
        # 验证码左上角和右下角坐标
        return [left, top, right, bottom]

    def get_screenshot(self):
        """
        获取网页截图
        :return: 截图对象
        """
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_touclick_image(self, name='captcha.png'):
        """
        获取验证码图片
        :return: 图片对象
        """
        left, top, right, bottom = self.get_code_position()
        print('验证码位置：', left, top, right, bottom)
        # 获取网页截图的Image对象
        screenshot = self.get_screenshot()
        # 获取验证码的Image对象
        jianshu_code = screenshot.crop((left, top, right, bottom))
        # 存储
        jianshu_code.save(name)
        return jianshu_code

    def get_points(self, captcha_result):
        """
        解析超级鹰识别结果
        :param captcha_result: 识别结果
        :return: 转化结果
        """
        # 获取pic_str的values
        groups = captcha_result.get('pic_str').split('|')
        # 将 字符串坐标值 转换为 整数型的坐标值
        locations = [[int(number) for number in group.split(',')] for group in groups]
        return locations

    def touch_click_words(self, locations):
        """
        点击验证图片
        :param locations: 点击位置
        :return: None
        """
        cnt = 1
        for location in locations:
            print('坐标点{}: {}'.format(cnt,location))
            ActionChains(self.browser).move_to_element_with_offset(self.get_touclick_element(),location[0], location[1]).click().perform()
            cnt = cnt + 1
            sleep(1)

    def get_verifi_button(self):
        """
        确认按钮
        :return: None
        """
        submit = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="geetest_commit_tip"]')))
        submit.click()

    def get_article_info(self):
        pass

    def connect_db(self):
        pass

    def save_to_db(self):
        pass


    def crack_login(self):
        """
        登录
        :return: None
        """
        # 打开简书登录界面
        self.open()
        # 点击登录按钮
        button = self.get_submit_btn()
        button.click()
        # 获取验证码图片
        image = self.get_touclick_image()
        bytes_array = BytesIO()
        # 存储为字节流格式
        image.save(bytes_array, format='PNG')
        # 识别验证码
        result = self.chaojiying.PostPic(bytes_array.getvalue(), CHAOJIYING_KIND)
        print("\n超级鹰识别结果：{}\n".format(result))
        locations = self.get_points(result)
        self.touch_click_words(locations)
        sleep(3)
        # 点击确认按钮
        self.get_verifi_button()

        # 通过获取"Logo"判断是否登录成功
        sleep(5)
        success = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'logo')))
        if success:
            print('\nSuccessful login!\n')

        # 失败重试
        if not success:
            print("-" * 50)
            self.crack_login()

if __name__ == '__main__':
    crack = Crack_Jianshu()
    crack.crack_login()