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
#### 1.Charles证书配置
> 不同OS安装过程基本一致。打开Charles, 点击"Help->SSL Proxy->Install Charles Root Certificate"，即可进入证书安装页面。如图：
