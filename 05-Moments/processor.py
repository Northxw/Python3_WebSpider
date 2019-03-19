# -*- coding:utf-8 -*-

import time
import re

class Processor():
    def date(self, datetime):
        """
        格式化时间
        :param date: 原始时间
        :return: 处理后时间
        """
        if re.match('\d+分钟前', datetime):
            minute = re.match('(\d+)', datetime).group(1)
            datetime = time.strftime('%Y-%m-%d', time.localtime(time.time() - float(minute) * 60))
        if re.match('\d+小时前', datetime):
            hour = re.match('(\d+)', datetime).group(1)
            datetime = time.strftime('%Y-%m-%d', time.localtime(time.time() - float(hour) * 60 * 60))
        if re.match('昨天', datetime):
            datetime = time.strftime('%Y-%m-%d', time.localtime(time.time() - 24 * 60 * 60))
        if re.match('\d+天前', datetime):
            day = re.match('(\d+)', datetime).group(1)
            datetime = time.strftime('%Y-%m-%d', time.localtime((time.time()) - float(day) * 24 * 60 * 60))
        return datetime