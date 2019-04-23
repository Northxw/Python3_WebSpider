## 大众点评字体反爬
&emsp; 大众点评css定位的字体反爬解决方案

## 处理思路
- 请求CSS链接获取文本内容，正则匹配class对应的坐标值
- 请求SVG链接，正则匹配被除数以及偏移文本
- 判断、获取、拼接数字

## 示例
&emsp; 网页对应文字截图（https://www.dianping.com/xian/ch0）：

![prt1](https://github.com/Northxw/Python3_WebSpider/blob/master/24-Dianping/utils/prtsc1.png)

&emsp; 代码运行结果截图：

![prt5](https://github.com/Northxw/Python3_WebSpider/blob/master/24-Dianping/utils/prtsc5.png)
