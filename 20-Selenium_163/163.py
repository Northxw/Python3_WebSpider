# -*- coding:utf-8 -*-

"""
Created at 17:43 at March 15,2019
@title: 模拟登录网易163邮箱并发送SOS邮件
@author: Northxw
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from utils.config import *
import pymysql
import re
import time

class Mailbox(object):
    def __init__(self):
        """
        初始化
        """
        self.url = URL
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, TIME_OUT)   # 显式等待时间10秒
        # 邮箱账号密码
        self.mail_user = MAIL_USER
        self.mail_pass = MAIL_PASS
        # MySql用户名密码
        # self.user = MYSQL_USER
        # self.pass_ = MYSQL_PASS

    def __del__(self):
        self.browser.close()

    def login_email(self):
        """
        登陆网页版网易163邮箱
        :return: None
        """
        self.browser.get(self.url)
        # 获取iframe节点
        frame_1 = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                                '//*[@id="loginDiv"]/iframe')))
        # 切换Frame
        self.browser.switch_to.frame(frame_1)
        time.sleep(3)
        # 账号输入框
        user = self.wait.until(EC.presence_of_element_located((By.NAME, 'email')))
        # 密码输入框
        password = self.wait.until(EC.presence_of_element_located((By.NAME, 'password')))
        # 登录按钮
        button = self.wait.until(EC.element_to_be_clickable((By.ID, 'dologin')))
        # 输入账号
        user.clear()
        user.send_keys(self.mail_user)
        time.sleep(3)
        # 输入密码
        password.clear()
        password.send_keys(self.mail_pass)
        time.sleep(3)
        # 登录
        button.click()
        time.sleep(10)
        # 获取登录成功后界面左上角的Logo,验证登录成功.
        logo = self.wait.until(EC.presence_of_element_located((By.ID, 'h1Logo')))
        if logo:
            print('Successful login!')

    def send_email(self):
        """
        发送邮件
        :return: None
        """
        try:
            # "写信"节点
            send_ = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "mD0")]')))
            send_.click()
            time.sleep(5)
            # 收件人
            recipient = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'nui-editableAddr-ipt')))
            recipient.clear()
            recipient.send_keys(RECIPIENT)
            time.sleep(3)
            # 切换frame
            frame = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="APP-editor-iframe"]')))
            self.browser.switch_to.frame(frame)
            # 邮件内容
            content = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="nui-scroll"]')))
            content.clear()
            content.send_keys(CONTENT)
            time.sleep(3)
            # 切换至父级frame
            self.browser.switch_to.parent_frame()
            # 发送
            send_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="jp0"]/div[1]/span[1]')))
            send_button.click()
            time.sleep(3)
            # 确定不添加主题
            sure = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="nui-msgbox-ft-btns"]/div[1]/span')))
            sure.click()
            time.sleep(3)
            print('Send successfully！')
        except NoSuchElementException as e:
            print('Failed!')

    '''
        def get_email_info(self):
        """
        获取邮件的相关信息
        :return: None
        """
        # 收件箱节点
        Inbox = self.wait.until(EC.presence_of_element_located((
            By.XPATH, '//*[@id="dvNavTree"]/ul/li[1]')))
        # 切换至"收件箱"页面
        Inbox.click()
        # 延时等待
        time.sleep(10)
        # message
        messages = list()
        try:
            # 获取包含页码的节点
            page_element = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="nui-select-text"]')))
            # 获取收件箱总页码
            page = page_element.text.split('/')[-1]
            time.sleep(3)
            if page:
                for i in range(int(page)):
                    # 获取当前页面所有邮箱节点
                    divs = self.browser.find_elements((By.XPATH, '//*[contains(@class, "rF0")]'))
                    print(divs)
                    # divs = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'')))
                    for div in range(len(divs)):
                        # 获取每个div节点的aria-label属性(包含所有有效信息)
                        summary = div.get_attritubute('aria-label')
                        # 获取aria-label属性值
                        result = summary.split()
                        # result = re.findall(r'(.*?) 发件人 ：(.*?) 时间：(.*?$)', s)  正则匹配有效数据
                        messages.append({
                            'sender': result[3],
                            'content': result[0],
                            'time': '{} {} {}'.format(result[5], result[6], result[7])
                        })
                    # 下拉底部
                    self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                    # 下一页
                    time.sleep(3)
                    print('正在爬取第{}页'.format(str(i)))
                    next_page = self.wait.until(
                        EC.presence_of_element_located((By.XPATH, '//*[@class="nui-btn-text"]'))
                    )
                    next_page.click()
            return messages
        except NoSuchElementException as e:
            print('Error acquiring information!')
            return None

    def connect_db(self):
        """
        创建数据库连接对象
        :return: db
        """
        db = pymysql.connect(host=MYSQL_LOCALHOST, user=self.user, password=self.pass_,port=MYSQL_PORT, db=MYSQL_DB)
        # print('Successful connection!')
        return db

    def save_db(self, messages):
        """
        数据入库
        :messages: 邮件信息
        :return: None
        """
        db = self.connect_db()
        # 获取数据库操作指针
        cursor = db.cursor()
        # 数据库表格
        table = '163'
        for message in messages:
            keys = ', '.join(message.keys)
            values = ', '.join(['%s'] * len(message))
            sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(
                table = table, keys=keys, values=values
            )
            try:
                if cursor.execute(sql, tuple(message.values())):
                    # print('Successful')
                    db.commit()
            except:
                # print('Failed')
                db.rollback()
        db.close()
    '''

    def main(self):
        """
        主函数
        :return: None
        """
        # 登录邮箱
        self.login_email()
        # 发送邮件
        self.send_email()

if __name__ == '__main__':
    mail = Mailbox()
    mail.main()