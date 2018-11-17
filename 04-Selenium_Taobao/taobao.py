# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from urllib.parse import quote
from pyquery import PyQuery as pq
import pymongo
import time
from Taobao.utils.config import *
from xdaili import Xdaili

class Products(object):
    def __init__(self):
        """
        初始化
        """
        # 数据库配置
        self.client = pymongo.MongoClient(MONGO_URL)
        self.db = self.client[MONGO_DB]
        self.collection = self.db[MONGO_COLLECTION]
        # 代理配置
        self.auth = Xdaili().auth()
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--start-maximized')
        self.plugin_file = './utils/proxy_auth_plugin.zip'
        self.chrome_options.add_extension(self.plugin_file)
        self.browser = webdriver.Chrome(chrome_options=self.chrome_options)
        self.wait = WebDriverWait(self.browser, TIMEOUT)

    def index_page(self, page):
        """
        抓取索引页
        :param page: 页码
        :return:
        """
        print('正在爬取第', page, '页')
        try:
            url = 'https://s.taobao.com/search?q=' + quote(KEYWORD)
            self.browser.get(url)
            if page > 1:
                input = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input')))
                submit = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_Submit')))
                input.clear()
                input.send_keys(page)
                submit.click()
                self.wait.until(
                            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'), str(page)))
                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
                self.get_products()
        except TimeoutException:
            self.index_page(page)

    def get_products(self):
        """
        提取商品数据
        """
        # 获取网页源码
        html = self.browser.page_source
        doc = pq(html)
        # 获取包含商品信息的所有div标签
        items = doc('#mainsrp-itemlist .items .item').items()
        for item in items:
            product = {
                'image': item.find('.pic .img').attr('src'),
                'price': item.find('.price').text(),
                'deal': item.find('.deal-cnt').text()[:-3],
                'title': item.find('.title').text(),
                'shop': item.find('.shop').text(),
                'location': item.find('.location').text()
            }
            print(product)
            self.save_to_mongo(product)

    def save_to_mongo(self, result):
        """
        存储至数据库
        :param result: 抓取的数据
        :return: None
        """
        try:
            if self.db[MONGO_COLLECTION].insert(result):
                print('存储到MONGODB成功', result)
        except Exception:
            print('存储到MONGODB失败', result)

    def main(self):
        """
        主函数
        :return:
        """
        for i in range(1, MAX_PAGE + 1):
            time.sleep(1.5)
            self.index_page(i)

if __name__ == '__main__':
    taobao_product = Products()
    taobao_product.main()