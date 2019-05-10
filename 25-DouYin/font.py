# -*- coding:utf-8 -*-

# import requests
# import re
# import time
# 
# headers = {
#         "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
# }
# 
# def crack_font():
#     """处理反爬"""
#     url = "https://www.iesdouyin.com/share/user/59498826860"
#     response = requests.get(url, headers=headers)
#     ttf_url = "https://%s" % re.findall("format\('woff'\),url\(//(.*?\.ttf)\)", response.text, re.S)[0]  # 匹配字体文件链接
#     print(ttf_url)
#     # get_mapping_table(ttf_url)

def get_mapping_table(codeNum):
    """处理文字"""
    font_code_map = {
      "&#xe602": "num_",
      "&#xe603": "num_1",
      "&#xe604": "num_2",
      "&#xe605": "num_3",
      "&#xe606": "num_4",
      "&#xe607": "num_5",
      "&#xe608": "num_6",
      "&#xe609": "num_7",
      "&#xe60a": "num_8",
      "&#xe60b": "num_9",
      "&#xe60c": "num_4",
      "&#xe60d": "num_1",
      "&#xe60e": "num_",
      "&#xe60f": "num_5",
      "&#xe610": "num_3",
      "&#xe611": "num_2",
      "&#xe612": "num_6",
      "&#xe613": "num_8",
      "&#xe614": "num_9",
      "&#xe615": "num_7",
      "&#xe616": "num_1",
      "&#xe617": "num_3",
      "&#xe618": "num_",
      "&#xe619": "num_4",
      "&#xe61a": "num_2",
      "&#xe61b": "num_5",
      "&#xe61c": "num_8",
      "&#xe61d": "num_9",
      "&#xe61e": "num_7",
      "&#xe61f": "num_6",
    }

    font_num_map = {
        "1": "num_",
        "0": "num_1",
        "3": "num_2",
        "2": "num_3",
        "4": "num_4",
        "5": "num_5",
        "6": "num_6",
        "9": "num_7",
        "7": "num_8",
        "8": "num_9",
    }
    codeNumMap = font_code_map[codeNum]
    decodeNum = ''
    if codeNumMap in font_num_map.values():
        decodeNum = ''.join([k for k, v in font_num_map.items() if codeNumMap == v])
    return decodeNum


if __name__ == '__main__':
    print(get_mapping_table("&#xe60b"))