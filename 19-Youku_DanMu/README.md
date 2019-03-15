## Youku DanMu
&emsp; **弹幕爬取01** - 网页版优酷视频《我不是药神》的弹幕数据并制作词云图。

## Explain
&emsp; 首先，播放影片并打开Chrome开发者工具,选择Network。逐步拖动进度条并观察本地与服务器的请求规律，如图：

然后，确定弹幕数据来自JS实时加载而非XHR。需要注意的是，弹幕的请求数据不是规范的JSON格式。如图：

## Other
1. 请求链接的最后一个参数类似时间戳，去掉后不会影响数据的获取。      
2. 不要使用urllib.parse.urlencode()函数构造GET请求的链接，否则获取的数据为空，亲测。

## Demo
![wordcloud](https://github.com/Northxw/Python3_WebSpider/blob/master/19-Youku_DanMu/utils/cloud.jpg)

&emsp; 从词云图可以看出，"会员、电影票、五星力荐、王传君、癌症..."等关键字最为突出。
