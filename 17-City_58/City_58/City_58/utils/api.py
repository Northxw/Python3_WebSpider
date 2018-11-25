# -*- coding:utf-8 -*-

import requests
import json
import time
from fake_useragent import UserAgent
import logging

def get_ip_port(url):
    """
    获取API返回的JSON数据
    :param url: 代理API
    :return: 有效IP
    """
    time.sleep(1)
    response = requests.get(url)
    response = json.loads(response.text)
    result = response['RESULT']
    agent = ''
    for i in range(len(result)):
        agent = 'https://{}:{}/'.format(result[i]['ip'], result[i]['port'])
        logging.debug(agent)
    return agent

if __name__ == '__main__':
    # 代理ip
    agent = get_ip_port(url='http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=a31f8cd494e343d69b51b303859ac446&orderno=YZ2018112517118ojIuo&returnType=2&count=1')