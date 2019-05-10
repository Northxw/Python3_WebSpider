# -*- coding:utf-8 -*-

import requests
import re
from lxml import etree
from font import get_mapping_table
import os


def get_share_info(shareid):
    """个人主页信息"""
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
    }
    url = "https://www.iesdouyin.com/share/user/%s" % shareid
    r = requests.get(url, headers=headers)
    html = etree.HTML(r.text)
    user_info = {}
    # 昵称
    user_info['nickname'] = re.findall('class="nickname">(.*?)<', r.text, re.S)[0]
    # 抖音ID
    id_length = len(html.xpath('//p[@class="shortid"]/i'))
    regex_id = 'class="shortid">' + '.*?<i\sclass="icon iconfont ">\s(.*?);\s</i>' * id_length
    id_code_nums = re.search(regex_id, r.text, re.S).groups()
    user_info['id'] = ''.join([get_mapping_table(num) for num in id_code_nums])
    # 签名
    user_info['signature'] = re.findall('class="signature">(.*?)<', r.text, re.S)[0]
    # 头像
    user_info['avatar'] = html.xpath('//img[@class="avatar"]/@src')[0]

    # 关注
    focus_num_length = len(html.xpath('//span[contains(@class, "focus")]/span'))
    num_unit = ''.join(re.findall(r'[a-zA-Z]', ''.join(html.xpath('//span[contains(@class, "focus")]/span/text()'))))
    regex_focus = 'class="focus block">.*?<span\sclass="num">' + '.*?<i\sclass="icon iconfont follow-num">\s(.*?);\s</i>' * focus_num_length
    focus_code_nums = re.search(regex_focus, r.text, re.S).groups()
    focus = ''.join([get_mapping_table(num) for num in focus_code_nums])
    user_info['focus'] = focus if len(focus) < 5 and not num_unit else str(eval(focus) / 10) + num_unit

    # 粉丝
    fans_num_length = len(html.xpath('//span[contains(@class, "follower")]/span/i'))
    num_unit = ''.join(re.findall(r'[a-zA-Z]', ''.join(html.xpath('//span[contains(@class, "follower")]/span/text()'))))
    regex_fans = 'class="follower block">.*?<span\sclass="num">' + '.*?<i\sclass="icon iconfont follow-num">\s(.*?);\s</i>' * fans_num_length
    fans_code_nums = re.search(regex_fans, r.text, re.S).groups()
    fans = ''.join([get_mapping_table(num) for num in fans_code_nums])
    user_info['fans'] = fans if len(fans) < 5 and not num_unit else str(eval(fans) / 10) + num_unit

    # 赞
    like_num_length = len(html.xpath('//span[contains(@class, "liked-num")]/span/i'))
    num_unit = ''.join(re.findall(r'[a-zA-Z]', ''.join(html.xpath('//span[contains(@class, "liked-num")]/span/text()'))))
    regex_likes = 'class="liked-num block">.*?<span\sclass="num">' + '.*?<i\sclass="icon iconfont follow-num">\s(.*?);\s</i>' * like_num_length
    like_code_nums = re.search(regex_likes, r.text, re.S).groups()
    like_num = ''.join([get_mapping_table(num) for num in like_code_nums])
    user_info['liked_num'] = like_num if len(like_num) < 5 and not num_unit else str(eval(like_num) / 10) + num_unit

    # 作品
    user_tab_num_length = len(html.xpath('//div[@class="tab-wrap"]/div[1]/span/i'))
    num_unit = ''.join(re.findall(r'[a-zA-Z]', ''.join(html.xpath('//div[@class="tab-wrap"]/div[1]/span/text()'))))
    regex_tabs = 'class="user-tab active tab get-list" data-type="post">.*?<span class="num">' + '.*?<i\sclass="icon iconfont tab-num">\s(.*?);\s</i>' * user_tab_num_length
    tab_code_nums = re.search(regex_tabs, r.text, re.S).groups()
    tab_num = ''.join([get_mapping_table(num) for num in tab_code_nums])
    user_info['tab_num'] = tab_num if len(tab_num) < 5 and not num_unit else str(eval(tab_num) / 10) + num_unit

    # 喜欢
    like_tab_num_length = len(html.xpath('//div[@class="tab-wrap"]/div[2]/span/i'))
    num_unit = ''.join(re.findall(r'[a-zA-Z]', ''.join(html.xpath('//div[@class="tab-wrap"]/div[2]/span/text()'))))
    regex_like_tabs = 'class="like-tab tab get-list" data-type="like">.*?<span class="num">' + '.*?<i\sclass="icon iconfont tab-num">\s(.*?);\s</i>' * like_tab_num_length
    like_tab_code_nums = re.search(regex_like_tabs, r.text, re.S).groups()
    like_tab_num = ''.join([get_mapping_table(num) for num in like_tab_code_nums])
    user_info['like_tab_num'] = like_tab_num if len(like_tab_num) < 5 and not num_unit else str(eval(like_tab_num) / 10) + num_unit

    return user_info


if __name__ == '__main__':
    # print(get_share_info('98524936524'))
    shareid_path = os.path.dirname(os.path.realpath(__file__)) + "\\shareid.txt"
    with open(shareid_path) as f:
        shareid_list = f.readlines()
    for shareid in shareid_list:
        print(get_share_info(shareid.strip()))
