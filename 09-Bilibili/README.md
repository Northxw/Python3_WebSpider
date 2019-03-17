# Project name
&emsp; 使用Selenium模拟登录B站并破解滑动验证码。

# Sort
&emsp; **验证码识别** - 破解滑动验证码

# Install
**1. Selenium** - 建议使用低版本的Python-Selenium库，因为高版本在Chrome中不支持。
```
pip3 install selenium==2.48.0
```
**2. chromedriver.exe** - download_addr：http://npm.taobao.org/mirrors/chromedriver/, 版本要匹配。

# Process analysis
**1.验证码节点**
> B站验证码只要鼠标悬浮滑块就会出现, 当验证码出现后定位节点即可。过程比较繁琐，直接贴出来：
```
img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'gt_box')))
```

**2.获取坐标值**
> 获取的坐标值分别是左上角和右下角, 而前端页面的坐标原点在屏幕左上角并且元素节点一般都是相对位置，所以坐标值部分需要好好理解。比如B站登录界面包含"登录"的div节点其父节点是id=" login-app"的div,如图：

![location_demo](https://github.com/Northxw/Python3_WebSpider/blob/master/09-Bilibili/require/demo_location.png)

**3.缺口偏移量**
> 通过遍历图片的每个坐标点获取两张图片对应像素点的RGB，如果RGB差距在阈值范围内就认为相同，继续比对下一像素点。如果超过阈值，则说明像素点不同，当前位置
即为缺口位置。
```
    def get_gap(self, image1, image2):
        """
        获取缺口偏移量
        :param image1: 不带缺口的图片
        :param image2: 带缺口的图片
        :return: None
        """
        left = 60
        # 遍历两张图片的每个像素并判断同一位置像素是否相同,不相同的像素点即缺口位置
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                if not self.is_pixel_equal(image1, image2, i, j):
                    left = i
                    return left
        return left

    def is_pixel_equal(self, image1, image2, x, y):
        """
        判断像素是否相同
        :param image1: 极验原图
        :param image2: 缺口图片
        :param x: 位置X
        :param y: 位置Y
        :return: 像素是否相同
        """
        # 取两个图片的像素点
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        # 阈值60
        threshold = 60
        # 比较RGB的绝对值是否小于阈值60,如果在阈值内则相同,反之不同
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False
```
**4.模拟拖动**
> 模拟拖动滑块继承崔大模拟人类行为轨迹的"前段匀加速后段匀减速"。

**5.点按滑块呼出验证码**
> 点按滑块后, 两到三秒后验证码会自动隐藏, 所以不要添加延时，直接获取。

# Other
&emsp; 代码已更新, 正常情况下的破解率应该在50%以上, 主要看服务器怎么判定边界(像素差)。

# Demo
![demo](https://github.com/Northxw/Python3_WebSpider/blob/master/09-Bilibili/require/demo.gif)
