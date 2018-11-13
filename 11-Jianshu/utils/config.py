# -*- coding:utf-8 -*-

# APPIUM服务器
DRIVER_SERVER = 'http://localhost:4723/wd/hub'

# 启动参数：设备类型、名称、APP包名、入口类型
PLATFORM = 'Android'
DEVICE_NAME = 'vivo_X7'
APP_PACKAGE = 'com.jianshu.haruki'
APP_ACTIVITY = 'com.baiji.jianshu.MainActivity'

# 简书账号、密码
USER_PHONENUMBER = '********'
PASSWORD = '********'

# MONGODB数据库配置
MONGO_URL = 'localhost'
MONGO_DB = '17-Jianshu'
MONGO_COLLECTION = 'content'

# 等待时间
TIMEOUT = 100

# 滑动点
FLICK_START_X = 300
FLICK_START_Y = 300
FLICK_DISTANCE = 600

# 滑动的间隔时间
SCROLL_SLEEP_TIME = 3
