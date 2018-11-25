# -*- coding:utf-8 -*-

"""
@title: 本段代码用于解析数据、处理数据、测试各个待抓取的页面。
"""

import re
import base64
from fontTools.ttLib import TTFont
from io import BytesIO
from xdaili import Xdaili
from scrapy import Selector
import requests

def parse_xiaoqu(response):
    """
    抓取小区列表页
    :param response: 例如 http://cd.58.com/xiaoqu/21611/ 网页的响应
    :return: 所有小区的URL
    """
    selector = Selector(text=response.text)
    xiaoqu_url_list = selector.css('.t::attr("href")').extract()
    xiaoqu_url_list = [url.split()[0] for url in xiaoqu_url_list]   # 处理有Bug的小区详情页链接, 比如：https://cd.58.com/xiaoqu/ruisheng xiangshulinhuafu/
    return xiaoqu_url_list

def parse_xiaoqu_detail(response):
    """
    抓取小区详情页
    :param response: 例如 https://cd.58.com/xiaoqu/nanhuguojishequ/ 网页的响应
    :return: 小区详细信息的字典(主要信息包括小区名称，小区参考房价，小区地址，小区建筑年代)
    """
    result = dict()
    selector = Selector(text=response.text)
    result['name'] = selector.css('.title-bar .title::text').extract_first('成都小区')
    result['location'] = selector.css('.title-bar .addr::text').extract_first('成都')
    result['price'] = selector.css('.price-container .price::text').extract_first('15000')
    result['address'] = selector.css('.info-tb-container .info-tb').xpath('//tr[1]/td[4]/text()').extract_first('成都').strip()
    result['times'] = selector.css('.info-tb-container .info-tb').xpath('//tr[5]/td[2]/text()').extract_first().strip()
    return result

def get_ershoufang_list_page(response):
    """
    获取二手房页面的所有房价数据
    :param response: 例如：https://cd.58.com/xiaoqu/nanhuguojishequ/ershoufang/ 网页的响应
    :return: 价格列表
    """
    selector = Selector(text=response.text)
    price_tag = selector.css('.listwrap .tbimg').xpath('//tr/td[3]/span[1]/text()').extract()
    price_list = [i.replace('元/㎡', '') for i in price_tag]        # 遍历price_tag截取到倒数第三个元素
    return price_list

def get_chuzu_detail_page_list_url(response):
    """
    获取出租房页面的所有详情页链接
    :param response: 例如：https://cd.58.com/xiaoqu/nanhuguojishequ/chuzu/ 网页的响应
    :return: 所有出租房详情页的列表
    """
    result = dict()
    selector = Selector(text=response.text)
    chuzu_detail_url_list = selector.xpath('//*[@id="infolist"]/div[2]/table//tr/td[2]/a[1]/@href').extract()
    return chuzu_detail_url_list

def get_chuzu_house_info(response):
    """
    获取出租房详情页的数据
    :param response: 例如：https://cd.58.com/pinpaigongyu/36183067306911x.shtml 网页的响应
    :return: 出租房的相关数据
    """
    response = parse_font(response)
    result = dict()
    selector = Selector(text=response)
    result['name'] = selector.xpath('/html/body/div[3]/h2/text()').extract_first('^_^').strip()
    result['zu_price'] = selector.css('.detail_header .price::text').extract_first('Secret').strip()
    # 获取房屋面积及户型并处理
    _ = selector.css('.gray-wrap .house-desc .fr.pr.strongbox .house-info-list')
    result['mianji'] = _.xpath('./li[1]/span/text()').extract_first().replace(' ', '').strip()
    result['type'] = _.xpath('./li[2]/span/text()').extract_first().replace(' ', '').strip().split('\r\n')[0]
    return result

def parse_font(response):
    """
    处理出租房详情页的字体反爬
    :param response: 网页返回结果
    :return: 处理后的网页源码
    """
    if response:
        base64_str = re.findall('data:application/font-ttf;charset=utf-8;base64,(.*)\'\) format\(\'truetype\'\)}',
                                response.text)

        bin_data = base64.b64decode(base64_str[0])
        fonts = TTFont(BytesIO(bin_data))
        bestcmap = fonts.getBestCmap()
        newmap = {}
        for key in bestcmap.keys():
            # print(key)
            # print(re.findall(r'(\d+)', bestcmap[key]))
            value = int(re.findall(r'(\d+)', bestcmap[key])[0]) - 1
            key = hex(key)
            newmap[key] = value

        resp_ = response.text
        for key, value in newmap.items():
            key_ = key.replace('0x', '&#x') + ';'
            if key_ in resp_:
                resp_ = resp_.replace(key_, str(value))
        return resp_

if __name__ == '__main__':
    # 设置代理
    auth, proxy = Xdaili().proxy()
    # url = 'https://cd.58.com/xiaoqu/21611/'                           # 小区列表页测试链接
    # url = 'https://cd.58.com/xiaoqu/nanhuguojishequ/'                 # 小区详情页
    # url = 'https://cd.58.com/xiaoqu/nanhuguojishequ/ershoufang/'      # 二手房页面
    # url = 'https://cd.58.com/xiaoqu/nanhuguojishequ/chuzu/'           # 出租房页面
    url = 'https://cd.58.com/pinpaigongyu/36183067306911x.shtml'        # 出租房详情页信息
    # 请求头
    headers = {"Proxy-Authorization": auth}
    # 发送请求,接收响应
    result = get_chuzu_house_info(requests.get(url, headers=headers, proxies=proxy, verify=False, allow_redirects=False))
    print(result)