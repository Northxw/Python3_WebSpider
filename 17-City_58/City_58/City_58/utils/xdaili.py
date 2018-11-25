# -*- coding:utf-8 -*-

"""
提示：讯代理的Python3接入文档需要稍作修改,方能使用.
"""

import sys
import time
import hashlib
import requests
# import grequests
from lxml import etree

class Xdaili(object):
    def __init__(self):
        self.orderno = 'ZF201810230685eMVeQa'
        self.secret = 'ddde303a69274c989a308dc86e5e7a51'
        self.ip = "forward.xdaili.cn"
        self.port = '80'
        self.ip_port = self.ip + ":" + self.port

    def proxy(self):
        # 时间戳
        timestamp = str(int(time.time()))
        # 签名算法参数
        string = "orderno=" + self.orderno + "," + "secret=" + self.secret + "," + "timestamp=" + timestamp
        # Python3需要编码
        string = string.encode()
        # 计算sign
        md5_string = hashlib.md5(string).hexdigest()
        # 转大写
        sign = md5_string.upper()
        # auth
        auth = "sign=" + sign + "&" + "orderno=" + self.orderno + "&" + "timestamp=" + timestamp
        proxy = {
            "http": "http://" + self.ip_port,
            "https": "https://" + self.ip_port
        }
        return [auth, proxy]
