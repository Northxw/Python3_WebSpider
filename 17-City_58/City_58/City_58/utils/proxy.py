# -*- coding:utf-8 -*-

"""
轻量级ip代理池, 以89代理网站为例, ip成活率较低, 可做测试使用.
"""

import requests
from pyquery import PyQuery
from fake_useragent import UserAgent
import random

def get_ip_port(page):
    """
    获取网页的ip和port
    :param page: 页码
    :return: 随机ip
    """
    # 请求头(根据需要另行设置)
    headers = dict()
    # 代理池
    agents = list()
    for i in range(page):
        url = 'http://www.89ip.cn/index_{}.html'.format(i+1)    # 格式化请求链接
        response = requests.get(url)          # 获取网页内容

        if response.status_code == 200:
            jpy = PyQuery(response.text)
            tr_list = jpy('div.layui-form > table > tbody > tr').items()
            for tr in tr_list:
                ip = tr('td:nth-child(1)').text()
                port = tr('td:nth-child(2)').text()
                agent = 'http://{}:{}'.format(ip, port)         # 格式化ip,port
                agents.append(agent)                            # 添加至代理池
        else:
            print('The status code is {},Try again! '.format(response.status_code))

    # 检测有效ip代理,随机返回使用
    return random.choices(test_agent(agents))[0]

def test_agent(agents):
    """
    针对58同城测试获取的免费代理
    :param agents: 代理池
    :return: 有效的代理
    """
    agents_copy = agents
    for agent in agents_copy:
        try:
            res = requests.get('https://cd.58.com/', proxy=agent)
        except Exception as e:
            agents.remove(agent)
            continue
    return agents

if __name__ == '__main__':
    print(get_ip_port(random.randint(2, 4)))