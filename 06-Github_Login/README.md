## Github Login
&emsp; 模拟登录Github并抓取登录后才可以访问的页面信息, 包括好友动态、个人信息等。   

## Sort
&emsp; **模拟登陆 - requests**

## Explain
#### 1.清除Cookies
&emsp; 清除浏览器中待抓取网站的Cookies： [清除方法](https://blog.csdn.net/panbiao1999/article/details/77880649)
#### 2.浏览器设置Coookies
&emsp; 设置Cookies的过程发生在请求登录界面后(即：http://github.com/login)。
#### 3.From表单的验证参数
&emsp; Form表单的authenticity_token参数可在登陆界面的源码中获取。

