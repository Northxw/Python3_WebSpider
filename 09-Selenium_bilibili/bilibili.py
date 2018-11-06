# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from time import sleep
from PIL import Image
from io import BytesIO

EMAIL = 'northxw@163.com'
PASSWORD = 'wxf201678...'

BORDER = 10
INIT_LEFT = 51

class CrackGeetest_b(object):
    def __init__(self):
        """
        初始化信息
        """
        self.url = 'https://passport.bilibili.com/login'    # 目标站点
        self.browser = webdriver.Chrome()                   # 声明Chrome浏览器
        self.wait = WebDriverWait(self.browser, 10)         # 设置显式等待10秒，等待节点元素加载完成.
        self.email = EMAIL          # 邮箱
        self.password = PASSWORD    # 密码

    def __del__(self):
        self.browser.close()        # 关闭浏览器,gc垃圾回收机制回收

    def open(self):
        """
        打开B站登录界面输入邮箱和密码
        :return:
        """
        self.browser.get(self.url)      # 访问B站登录界面
        email = self.wait.until(EC.presence_of_element_located((By.ID, 'login-username')))      # 获取邮箱输入框节点
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'login-passwd')))     # 获取密码输入框节点
        email.send_keys(self.email)         # 输入邮箱账号
        sleep(3)
        password.send_keys(self.password)   # 输入密码

    def get_screenshot(self, name='web_screenshot.png'):
        """
        获取网页截图
        :return: 截图对象
        """
        print('正在获取全局截屏...')
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        screenshot.save(name)
        return screenshot

    def ge_slider(self):
        """
        获取滑动验证按钮
        :return: 按钮对象
        """
        # 注意：获取滑动按钮后，验证完成，会自动跳转，不需要点击登录按钮。
        slider = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'gt_slider_knob')))
        return slider

    def get_position(self):
        """
        获取验证码位置（未出现缺口的验证码）
        :return: 验证码位置坐标值
        """
        # B站极验验证原图由多切块组成
        img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'gt_box')))
        sleep(1)
        location = img.location     # 获取极验图片在网页中的位置
        size = img.size             # 获取极验图片的大小
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size['width']
        return [left, top, right, bottom]   # 返回验证图片的两个坐标值

    def get_geetest_image(self, name='captcha.png', name_='web_screenshot.png'):
        """
        获取验证码图片
        :return: 图片对象
        """
        left, top, right, bottom = self.get_position()  # 获取坐标值
        print('验证码位置：', left, top, right, bottom)
        screenshot = self.get_screenshot(name_)      # 获取网页截图的Image对象
        captcha = screenshot.crop((left, top, right, bottom))   # 裁剪极验原图
        # captcha = self.image_convert(captcha)           # 二值化验证码对象
        captcha.save(name)  # 存储照片
        return captcha

    def image_convert(self, image):
        """
        将验证码图像二值化,提高识别精度
        :param image: 验证码的Image对象
        :return: 返回二值化image对象
        """
        image = image.convert("L")  # 灰度处理
        threshold = 127  # 设置阈值为127
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        image = image.point(table, '1')
        return image

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
        threshold = 60      # 设置阈值60
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
            pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False

    def get_gap(self, image1, image2):
        """
        获取缺口偏移量
        :param image1: 极验原图
        :param image2: 缺口图片
        :return:
        """
        left = 60
        for i in range(left, image1.size[0]):   # 遍历两张图片的每个像素
            for j in range(image1.size[1]):
                if not self.is_pixel_equal(image1, image2, i, j):   # 判断同一位置的像素是否相同
                    left = i
                    return left
        return left

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
        :return:
        """
        ActionChains(self.browser).click_and_hold(slider).perform()     # 按住鼠标准备拖动
        for x in tracks:
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()   # 拖动滑块
        sleep(0.5)
        ActionChains(self.browser).release().perform()      # 释放滑块

    def crack_login(self):
        """
        登录
        """
        # 打开B站登录界面,输入用户名密码
        self.open()
        # 鼠标悬停滑块验证按钮位置(自动显示极验原图)
        slider = self.ge_slider()
        ActionChains(self.browser).move_to_element(slider).perform()    # 鼠标悬停
        # 获取验证码图片
        image1 = self.get_geetest_image('captcha1.png', './screenshot/带有极验原图的网页截图.png')     # 获取极验原图
        # 点按呼出缺口
        slider.click()
        sleep(2)
        # 获取带缺口的验证码图片
        image2 = self.get_geetest_image('captcha2.png', './screenshot/带有极验缺口的网页原图.png')     # 获取缺口图片
        # 获取缺口位置
        gap = self.get_gap(image1, image2)
        print('缺口位置', gap)
        # 减去缺口位移
        gap -= BORDER
        # 获取移动轨迹
        track = self.get_track(gap)
        print('滑动轨迹', track)
        # 拖动滑块
        self.move_to_gap(slider, track)
        sleep(5)   # 延迟10秒,等待登录成功后的主页节点完全加载

        # 获取页面登录之后菜单栏的"主页"节点.
        success = ''
        try:
            success = self.wait.until(
                EC.text_to_be_present_in_element((By.CLASS_NAME, 'bili-icon'), '验证成功'))
        except Exception as e:
            _ = e   # 接收异常
        else:
            print(success)

        # 失败后重试
        if not success:
            print("-"*50)
            self.crack_login()
            print('登录成功!')

if __name__ == '__main__':
    crack = CrackGeetest_b()
    crack.crack_login()

