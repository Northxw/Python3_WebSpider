#!/usr/bin/env python

import requests
import time
import hashlib


class Chaojiying_Client(object):

    def __init__(self, username, password, soft_id):
        self.username = username
        password = password.encode('utf8')
        self.password = hashlib.md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id: 报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()


class Crack_Sougou_Anti(object):

    def __init__(self, url):
        self.normal_url = url       # 正常页面URL
        self.session = requests.Session()
        self.seccode_url = "https://weixin.sogou.com/antispider/util/seccode.php?tc={}"     # 验证码图片的接口地址
        self.thank_url = "https://weixin.sogou.com/antispider/thank.php"                    # 提交接口
        self.url_quote = self.normal_url.split('weixin.sogou.com/')[-1]
        self.chaojiying = Chaojiying_Client('Northxw', '000000', 123456)                    # 打码平台的账号、密码、软件ID
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            , 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/74.0.3729.169 Chrome/74.0.3729.169 Safari/537.36'
            , 'Referer': 'http://weixin.sogou.com/antispider/?from=%2f' + self.url_quote
        }

    def get_captcha(self):
        """
        获取验证码
        :return: 字节流验证码
        """
        self.session.get(self.normal_url)
        img = self.session.get(self.seccode_url.format(str(int(time.time()*1000))), headers=self.headers).content
        # with open("captcha.png", 'wb+') as f:
        #     f.write(img)
        return img

    def get_captcha_result(self, img):
        """
        返回识别结果
        :param img: 字节流验证码
        :return: 识别结果
        """
        captcha_result = self.chaojiying.PostPic(img, 1902)
        result = captcha_result.get("pic_str")
        print("captcha code:", result)
        return result

    def send_post(self, result):
        """
        发送成功请求
        :return: normal code
        """
        data = {
            "c": result
            , "r": '%2F' + self.url_quote
            , "v": 5
        }
        code = self.session.post(self.thank_url, data, self.headers).json()['code']
        return code

    def crack(self):
        """
        验证码识别主逻辑
        :return: statue code
        """
        img = self.get_captcha()
        result = self.get_captcha_result(img)
        code = self.send_post(result)
        return 200 if code == 0 else 501


if __name__ == "__main__":
    url = "https://weixin.sogou.com/weixin?type=1&s_from=input&query=caitongzhengquan&ie=utf8&_sug_=n&_sug_type_="
    crack = Crack_Sougou_Anti(url)
    print(crack.crack())
