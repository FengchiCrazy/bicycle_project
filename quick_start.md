#  自行车项目快速入门

本文档是为了帮助您从服务器hive上快速上手获得数据。至于进一步的分析，您可以自行定制需要的数据，清洗数据之后建模分析。

涉及到的软件有：Xshell, Linux的一些初级指令, Hive。

## 1. Xshell

### 1.1 Xshell 简介

由于我们的数据存储在服务器上的，要从本地访问的话需要借助一定的工具。Xshell 是一个终端模拟软件，它的作用在于在本地电脑远程登服务器。当然还有很多的同类的产品，比如SecureCRT等。甚至还可以通过本地的ssh命令实现登录。他们的最终效果都是一样的，就是登录远程服务器后进行操作。这里我们只选择Xshell进行介绍。

### 1.2 Xshell 下载与安装

搜索引擎搜索Xshell，可以得到Xshell的[下载页面](http://www.netsarang.com/download/down_xsh.html)选择下方的下载链接后，可以进入正式的下载页面。

正式的下载页面中会有两个选择：`Evaluation user / Home & School user` 以及 `Existing customer`。Xshell对家庭和学校客户是免费的，只需选择上面一项，将License type 修改为`Home and School use`即可。填写带星号的必填项之后，选择提交。如下图所示：

![download](./img/download1.png)

*Notice:* Email地址为接收下载链接地址，请务必正确填写。网页上提到qq.com和163.com,126.com的邮箱可能会出现接收不到邮件的问题。我用的是163的邮箱，并没有出现什么问题。大家如果没有接收到邮件，不妨换一个邮箱试试看。

登录刚才填写的email地址可以找到一个下载页面的连接，点击即可完成下载。

安装Xshell比较简单，像所有windows程序安装一样，比较傻瓜化，这里就不多介绍了。注意有一个页面要选择Home & School use即可。

### 1.3 配置Xshell连接服务器

安装完成后打开Xshell，会弹出一个会话窗口，点击左上角新建。如果没有弹出也不要紧，在左上角文件菜单中也可以找到新建。

