# -*- coding:utf-8 -*-

from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from time import sleep
from config import *
import time

class DouYin(object):
    def __init__(self):
        """
        初始化
        """
        # 配置启动APP的参数
        self.desired_caps = {
            'platformName': PLATFORM,
            'deviceName': DEVICE_NAME,
            'appPackage': APP_PACKAGE,
            'appActivity': APP_ACTICITY
        }
        self.driver = webdriver.Remote(APPIUM_SERVER, self.desired_caps)
        self.wait = WebDriverWait(self.driver, TIME_OUT)

    def open(self):
        """
        打开抖音APP
        """
        time.sleep(5)
        # 跳过"滑动查看更多"界面
        unknown = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@class="android.widget.FrameLayout"]')))
        unknown.click()
        """
        try:
            # 出现抖音"用户隐私政策概要"界面后,选择"仅浏览"
            yes = self.wait.until(EC.element_to_be_clickable((By.ID, 'com.ss.android.ugc.aweme:id/mw')))
            yes.click()
        except NoSuchElementException as e:
            pass
        # 跳过"滑动查看更多"界面
        unknown = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="android.widget.FrameLayout"]')))
        unknown.click()
        """

    def scroll(self):
        """
        滑动
        """
        while True:
            # 上滑刷新
            self.driver.swipe(FLICK_START_X, FLICK_START_Y + FLICK_DISTANCE, FLICK_START_X, FLICK_START_Y)
            sleep(SCROLL_SLEEP_TIME)

    def main(self):
        self.open()
        self.scroll()

if __name__ == '__main__':
    douyin = DouYin()
    douyin.main()