# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
from pyquery import PyQuery as pq
import pymongo

browser = webdriver.Chrome()    # 创建浏览器对象
wait = WebDriverWait(browser, 10)   # 设置显示等待时间为10秒
KEYWORD = 'ipad'

MONGO_URL = 'localhost'
MONGO_DB = 'taobao'
MONGO_COLLECTION = 'products'
client = pymongo.MongoClient(host=MONGO_URL)
db = client[MONGO_DB]

MAX_PAGE = 100  # 最大页码数100

def index_page(page):
    """
    抓取索引页
    :param page: 页码
    :return: None
    """
    print("正在爬取第", page, "页")
    try:
        url = 'https://s.taobao.com/search?q='+quote(KEYWORD)   # 构造URL
        browser.get(url)    # 获取网页数据

        if page > 1:
            input = wait.until(     # 等待页码输入框加载完毕后，获取并赋值给input
                EC.presence_of_element_located((By.CSS_SELECTOR, '#mainarp-pager div.form > input')))
            submit = wait.until(    # 判断确定按钮，获取并赋值给submit
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#mainsrp-pager div.form")))
            input.clear()           # 清除掉默认文本
            input.send_keys(page)   # 发送下一页的页码
            submit.click()          # 模拟点击确定

        # 等待条件：text_to_be_present_in_element, 判断是否跳转到对应页码（根据页码高亮显示判断，将高亮的页码节点对应的CSS选择器和当前
        # 要跳转的页码通过参数传递给这个等待时间来判断）
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'), str(page)))

        # 等待条件：presence_of_element_located，如果10秒内商品信息加载出来，就执行get_products()函数提取商品信息.
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
        get_products()
    except TimeoutException:
        index_page(page)

def get_products():
    """
    提取商品数据
    :return: None
    """
    html = browser.page_source
    doc = pq(html)
    items = doc("#mainsrp-itemlist .items .item").items()   # 定位到商品列表的节点位置
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('data-src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text(),
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
        print(product)
        save_to_mongo(product)

def save_to_mongo(result):
    """
    保存至MongoDB
    :param result: 结果
    :return: None
    """
    try:
        if db[MONGO_COLLECTION].insert(result):
            print("存储到MongoDB成功")
    except Exception:
        print("存储到MongoDB失败")

def main():
    """
    遍历每一页
    :return:
    """
    for i in range(1, MAX_PAGE + 1):
        index_page(i)

if __name__ == '__main__':
    main()