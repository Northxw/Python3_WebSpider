## Project name
&emsp; 模拟登录网易163邮箱并发送SOS邮件。

## Purpose
&emsp; Selenium打开站点默认父级Frame, 获取不到子页面的节点。项目可以训练对iframe的处理。

## Install
&emsp; 基于自动化测试工具Selenium的模拟登录并发送SOS邮件，需要安装的库：

**1. Selenium** - 建议使用低版本的Python-Selenium库，因为高版本在Chrome中不支持。
```
pip3 install selenium==2.48.0
```
**2. chromedriver.exe** - 下载地址：http://npm.taobao.org/mirrors/chromedriver/, 版本要匹配。将 .exe 程序放在"..Python\Python36\Scripts"目录下。   

**3. pymysql**
```
pip3 install pymysql
```

## Process analysis
 **1.登录界面iframe**   
> iframe的id值添加了时间戳,直接获取相对麻烦。可通过XPATH或CSS选择器获取该节点。如图：    


![login_frame](https://github.com/Northxw/Python3_WebSpider/blob/master/20-Selenium_163/require/login_frame.png)

**2. "写信"节点**
> 写信节点的元素定位li节点, 不要定位span子节点，否则获取不到。另外，如果是获取APP节点，可以选择小一级的。    

**3. 邮件主题**
> 主题节点不可交互，无法输入文字，这里选择不设置。    

**4. 邮件内容**
> 邮件内容的文本输入框处于iframe中，输入文本前需要切换frame，可直接通过class获取并切换。如图：    

![content_frame](https://github.com/Northxw/Python3_WebSpider/blob/master/20-Selenium_163/require/content_frame.png)

**5. "发送"节点**
> 由于输入邮件内容时切换至子页面，在点击发送前需要切换到父级Frame。

**6. 登录限制**
> 不要频繁使用Selenium, 否则会出现点触式验证。当然，完全可以破解。但是，网易相对友好，短时间过后便可恢复正常访问，也不会ban IP。

## Demo
![demo](https://github.com/Northxw/Python3_WebSpider/blob/master/20-Selenium_163/require/demo.gif)
