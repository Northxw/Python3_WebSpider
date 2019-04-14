# -*- coding:utf-8 -*-

import smtplib
from email.mime.text import MIMEText

class EmailSender(object):
    def __init__(self):
        # 发送方smtp服务器
        self.smtp_host = 'smtp.163.com'
        # 发送方邮箱(同于登录smtp服务器)
        self.smtp_user = 'northxw@163.com'
        # 授权码
        self.smtp_authcode = '123456'
        # smtp服务器默认端口465
        self.smtp_port = 465
        # 发送方邮箱
        self.sender = 'northxw@163.com'

    def sendEmail(self, recipient_list, email_subject, body):
        """
        发送邮件
        :param recipient_list: 收件人列表
        :param email_subject: 邮件主题
        :param body: 邮件内容
        :return: None
        """
        # 邮件内容、格式、编码
        message = MIMEText(_text=body, _subtype='plain', _charset='utf-8')
        # 发件人
        message['From'] = self.sender
        # 收件人
        message['To'] = ', '.join(recipient_list)
        # 主题
        message['Subject'] = email_subject
        try:
            # 实例化SMTP_SSL对象
            smtpSSLClient = smtplib.SMTP_SSL(self.smtp_host,self.smtp_port)
            # 登录
            loginResult = smtpSSLClient.login(self.smtp_user, self.smtp_authcode)
            # loginRes = (235, b'Authentication successful')
            print("Login Result：LoginRes = {}".format(loginResult))

            if loginResult and loginResult[0] == 235:
                print("Successful login, Code = {}".format(loginResult[0]))
                smtpSSLClient.sendmail(self.sender, recipient_list, message.as_string())
                print("Successful delivery. Message:{}".format(message.as_string()))
            else:
                print("Login failed, Code = {}".format(str(loginResult[0])))

        except Exception as e:
            print("Failed to send, Exception: e={}".format(e))
