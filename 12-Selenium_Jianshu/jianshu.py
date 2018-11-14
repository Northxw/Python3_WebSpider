# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from PIL import Image
from io import BytesIO
from chaojiying import Chaojiying
from Jianshu.utils.config import *

class Login_Jianshu(object):
    def __init__(self):
        """
        初始化
        """
        self.url = URL
        self.driver = webdriver.Chrome()            # 声明浏览器对象
        self.wait = WebDriverWait(self.driver, 5)   # 设置显式等待5秒
        self.user_phone = USER_PHONENUMBER          # 简书账号
        self.password = PASSWORD                    # 密码
        self.chaojiying = Chaojiying(CHAIJIYING_USERNAME, CHAOJIYING_PASSWORD, CHAIJIYING_SOFT_ID)  # 创建超级鹰对象

    def __del__(self):
        self.driver.close()

    def open(self):
        """
        打开简书网页版登录界面输入账号和密码
        :return: None
        """
        self.driver.get(URL)
        account = self.wait.until(EC.presence_of_element_located((By.ID, 'session_email_or_mobile_number')))
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'session_password')))
        account.send_keys(self.user_phone)
        sleep(3)
        password.send_keys(self.password)

    def get_submit_button(self):
        """
        获取登录按钮
        :return: 登录按钮
        """
        button = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'sign-in-button')))
        return button

    def get_screenshot(self):
        """
        获取网页截图
        :return: 截图对象
        """
        screenshot = self.driver.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_verifi_element(self):
        """
        获取验证码
        :return: 验证码节点
        """
        element = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_item_img')))
        return element

    def get_position(self):
        """
        获取验证码位置
        :return: 验证码位置列表
        """
        element = self.get_verifi_element()
        sleep(2)
        location = element.location
        size = element.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
            'width']
        return [left, top, right, bottom]  # 返回验证图片的两个坐标值

    def get_verifi_image(self, name='verifi.png'):
        """
        获取验证码图片
        :return: 图片对象
        """
        left, top, right, bottom = self.get_position()
        print('验证码位置：', left, top, right, bottom)
        screenshot = self.get_screenshot()                  # 获取网页截图的Image对象
        jianshu_code = screenshot.crop((left, top, right, bottom))   # 裁剪验证码
        jianshu_code.save(name)  # 存储照片
        return jianshu_code

    def get_points(self, verified_result):
        """
        获取超级鹰的识别结果
        :param verified_result: 识别结果
        :return: 转化后的结果
        """
        # 获取结果
        groups = verified_result.get('pic_str').split('|')
        # 将字符串转化为整形
        locations = [[int(number) for number in group.split(',')] for group in groups]
        return locations

    def touch_click(self, locations):
        """
        点击点触式验证码
        :param locations: 点击位置
        :return: None
        """
        for location in locations:
            print(location)
            ActionChains(self.driver).move_to_element_with_offset(self.get_verifi_element(), location[0],
                                                                   location[1]).click().perform()
            sleep(1)

    def verifi_button(self):
        """
        确认按钮
        :return: None
        """
        submit = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_commit_tip')))
        submit.click()

    def crack(self):
        """
        破解
        """
        # 打开简书登录界面
        self.open()
        # 点击登录按钮
        button = self.get_submit_button()
        button.click()
        # 获取验证码图片
        image = self.get_verifi_image()
        bytes_array = BytesIO()
        image.save(bytes_array, format='PNG')
        # 识别验证码
        result = self.chaojiying.PostPic(bytes_array.getvalue(), CHAOJIYING_KIND)
        print("超级鹰识别结果：", result)
        locations = self.get_points(result)
        self.touch_click(locations)
        sleep(3)
        # 点击确认按钮
        self.verifi_button()

        # 通过获取"用户头像节点"判断是否登录成功
        sleep(8)
        success = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'avatar')))
        print('已获取到头像节点!')

        # 失败重试
        if not success:
            print("-" * 50)
            self.crack()
        else:
            print('登录成功!')
            sleep(5)

if __name__ == '__main__':
    crack_jianshu = Login_Jianshu()
    crack_jianshu.crack()