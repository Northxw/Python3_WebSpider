## Github Login
&emsp; 模拟登录Github并抓取登录后才可以访问的页面信息, 包括好友动态、个人信息等。   

## Crawl Analysis
&emsp; 模拟登录的分析思路沿袭崔大的"Python3网络爬虫开发实战"。

## Tips
+ 清除浏览器(Chrome)中Git站点的Cookies： [清除方法](https://blog.csdn.net/panbiao1999/article/details/77880649)
+ 设置Cookies的过程发生在访问登录界面的过程（可在开发者工具中查看访问登录界面的数据请求信息）
+ Form表单的authenticity_token参数可能隐藏在其他地方或者通过计算获得。对于Github而言，可在 [登录界面](https://github.com/login) 的网页源码中找到   

