### 1.声明:
*本次爬取参考* ***"崔庆才-Python3网络爬虫开发实践"*** *第七章7.4节*

### 2.Selenium爬取淘宝商品数据信息简介：
+ 使用Selenium模拟浏览器操作，抓取淘宝商品数据，并将结果存储至MongoDB
+ 商品信息包括：商品图片、名称、价格、购买人数、店铺名称和店铺所在地信息
+ 需要事先安装Chorme浏览器和[对应版本的ChromeDriver](http://chromedriver.storage.googleapis.com/index.html)；另外, 需要[正确安装Selenium库](https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=94886267_hao_pg&wd=selenium%20%E5%AE%89%E8%A3%85&oq=Python%2520selenium%2520%25E5%25AE%2589%25E8%25A3%2585&rsv_pq=968033890000f449&rsv_t=ff28w%2F%2F3j0ZIipTUPJ2g1a13bUlLQ71Dquj0NKcSpikZQOkhVzntwnlssg%2Bun2mBGn7Chmnh&rqlang=cn&rsv_enter=1&inputT=29847&rsv_sug3=33&rsv_sug1=26&rsv_sug7=100&bs=Python%20selenium%20%E5%AE%89%E8%A3%85)
+ 采取Selenium爬取的原因：不需要考虑Ajax接口及其参数的规律，只要在浏览器中可以看到的，都可以爬取

### 3.待优化的地方
+ 商品数据待做数据可视化分析。原因：购买者需要看到真实的评价情况或者好评度等等，若做条形图或饼状图将会更加直观，节省时间，提高效率
+ 数据库存储。原因：如果根据用户键盘输入关键字搜索商品，需要根据不同的关键字创建不同的数据库，做到随机应变
+ 商品数据去重。商品数据是否需要去重，这是一个应该考虑的问题，原因：比如某个商家开了两家ID不同而销售相同物品

### 4.存在的问题
+ 未解决爬取过程的用户登录以及验证码问题，后期定会解决，时间问题
+ 爬取速度