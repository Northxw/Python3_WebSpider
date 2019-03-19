# -*- coding：utf-8 -*-

"""
Created at 22:00 on March 18,2019
@author: Northxw
@title: 模拟登录微信并获取朋友圈数据
@precautions: (1) 代码中所有节点都须提前通过 Appium新建Session获取(亲测同版本的微信中vivo_x7和Mi_8节点相同,其余机型未知)
              (2) 建议使用高性能手机测试(MI_8|MI_9等)
"""

from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from time import sleep
from config import *
from pymongo import MongoClient
from processor import Processor

class Moments(object):
    def __init__(self):
        """
        初始化
        """
        # 启动APP的参数配置
        self.desired_caps = {
            'platformName': PLANTFORM,
            'deviceName': DEVICE_NAME,
            'appPackage': APP_PACKAGE,
            'appActivity': APP_ACTIVITY,
        }
        self.driver = webdriver.Remote(DRIVER_SERVER, self.desired_caps)
        self.wait = WebDriverWait(self.driver, TIMEOUT)
        self.client = MongoClient(MONGO_URL)
        self.db = self.client[MONGO_DB]
        self.collection = self.db[MONGO_COLLECTION]
        # 处理日期
        self.processor = Processor()

    def login(self):
        """
        登录
        """
        # 点击登录
        login = self.wait.until(EC.element_to_be_clickable((By.ID, 'com.tencent.mm:id/e4g')))
        login.click()
        # 输入手机号
        phone = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/kh')))
        phone.set_text(USERNAME)
        # 点击下一步
        next = self.wait.until(EC.element_to_be_clickable((By.ID, 'com.tencent.mm:id/axt')))
        next.click()
        # 输入密码
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/kh')))
        password.set_text(PASSWORD)
        # 提交
        submit = self.wait.until(EC.element_to_be_clickable((By.ID, 'com.tencent.mm:id/axt')))
        submit.click()
        # 通讯录匹配提示(这里选"否",加快tab节点的加载速度)
        # yes = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/az_')))
        no = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/az9')))
        no.click()

    def enter(self):
        # 点击"发现"
        # global explore
        # explore = self.driver.find_element_by_android_uiautomator('new UiSelector().text("发现")')
        """
        try:
            explore = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/d7_')))
        except:
            self.driver.refresh()
            explore = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/b7b')))
        """
        explore = self.wait.until(EC.presence_of_element_located((
                                            By.XPATH, '//*[@class="android.widget.RelativeLayout"][3]')))
        # explore = self.wait.until(EC.presence_of_element_located((By.XPATH,'//android.widget.FrameLayout[@content-desc="当前所在页面,与的聊天"]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.View/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.RelativeLayout[3]')))
        explore.click()
        # 朋友圈
        # momnets = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/y6')))
        momnets = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/d7v')))
        momnets.click()

    def crawl(self):
        """
        无限拖动
        :return:
        """
        cnt = 0
        while True:
            # items存储当前页面所有发布的朋友圈信息
            items = self.wait.until(
                EC.presence_of_all_elements_located(
                    # 每个ej9节点对应一条朋友圈数据
                    (By.XPATH, '//*[@resource-id="com.tencent.mm:id/ej9"]/android.widget.LinearLayout')))
            # 上滑刷新朋友圈
            self.driver.swipe(FLICK_START_X, FLICK_START_Y + FLICK_DISTANCE, FLICK_START_X, FLICK_START_Y)

            for item in items:
                try:
                    # 昵称
                    nickname = item.find_element_by_id('com.tencent.mm:id/b5o').get_attribute('text')
                    # 正文
                    content = item.find_element_by_id('com.tencent.mm:id/ejc').get_attribute('text')
                    # 日期
                    date = item.find_element_by_id('com.tencent.mm:id/eec').get_attribute('text')
                    # 处理日期
                    date = self.processor.date(date)
                    data = {
                        'nickname': nickname,
                        'content': content,
                        'date': date,
                    }
                    print("昵称：", data['nickname'])
                    print("正文：", data['content'])
                    print("时间：", data['date'])
                    # 根据昵称和正文来查询信息,然后设置第三个参数为True.实现存在就更新,不存在就插入数据
                    self.collection.update({'nickname': nickname, 'content': content}, {'$set': data}, True)
                    sleep(SCROLL_SLEEP_TIME)
                except NoSuchElementException:
                    # print('Error')
                    pass

            # 循环加1
            cnt = cnt + 1
            if cnt == 200:
                break

    def main(self):
        """
        入口
        :return:
        """
        # 登录
        self.login()
        # 进入朋友圈
        self.enter()
        # 爬取
        self.crawl()

if __name__ == '__main__':
    moments_ = Moments()
    moments_.main()