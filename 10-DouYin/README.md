# DouYin
&emsp; 使用 Mitmdump 爬取 "抖音" App短视频信息，包含标题、视频下载地址、作者、发布时间、获赞数等。

# Sort
&emsp; **非自动化爬取App数据** - 基于Mitmproxy的Mitmdump组件实现APP数据的爬取。

# Explain
#### 1. Charles获取视频接口
&emsp;爬取之前先将手机与PC至于同局域网并确保手机WIFI的代理端口为8888，然后打开Charles获取视频请求的链接，如图：

![video_url](https://github.com/Northxw/Python3_WebSpider/blob/master/10-DouYin/plates/charles.png)

#### 2. 手动上滑触发视频请求接口
emsp; 自动化滑动刷新有尝试过，但是由于技术有限，不能实现抖音APP的登录，所以用Charles只能获取视频下载链接，而不能获取其他有效信息，比如视频的名称、作者名称、获赞数、转发量等。

#### 3. Python脚本获取视频信息
emsp; 使用Python脚本拦截response爬取视频信息并下载视频，同时将视频信息存储至JSON。

#### 4. 视频无水印
&emsp; 如图：

![video_demo](https://github.com/Northxw/Python3_WebSpider/blob/master/10-DouYin/plates/video_demo.gif)

# Other
&emsp; 获取的数据不能直接存储至MongoDB等数据库，具体原因尚不清楚，若您知道，请提交issuse。

# Demo Of Screenshot
#### 1.JSON
![json_result](https://github.com/Northxw/Python3_WebSpider/blob/master/10-DouYin/plates/video_info_json.png)

#### 2.VIDEO
![video_screenshot](https://github.com/Northxw/Python3_WebSpider/blob/master/10-DouYin/plates/video_screentshot.png)

#### 3.Demo
![gif_show](https://github.com/Northxw/Python3_WebSpider/blob/master/10-DouYin/plates/demo.gif)
