# -*- encoding:utf-8 -*-

from selenium import webdriver

import zipfile

class Xdaili(object):
    def __init__(self):
        """
        初始化信息
        """
        # 代理服务器
        self.ip = "forward.xdaili.cn"
        self.port = '80'
        # 订单号和个人密钥(可在讯代理官网购买)
        self.orderno = "ZF2018***********"
        self.secert = "**********************************"

    def auth(self):
        """
        构造代理
        :return:
        """
        manifest_json = """
            {
                "version": "1.0.0",
                "manifest_version": 2,
                "name": "Xdaili Proxy",
                "permissions": [
                    "proxy",
                    "tabs",
                    "unlimitedStorage",
                    "storage",
                    "<all_urls>",
                    "webRequest",
                    "webRequestBlocking"
                ],
                "background": {
                    "scripts": ["background.js"]
                },
                "minimum_chrome_version":"22.0.0"
            }
            """

        background_js = """
            var config = {
                mode: "fixed_servers",
                rules: {
                    singleProxy: {
                        scheme: "http",
                        host: "%(ip)s",
                        port: "%(port)s")
                    },
                    bypassList: ["foobar.com"]
                }
                };

            chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

            function callbackFn(details) {
                return {
                    authCredentials: {
                        username: "%(orderno)s",
                        password: "%(secert)s"
                    }
                };
            }

            chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
            );
            """ % {'ip': self.ip, 'port': self.port, 'orderno': self.orderno, 'secert': self.secert}
        playin_file = './utils/proxy_auth_plugin.zip'
        with zipfile.ZipFile(playin_file, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
