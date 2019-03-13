## Youku DanMu
&emsp; 爬取优酷网页视频-我不是药神的弹幕数据并制作词云图。

## Explain
&emsp; 首先，毋庸置疑的打开谷歌开发者工具并选择Network选项卡; 然后，确定弹幕数据来自JS实时加载而非XHR; 最后，拖动进度条寻找请求链接的规律并编写代码爬取。

&emsp; 注意：(1)请求链接的最后一个参数类似时间戳，去掉后不会影响数据的获取；(2)不要使用urllib.parse.urlencode方式构造GET请求的链接，否则获取的数据为空，亲测。

## Demo
![wordcloud](https://github.com/Northxw/Python3_WebSpider/blob/master/19-Youku_DanMu/utils/cloud.jpg)
&emsp; 从词云图可以看出，"会员、女人、五星力荐、王传君、癌症..."等关键字最为突出。
