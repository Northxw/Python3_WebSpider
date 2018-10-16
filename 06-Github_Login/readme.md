### 目标
&emsp; 模拟登录Github，并获取登录后才可以访问的页面信息，比如好友动态、个人信息等内容   

### 分析
&emsp; *仅简单叙述分析过程的难点, 原因：模拟登录Github的分析过程较为简单，多尝试即可*
+ 清除浏览器(Chrome)中Git站点的Cookies： [清除方法](https://blog.csdn.net/panbiao1999/article/details/77880649)
+ 设置Coiokies的过程发生在访问登录界面的过程（可在开发者工具中查看访问登录界面的数据请求信息）
+ Form表单的authenticity_token参数可能隐藏在其他地方或者通过计算获得。对于Github而言，可在[登录界面](https://github.com/login)的源码中找到   

&emsp; 通过上述分析, 可以获取到所有信息，即可实现模拟登录, 然后获取所需的数据

### 存在问题
&emsp; 有一点不解, 包含动态信息的所有div节点无法一次性获取（xpath是手写的）, 代码应该是没有问题。后期再回头看，尽快修改不足之处