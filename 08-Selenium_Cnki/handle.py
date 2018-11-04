# -*- coding:utf-8 -*-

import tesserocr
import pytesseract

def handle_code(image):
    """
    处理验证码
    :param image: Image对象
    :return:
    """
    image = image.convert("L")      # 灰度处理
    threshold = 120      # 设置阈值为120(可灵活配置)
    table = []
    for i in range(256):    #
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    image = image.point(table, '1')     # 二值化处理
    result_1 = tesserocr.image_to_text(image).strip()   # 使用tesserocr获取处理结果
    result_2 = pytesseract.image_to_string(image).strip()   # 使用pytesseract获取处理结果
    # print('验证码为：', result_1)
    return result_1, result_2
