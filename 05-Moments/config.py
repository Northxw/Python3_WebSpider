# -*- coding:utf-8 -*-

import os

# 设备类型：Android 或 iOS
PLANTFORM = 'Android'
# 设备名称：可在命令行输入 adb devices -l 获取
DEVICE_NAME = 'vivo_X7'
# APP包名
APP_PACKAGE = 'com.tencent.mm'
# 入口类型
APP_ACTIVITY = '.ui.LauncherUI'

# APP安装包路径（手机没有安装微信时，通过修改启动参数完成安装并启动微信执行后续操作）
APP = os.path.abspath('.') + '/weixin.apk'

# Appium 服务地址
DRIVER_SERVER = 'http://localhost:4723/wd/hub'

# 元素加载时间（一般退出重新登录的耗时主要在登录和加载数据界面，可根据设备运行速度灵活调整）
TIMEOUT = 200

# 微信登录的手机号、密码
USERNAME = '132********'    # 你的手机号码
PASSWORD = '123456789'       # 你的微信账号密码

# 滑动点
FLICK_START_X = 300
FLICK_START_Y = 300
FLICK_DISTANCE = 500

# 滑动的间隔时间
SCROLL_SLEEP_TIME = 3      #设置间隔5秒+是确保新加载的朋友圈节点信息能完全加载出来

# MYSQL数据库配置
HOST = 'localhost'
USER = 'root'
PASSWORD_ = '123456'
PORT = 3306
DB = 'wechat'

# MongoDB配置
MONGO_URL = 'localhost'
MONGO_DB = 'wechat'
MONGO_COLLECTION = 'moments'
