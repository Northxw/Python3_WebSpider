"""
提示：该文件仅用于生成xml结构文件, 便于分析问题（如作者的原文所述）
"""
from fontTools.ttLib import TTFont

font = TTFont('01.ttf')
font.saveXML('01.xml')      # 将ttf文件转化成xml格式并保存到本地（主要是方便查看内部数据结构）
