# Project Name
&emsp; 使用Selenium注册并登录中国知网并识别知网的图形验证码。

# Sort
&emsp; **验证码识别** - 图形验证码

# Demand
**1. Selenium** - 建议使用低版本的Python-Selenium库，因为高版本在Chrome中不支持。
```
pip3 install selenium==2.48.0
```
**2. chromedriver.exe** - download_addr：http://npm.taobao.org/mirrors/chromedriver/

**3. Chaojiying_Python.rar** - download_addr：http://www.chaojiying.com/download/Chaojiying_Python.rar

# Process analysis
#### 1.验证码类型     
&emsp; 知网注册页的验证码类型属于常见四位英文和数字组成的验证码。可以在超级鹰的 [验证码类型于价格表](http://www.chaojiying.com/price.html#table-item5) 页面参考。

#### 2.Python识别库 - tesserocr、pytesseract      
&emsp; 这两个三方库识别精度均较差, 字体略微差异可能就不是正常结果。所以选择超级鹰识别，识别前可做灰度、二值化处理（我这里做了注释选择不用，感觉平台打码精度挺高的），代码如下：
```Python
def handle_code(image):
    """
    处理验证码
    :param image: Image对象
    :return:
    """
    # 灰度处理
    image = image.convert("L")
    # 阈值120(可灵活配置)
    threshold = 120
    table = []
    for i in range(256):    #
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    # 二值化处理
    image = image.point(table, '1')
    # 使用tesserocr获取处理结果
    result_1 = tesserocr.image_to_text(image).strip()
    # 使用pytesseract获取处理结果
    result_2 = pytesseract.image_to_string(image).strip()   
    # print('验证码为：', result)
    # 两者识别结果相同再继续程序，否则循环识别。但是代价很大，所以弃用。
    return result_1, result_2
```

# Other
&emsp; 代码可继续扩展，例如：登录后知网文献的爬取，并做数据可视化分析等。

# Demo
![程序运行的GIF动态演示图](https://github.com/Northxw/Python3_WebSpider/blob/master/08-Selenium_Cnki/demo/demo.gif)
