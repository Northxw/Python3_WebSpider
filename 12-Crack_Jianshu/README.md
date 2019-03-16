## Project name
&emsp; 使用Selenium模拟登录网页版简书并识别点触式验证码。

## Sort
&emsp;  **验证码识别** - 点触验证码

## Demand
**1. Selenium** - 建议使用低版本的Python-Selenium库，因为高版本在Chrome中不支持。
```
pip3 install selenium==2.48.0
```
**2. chromedriver.exe** - download_addr：http://npm.taobao.org/mirrors/chromedriver/, 版本要匹配。  

**3. Chaojiying_Python.rar** - download_addr：http://www.chaojiying.com/download/Chaojiying_Python.rar

## Process analysis
**1.不要频繁运行程序模拟登录**
> 频繁模拟登录并识别验证码后，会出现验证码却来越模糊到难以识别，并且识别后点击"确认"按钮无法登录（或者说登录失败）的情况。如图所示的位置失效：

![sure_button](https://github.com/Northxw/Python3_WebSpider/blob/master/12-Crack_Jianshu/require/code_demo.png)

**2.超级鹰**
> [超级鹰打码平台](http://www.chaojiying.com/) 打码效率可以达到90%以上。在平台上注册绑定微信后会赠送1000积分，基本够用了。如图是我的积分情况：

![jifen](https://github.com/Northxw/Python3_WebSpider/blob/master/12-Crack_Jianshu/require/chaojiying.png)

**3.超级鹰软件ID和验证码类型**
> 软件ID相当于发给你身份证，每次打码都必须携带；验证码类型需要你去 [平台](http://www.chaojiying.com/price.html#table-item5) 确认。例如该项目的简书
验证码类型属于**9004	坐标多选,返回1~4个坐标**。

**4.识别思路(简要)**
> 首先，获取验证码位置；然后，获取验证码图像并发送给超级鹰打码平台；最后，转化识别结果并使用Selenium点击登录即可。

## Other
&emsp; 代码中pass留空函数为预留功能：爬取简书文章信息。有兴趣可以继续完善。

## Demo
![demo](https://github.com/Northxw/Python3_WebSpider/blob/master/12-Crack_Jianshu/require/demo.gif)
