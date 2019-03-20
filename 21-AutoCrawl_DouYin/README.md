# Project Name
&emsp; Appium、Mitmdump爬取抖音短视频。

# Sort
&emsp; **自动化爬取APP数据** - 基于 Appium + Mitmdump 的自动化爬取程序。

# Install
&emsp; 请移步：[Environmental_installation](https://github.com/Northxw/Python3_WebSpider/blob/master/05-Moments/Readme.md)

# Explain
### 1. 不登录抖音账号
&emsp; 若选择登录抖音账号，第一个问题是无法自动化获取短信验证码，第二个问题是填写短信验证码后会出现点触式图形验证码，如图：

![yanzhengma](https://github.com/Northxw/Python3_WebSpider/blob/master/21-AutoCrawl_DouYin/plates/%E5%9B%BE%E5%BD%A2%E7%82%B9%E8%A7%A6%E9%AA%8C%E8%AF%81%E7%A0%81.png)

### 2.跳过"滑动查看更多"
&emsp; 自动化打开抖音APP后会出现"滑动查看更多", 须通过获取点击位置跳过该页面，如图：

![scroll_and_more](https://github.com/Northxw/Python3_WebSpider/blob/master/21-AutoCrawl_DouYin/plates/start.png)

### 3. 视频请求接口
&emsp; 抖音视频的接口较多，有的包含较多广告，有的全是短视频，这里选择全部获取，构造共16个URL，代码如下：
```
nums = [1,3,6,9]
    for num in nums:
        url_first = 'http://v{}-dy.ixigua.com/'.format(str(num))
        url_second = 'http://v{}-dy-x.ixigua.com'.format(str(num))
        url_third = 'http://v{}-dy-z.ixigua.com'.format(str(num))
        url_fouth = 'http://v{}-dy-y.ixigua.com'.format(str(num))
        urls.extend([url_first, url_second, url_third, url_fouth])
```

### 4. 视频文件名称
&emsp; 取视频URL中的唯一值作为保存视频的名称，如图：

![file_name](https://github.com/Northxw/Python3_WebSpider/blob/master/21-AutoCrawl_DouYin/plates/video_url.png)

# Other
&emsp; 自动化爬取抖音短视频只能下载视频，而不能获取视频的其他有效信息，就好比有些网站必须登录之后才能获取数据是一样的。

# Demo
#### 1. GIF-Download_Video
![download](https://github.com/Northxw/Python3_WebSpider/blob/master/21-AutoCrawl_DouYin/plates/douyin_demo.gif)

#### 2. GIF-Crawl_Video
![crawl](https://github.com/Northxw/Python3_WebSpider/blob/master/21-AutoCrawl_DouYin/plates/demo.gif)
