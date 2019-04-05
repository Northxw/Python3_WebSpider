## Github Login
&emsp; 使用 Scrapy 的 FormReqeust 模拟登陆 Github。

## Sort
&emsp; **模拟登陆 - FormReqeust**

## Analysis
#### 1. 清除Cookies
&emsp; 查找POST表单参数之前先清除待爬取站点的Cookies。

#### 2. Form表单
&emsp; 打开Github登陆界面，F12打开开发者工具并选择All，正常登陆Github，在请求列表中可以看到session请求，然后查看POST参数。

#### 3. 表单参数 - authenticity_token
&emsp; 该参数是在访问登陆界面时浏览器设置的，可以在登陆界面的源码中找到。

#### 4. Cookies
&emsp; 利用Scrapy的FormReqeust模拟登陆时，不需要像requests模拟登陆时保存Cookies, 因为在后续的Request中会默认将前面的Cookies携带。

## Tip
&emsp;  截止2019/4/2 19:50代码运行无误。
