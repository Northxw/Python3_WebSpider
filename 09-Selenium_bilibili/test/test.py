# -*- coding:utf-8 -*-

"""
@record: 2018.11.5 23:14 测试鼠标悬停成功 | 2018.11.6 19:34 测试获取极验原图与缺口图成功
"""

from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

#测试站点：B站
URL = 'https://passport.bilibili.com/login'
browser = webdriver.Chrome()    # 声明浏览器
browser.get(URL)                # 访问网页
wait = WebDriverWait(browser, 10)   # 设置显式等待10秒

# 获取滑块节点
slider = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'gt_slider_knob')))
ActionChains(browser).move_to_element(slider).perform()

# 获取带有极验原图的网页截图
time.sleep(1)
screenshot_1 = browser.get_screenshot_as_png()
screenshot_1 = Image.open(BytesIO(screenshot_1))
screenshot_1.save('code.png')

# 点击
slider.click()
# 鼠标移动至其他位置
# other = browser.find_element_by_css_selector('.title-line .tit')
# ActionChains(browser).move_to_element(other).perform()
time.sleep(2)

# 获取带有极验缺口的网页截图
screenshot_2 = browser.get_screenshot_as_png()
screenshot_2 = Image.open(BytesIO(screenshot_2))
screenshot_2.save('code_.png')
time.sleep(2)

browser.close()     # 关闭浏览器
