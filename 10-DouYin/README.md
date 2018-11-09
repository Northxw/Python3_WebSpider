## DouYin
&emsp; 使用 Mitmdump 爬取 "抖音" App短视频信息，包含标题、视频下载地址、作者、发布时间、获赞数等。

## Explain
+ 程序需手动上滑视频触发请求接口(后期不打算自动化,有兴趣可以自行完善,有任何疑问都可邮箱联系)。
+ 运行结果以JSON格式保存(非规范格式,需要处理)。
+ 执行脚本后出现红色报错的原因：数据未加载或未完全加载,待缓冲结束,便可正常获取数据。
+ 注意：程序不能使用MongoDB或Mysql数据库保存([传送门](https://github.com/Python3WebSpider/IGetGet/issues/1)), 具体原因尚不清楚。

## Demo
&emsp; ![程序运行动图](https://github.com/Northxw/Python3_WebSpider/blob/master/10-DouYin/demo/demo.gif)
