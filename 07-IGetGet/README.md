# Project Name
&emsp; **IGetGet**，使用 Mitmproxy 的 Mitmdump 组件爬取"得到"App的电子书信息,并将信息存储至Json文件。

# Sort
&emsp; **非自动化爬取App数据** - 通过Python脚本捕获服务器返回的response并处理。

# Demand
**1. Charles** - 跨平台支持度很好的网络抓包工具。addr: https://www.charlesproxy.com/download/

**2. mitmproxy** - 一个支持HTTP、HTTPS的抓包程序，类似Fiddler、Charles的功能, 通过控制台的形式操作。
```
pip3 install mitmproxy
```

# Process analysis
#### 1.Charles证书安装
> 不同OS安装过程基本一致。打开Charles, 点击"Help->SSL Proxy->Install Charles Root Certificate"，即可进入证书安装页面。如图：    

![CA](https://github.com/Northxw/Python3_WebSpider/blob/master/07-IGetGet/utils/charles%E5%AE%89%E8%A3%85%E8%AF%81%E4%B9%A6%E9%A1%B5%E9%9D%A2.png)

> 具体的证书安装过程请自行谷歌。

#### 2.手机证书安装
> **前提：**确保Charles的HTTP代理开启，默认端口8888。然后将手机和电脑连接再同一个局域网下。如图：

> 然后，在手机浏览器上打开 chls.pro/ssl,  即可自动安装（安卓尽量使用本机自带浏览器）

#### 3.mitmproxy证书安装的Bug
> PC端证书安装请自行谷歌。安装结束后可在用户目录的.mitmproxy目录下找到CA证书，如图：

> 手机安装此证书不要局限于"mitmproxy-ca-cert.pem", 可能无法识别为CA证书并安装。可以尝试将上图中1-5中的任何一个传输到手机安装测试，哪个能用即用哪个。

#### 4.数据库存储失败
> 测试期间，若添加数据库的插入操作，命令行就不会显示数据并且手机端网络丢失（当前局域网没有任何出错）；而注释掉数据库插入操作，即可正常显示。具体原因尚不清楚，目前暂时将数据存储至Json。 错误如图：

# Other
&emsp; 目前的遗留问题是数据库存储，还没有一个切实可行的解决方案。有知道的可以提交issue。

# Demo
#### 1.JSON

#### 2.Run Screenshot
