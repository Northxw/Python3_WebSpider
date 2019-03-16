# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from utils.config import *
from time import sleep
from PIL import Image
from io import BytesIO

class Crack_bb(object):
    def __init__(self):
        """
        初始化
        """
        self.url = URL
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 15)
        # 邮箱、密码
        self.email = EMAIL
        self.password = PASSWORD

    def __del__(self):
        """
        gc机制关闭浏览器
        """
        self.browser.close()

    def open(self):
        """
        打开B站登录界面输入邮箱和密码
        :return: None
        """
        # 访问B站登录界面
        self.browser.get(self.url)
        # 邮箱
        username = self.wait.until(EC.presence_of_element_located((By.ID, 'login-username')))
        # 密码
        passwd = self.wait.until(EC.presence_of_element_located((By.ID, 'login-passwd')))
        # 输入账号
        username.clear()
        username.send_keys(self.email)
        sleep(3)
        # 输入密码
        passwd.clear()
        passwd.send_keys(self.password)
        sleep(3)

    def get_slider(self):
        """
        获取滑块
        :return: 滑块对象
        """
        slider = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@class,"gt_slider_knob")]')))
        return slider

    def get_code_position(self):
        """
        获取验证码位置
        :return: 验证码位置列表
        """
        # B站滑动验证码原图由多个切片组成
        img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'gt_box')))
        sleep(1)
        # 获取验证码在网页中的相对位置
        location = img.location
        # 获取节点宽高
        size = img.size
        # img坐标值
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size['width']
        # 验证码左上角和右下角坐标
        return [left, top, right, bottom]

    def get_geetest_image(self, name='demo.png'):
        """
        获取验证码图片
        :return: 图片对象
        """
        # 获取坐标值
        left, top, right, bottom = self.get_code_position()
        print('验证码位置：({}, {}), ({}, {})'.format(left, top, right, bottom))
        # 获取网页截图
        screenshot = self.get_screenshot()
        # 裁剪验证码图片
        captcha = screenshot.crop((left, top, right, bottom))
        # 存储
        captcha.save(name)
        return captcha

    def get_screenshot(self):
        """
        获取网页截图
        :return: 截图对象
        """
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_gap(self, image1, image2):
        """
        获取缺口偏移量
        :param image1: 不带缺口的图片
        :param image2: 带缺口的图片
        :return: None
        """
        left = 60
        # 遍历两张图片的每个像素并判断同一位置像素是否相同,不相同的像素点即缺口位置
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                if not self.is_pixel_equal(image1, image2, i, j):
                    left = i
                    return left
        return left

    def is_pixel_equal(self, image1, image2, x, y):
        """
        判断像素是否相同
        :param image1: 极验原图
        :param image2: 缺口图片
        :param x: 位置X
        :param y: 位置Y
        :return: 像素是否相同
        """
        # 取两个图片的像素点
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        # 阈值60
        threshold = 60
        # 比较RGB的绝对值是否小于阈值60,如果在阈值内则相同,反之不同
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False

    def get_track(self, distance):
        """
        根据偏移量获取移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.2
        # 初速度
        v = 0

        while current < distance:
            if current < mid:
                # 加速度为正2
                a = 2
            else:
                # 加速度为负3
                a = -3
            # 初速度v0
            v0 = v
            # 当前速度v = v0 + at
            v = v0 + a * t
            # 移动距离x = v0t + 1/2 * a * t^2
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))
        return track

    def move_to_gap(self, slider, tracks):
        """
        拖动滑块到缺口位置
        :param slider: 滑块
        :param tracks: 轨迹
        :return: None
        """
        # 按住鼠标准备拖动
        ActionChains(self.browser).click_and_hold(slider).perform()
        # 拖动滑块
        for x in tracks:
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
        sleep(0.5)
        # 释放滑块
        ActionChains(self.browser).release().perform()

    def crack_login(self):
        """
        登录
        :return: None
        """
        # 打开B站登录界面,输入用户名密码
        self.open()
        # 鼠标悬停滑块(自动显示极验原图)
        slider = self.get_slider()
        ActionChains(self.browser).move_to_element(slider).perform()
        # 获取不带缺口的验证码图片
        image1 = self.get_geetest_image('captcha1.png')
        # 点按呼出缺口
        slider.click()
        sleep(2)
        # 获取带缺口的验证码图片
        image2 = self.get_geetest_image('captcha2.png')
        # 获取缺口位置
        gap = self.get_gap(image1, image2)
        print('缺口位置：', gap)
        # 减去缺口位移
        gap -= BORDER
        # 获取移动轨迹
        track = self.get_track(gap)
        print('滑动轨迹：', track)
        # 拖动滑块
        self.move_to_gap(slider, track)
        # 延迟5秒,等待登录成功后的主页节点完全加载
        sleep(5)

        success = self.wait.until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, 't'), '验证成功'))
        print(success)

        # 失败后重试
        if not success:
            self.crack_login()

if __name__ == '__main__':
    crack = Crack_bb()
    crack.crack_login()