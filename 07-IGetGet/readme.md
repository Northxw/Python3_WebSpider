### 目标
&emsp; 爬取"得到"APP内电子书板块的电子书信息, 并将信息保存到MongoDB

### 准备工作
+ 确保正确安装 mitmproxy 和 mitmdump.[参考方法 !](https://yq.aliyun.com/articles/603782?utm_content=m_1000003864)
+ 手机和PC机处于同一个局域网下，并确保在手机上配置好了mitmproxy的CA证书.
+ 正确安装并启动MongoDB服务，并安装PyMongo库（pip install pymong)

### 抓取分析
+ 寻找电子书页面的URL和返回内容, 编写脚本并命名为scripts.py、如下：

```
def response(flow):
    print(flow.request.url)
    print(flow.response.text)
```
&emsp; 在命令行运行mitmdump，命令如下：

```
mitmdump -s scripts.py
```
&emsp; 手机上打开得到APP，进入电子书页面，便可以看到PC端控制台的相应输出。不断滑动更新页面，会伴随新的加载请求，包含了下一页的电子书内容。
+ 可以找到书籍列表请求的url: https://dedao.igetget.com/v3/discover/bookList.   格式化后，即可找到相应的数据段（c段,list段）
+ 编写代码抓取并保存至数据库即可.
