# -*- coding:utf-8 -*-

import re
import requests
import lxml.html

def get_css_text(class_):
    """
    获取坐标值
    """
    css_html = requests.get('https://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/1595b8f4917c831efb53461c8d9b86cb.css').text
    info_css = re.findall(r'%s{background:-(\d+).0px -(\d+).0px' % class_, css_html, re.S)[0]
    return info_css

def get_completed_nums(compelted_nums=''):
    """
    获取数字
    """
    result_svgtext = requests.get('http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/7226aa7d9b89866aecb63ab0f06ca037.svg').text
    a, b, c = re.findall('y=.*?>(.*?)<', result_svgtext, re.S)                  # 示例a：56422383356911691085268889707857...
    y1, y2, y3 = re.findall('y="(.*?)">', result_svgtext, re.S)                 # 示例: 46, 83, 129
    divisor = eval(re.search('x="(\d{2}) ', result_svgtext, re.S).group(1))     # 示例：x = 12,......
    for class_ in class_list:
        x, y = get_css_text(class_)
        x, y = int(x), int(y)
        if y < int(y1):
            compelted_nums += a[x // divisor]
        elif y < int(y2):
            compelted_nums += b[x // divisor]
        elif y < int(y3):
            compelted_nums += c[x // divisor]
    print("总评论数：", compelted_nums)
    return compelted_nums

if __name__ == '__main__':
    class_list = ['ovr2h', 'ovjpg', 'ovra6', 'ovzs7']
    get_completed_nums()