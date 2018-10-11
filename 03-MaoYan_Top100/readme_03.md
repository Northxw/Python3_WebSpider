### 1.目标
&emsp; 提取猫眼电影排行TOP100的电影名称、时间、评分、图片等信息，提取站点的URL为[猫眼电影排行首页](http://maoyan.com/board/4)，提取的结果以文本格式保存

### 2.准备
+ 正确安装requests库和re库, 验证安装成功
+ Json库主要用来将字典序列化(json.dumps)，这是自带库，无须pip安装

### 3.抓取分析
&emsp; 打开目标站点，可以看到榜单信息，如图：
![1](https://qiniu.cuiqingcai.com/wp-content/uploads/2018/02/3-11.jpg)
排名第一的电影依旧是霸王别姬，页面中显示的有效信息有影片名称、主演、上映时间、上映地区、评分、图片等信息。   
&emsp; 翻页规律：滚动页面到对下方，点击下一页，观页面的URL和内容发生的变化，如图：
![2](https://qiniu.cuiqingcai.com/wp-content/uploads/2018/02/3-12.jpg)
可以发现页面的URL变成http://maoyan.com/board/4?offset=10，比之前的URL多了一个参数，那就是offset=10，而目前显示的结果是排行11-20名的电影，初步推断这是一个偏移量的参数。再点击下一页，发现页面的URL变成了http://maoyan.com/board/4?offset=20，参数offset变成了20，而显示的结果是排行21~30的电影  
&emsp; 由此可以总结出规律，offset代表偏移量值，如果偏移量为n，则显示的电影序号就是n+1到n+10，每页显示10个。所以，如果想获取TOP100电影，只需要分开请求10次，而10次的offset参数分别设置为0、10、20、…90即可，这样获取不同的页面之后，再用正则表达式提取出相关信息，就可以得到TOP100的所有电影信息了。

### 4.其他
+ 目标信息采用正则匹配（当然，你完全可以利用其他方法，例如xpath,pyquery,css等）
+ 网页的真实源码建议在（谷歌）浏览器的开发者模式下的Network监听组件中查看
+ 写入文件的时候为了保证输出结果是中文形式而不是Unicode编码，需要将open的encoding参数设置为"utf-8"，然后在 f.write 时添加 ensure_ascii 参数并设置为False
+ 猫眼反爬虽然不是很明显，但还是建议设置延时爬取

### 5.结果
![3](https://qiniu.cuiqingcai.com/wp-content/uploads/2018/02/3-15.jpg)