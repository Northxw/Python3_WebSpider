# -*- coding:utf-8 -*-

from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from .utils.config import *

class JianshuAction(object):
    def __init__(self):
        """
        初始化信息
        """
        # 驱动配置
        self.desired_caps = {
            "platformName": PLATFORM,
            "deviceName": DEVICE_NAME,
            "appPackage": APP_PACKAGE,
            "appActivity": APP_ACTIVITY
        }
        self.driver = webdriver.Remote(DRIVER_SERVER, self.desired_caps)
        self.wait = WebDriverWait(self.driver, TIMEOUT)

    def login(self):
        """
        登录
        :return: None
        """
        # 点击"我的"进入登录界面
        tab_login = self.wait.until(EC.presence_of_element_located((By.ID, 'com.jianshu.haruki:id/tab_more')))
        tab_login.click()
        sleep(3)
        # 点击"头像"登录简书
        image_login = self.wait.until(EC.presence_of_element_located((By.ID, 'com.jianshu.haruki:id/user_top_info_avatar')))
        image_login.click()
        sleep(3)

        # 用户
        # account = self.wait.until(EC.presence_of_element_located((By.ID, 'com.jianshu.haruki:id/et_account')))
        # account.send_keys(USER_PHONENUMBER)
        # 密码
        # password = self.wait.until(EC.presence_of_element_located((By.ID, 'com.jianshu.haruki:id/et_password')))
        # password.send_keys(PASSWORD)

        # 选择"微信登录"省略输入账号密码的步骤
        weixin_login = self.wait.until(EC.presence_of_element_located((By.ID, 'com.jianshu.haruki:id/iv_wechat')))
        weixin_login.click()
        sleep(10)

        # 解释：因为之前已经微信授权,所以这里直接登录进入个人页面

        # 点击"发现"进入文章推荐页面
        discorver = self.wait.until(EC.presence_of_element_located((By.ID, 'com.jianshu.haruki:id/tab_discover')))
        discorver.click()
        sleep(3)

    def scroll(self):
        """
        上滑页面、触发请求
        :return:None
        """
        # 由于推荐页面的文章数目很多,当获取到1000条文章的具体信息之后，程序终止。
        count = 100
        while count > 0:
            # 模拟拖动
            self.driver.swipe(FLICK_START_X, FLICK_START_Y + FLICK_DISTANCE, FLICK_START_X, FLICK_START_Y)
            sleep(SCROLL_SLEEP_TIME)
            count = count - 1

    def main(self):
        """
        主函数
        :return:
        """
        self.login()
        self.scroll()

if __name__ == '__main__':
    action = JianshuAction()
    action.main()