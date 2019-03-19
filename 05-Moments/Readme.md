# Project Name
&emsp; Appium爬取微信朋友圈。

# Sort
&emsp; **自动化爬取App数据** - 基移动端的自动化测试工具Appium的自动化爬取程序。

# Install
**1.JDK** - [Download JDK](https://www.oracle.com/technetwork/java/javase/downloads/jdk11-downloads-5066655.html)，Appium要求用户必须配置JAVA环境, 否则启动Seesion报错。

**2.Appium** - [Download Appium](https://github.com/appium/appium-desktop/releases), 安装过程请自行搜索。

**3.Android SDK** - [Download SDK](https://developer.android.com/studio/index.html?hl=zh-cn)

**4. Selenium** - 建议使用低版本的Python Selenium库，在Chrome高版本可能会报错。例如：
```
pip3 install selenium==2.48.0
```
**5. chromedriver.exe** - [Download Chromedriver](http://npm.taobao.org/mirrors/chromedriver/),  确保版本要匹配, 然后将 .exe 程序放在"..Python\Python36\Scripts"目录下。

**6. pymongo**
```
pip3 install pymongo
```

**7. MongoDB Server** - [Download MongoDB](https://www.mongodb.com/)


# Explain
#### 1. 爬取思路
> 沿袭崔大的爬取思路：**模拟登录、抓取动态、保存数据**。

#### 2. Android SDK的安装与配置
> 打开Android Studio, 选择"**Configure->SDK Manager->Apperance&Behavior->System Settings->Android SDK**", 选择对应安卓机版本的SDK，如图：

![sdk](https://github.com/Northxw/Python3_WebSpider/blob/master/05-Moments/plates/SDK.png)

> 此外，还需要将SDK所在路径添加到系统环境变量中，否则报错。

#### 3. Desired Capabilites 参数
> 分别是：platfornName, deviceName, appPackage, appActivity。前两个可通过如下命令获取, 前提是连接手机、打开USB调试：
```
adb devices -l
```

![devicename](https://github.com/Northxw/Python3_WebSpider/blob/master/05-Moments/plates/device_name.png)

> 后两个参数请移步：[获取appPackage和appActivity](https://blog.csdn.net/mtbaby/article/details/78676477)

#### 4. 开启安卓的" 开发者选项、USB调试 "
> 测试之前，确保打开 **开发者选项、USB调试**。开发者模式确保调试程序在手机安装辅助软件：**Unlock, Appium Settings**；USB调试主要是利用Appium内置驱动打开APP。此外，要保持屏幕长亮。

#### 5. 节点ID或XPATH值获取
> 安卓微信节点获取，相对比较容易获取，比如获取"登录"ID值，启动Session后只需点击屏幕左侧安卓屏的登录按钮，中间就会自动定位到所在节点，最右侧还会显示该节点的所有属性。如图：

![element](https://github.com/Northxw/Python3_WebSpider/blob/master/05-Moments/plates/login.png)

> 对于文本输入框，只需要点击最右侧的"send text"即可。

#### 6. "是否匹配通讯录"
> 这里选择"否", 理由：重新登录进入微信后会自动加载本地数据，耗时较长，如果匹配通讯录好友，增加耗时，可能在TIMEOUT时间内获取不到节点，导致程序终止。我这里选择了"是", 如图：

![no](https://github.com/Northxw/Python3_WebSpider/blob/master/05-Moments/plates/yes-no.png)

#### 7. 朋友圈信息获取思路
> 获取当前显示的朋友圈每条状态对应的区块元素，遍历每个区块元素，再获取内部显示的用户名、正文、发布时间，代码如下：
```
# items存储当前页面所有发布的朋友圈信息
items = self.wait.until(
    EC.presence_of_all_elements_located(
        # 每个ej9节点对应一条朋友圈数据
        (By.XPATH, '//*[@resource-id="com.tencent.mm:id/ej9"]/android.widget.LinearLayout')))

for item in items:
    try:
        # 昵称
        nickname = item.find_element_by_id('com.tencent.mm:id/b5o').get_attribute('text')
        # 正文
        content = item.find_element_by_id('com.tencent.mm:id/ejc').get_attribute('text')
        # 日期
        date = item.find_element_by_id('com.tencent.mm:id/eec').get_attribute('text')
        # 处理日期
        date = self.processor.date(date)
        data = {
            'nickname': nickname,
            'content': content,
            'date': date,
        }

```

#### 8.日期处理
> 日期处理依旧采用崔大的实现方式，代码如下：
```
class Processor():
    def date(self, datetime):
        """
        格式化时间
        :param date: 原始时间
        :return: 处理后时间
        """
        if re.match('\d+分钟前', datetime):
            minute = re.match('(\d+)', datetime).group(1)
            datetime = time.strftime('%Y-%m-%d', time.localtime(time.time() - float(minute) * 60))
        if re.match('\d+小时前', datetime):
            hour = re.match('(\d+)', datetime).group(1)
            datetime = time.strftime('%Y-%m-%d', time.localtime(time.time() - float(hour) * 60 * 60))
        if re.match('昨天', datetime):
            datetime = time.strftime('%Y-%m-%d', time.localtime(time.time() - 24 * 60 * 60))
        if re.match('\d+天前', datetime):
            day = re.match('(\d+)', datetime).group(1)
            datetime = time.strftime('%Y-%m-%d', time.localtime((time.time()) - float(day) * 24 * 60 * 60))
        return datetime
```

# Other
&emsp; (⊙_⊙)?

# Result
![mongodb_moments](https://github.com/Northxw/Python3_WebSpider/blob/master/05-Moments/plates/moment_db.png)
