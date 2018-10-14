from fontTools.ttLib import TTFont

font1 = TTFont('01.ttf')    # 打开本地文件01.ttf
obj_list1 = font1.getGlyphNames()[1:-1]     # 获取所有字符的对象, 去除第一个和最后一个
uni_list1 = font1.getGlyphOrder()[2:]       # 获取所有编码, 去除前两个

# 手动确认编码和数字之间的对应关系,保存到字典中（利用FontCreator软件）
dict = {
    'uniEEC3': '1',
    'uniE1B7': '2',
    'uniE8F9': '3',
    'uniE30D': '4',
    'uniF045': '5',
    'uniF742': '6',
    'uniEBE3': '7',
    'uniE8A3': '8',
    'uniEA2D': '9',
    'uniE755': '0',
}

font2 = TTFont('02.ttf')    # 打开访问网页新获得的字体文件02.ttf
obj_list2 = font2.getGlyphNames()[1: -1]
uni_list2 = font2.getGlyphOrder()[2:]

for uni2 in uni_list2:
    obj2 = font2['glyf'][uni2]  # 获取编码uni2在02.ttf中对应的对象
    for uni1 in uni_list1:
        obj1 = font1['glyf'][uni1]
        if obj1 == obj2:
            print(uni2, dict[uni1])     # 打印结果, 编码uni2和对应的数字
