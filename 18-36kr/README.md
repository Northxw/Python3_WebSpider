## Spider 36kr
&emsp; 爬取36氪的最新文章信息并存储至Mysql、制作中文词云图,  爬取内容包含文章ID, 标题，封面图片链接，发布时间，类别名称等。

## Explain
&emsp; 首先，确定36氪的新闻信息是通过Js加载；然后，打开谷歌浏览器开发者工具选择NetWork寻找真实请求的URL；最后，编写Code爬取文章信息。

&emsp; 注意：真实请求URL最后的数字参数是时间戳，去掉后可正常获取网页内容。

## Demo
![db](https://github.com/Northxw/Python3_WebSpider/blob/master/18-36kr/utils/db.png)
&emsp;
![wordcloud](https://github.com/Northxw/Python3_WebSpider/blob/master/18-36kr/utils/cloud.jpg)
