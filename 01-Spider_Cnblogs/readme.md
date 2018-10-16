### 目标
+ 博客园首页、精华、新闻页面的文章的详细信息，比如：文章标题、链接、作者主页链接，发布时间，文章简介等
+ 数据处理为TXT文本格式（后期做数据可视化分析）
+ 打包exe程序，每次运行程序，获取当天最新文章信息

### 解释
&emsp; 爬取的范围仅限于首页、精华、新闻页面。原因：仅这三个页面包含了有用的信息，其他栏目下的非目标爬取内容。

### 库的使用
+ requests
+ re
+ time
+ fake_useragent - 作用：随机更换User-Agent, 防ban;  Github地址: https://github.com/hellysmile/fake-useragent       
+ colorama  - 作用：设置字体显示的颜色(windows黑框显示不友好);  Github地址：https://github.com/tartley/colorama       
+ numba - 作用：加快程序运行速度;  Github地址: https://github.com/numba/numba      
+ tqdm - 作用：进度显示条; Github地址：https://github.com/tqdm/tqdm     

### URL分析
+ 首页：https://www.cnblogs.com/， 点击下一页，URL为：https://www.cnblogs.com/#p2。 因为翻页规律显而易见，只需要修改p后面的数字即可。
+ 精华页：https://www.cnblogs.com/pick/， 点击下一页，URL为：https://www.cnblogs.com/pick/#p2。 翻页规律同上。
+ 新闻页面：https://www.cnblogs.com/news/， 翻页规律同上。

### 其他
+ a打包用到的是pyinstaller第三方库，执行pip install pyinstaller进行安装，pyinstaller两个参数解释如下：i.<font color="#dd0000"> -F：</font>指定打包后只生成一个exe格式的文件； ii.	<font color="#dd0000"> –i：</font>改变生成程序的icon图标（图片必须是ico格式）
+ 打包命令：<font color="#dd0000">pyinstaller –F –i New.ico New.py</font>
+ 为了方便打包为exe程序，将源代码复制并重命名为了New.py，icon图标名称也是New.ico
+ 生成的 .exe 程序包含在dist文件夹下，点击运行的结果会直接创建在该目录下（三个文本文件）