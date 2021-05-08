
<div align="center"> 
<h1 align="center">
xsyu-wzxy-sign
</h1>
</div>

## 🌀简介
本项目可以实现“我在校园”微信小程序每日晨午检和晚签到自动打卡，本项目中配置的各项参数仅适用于西安石油大学（鄠邑校区）。每个学校的程序配置不一致，其他学校根据情况自行修改代码中的参数测试运行即可

 > 注意：由于小程序限制token有效期为四天，请注意时间及时更换token，否则打卡失败


## 💡特性

- [x] **自动签到**  程序会在每天6点、11点、22点自动执行打卡和签到流程(可能存在延迟)，也可以随时通过部署教程的`步骤4`手动触发，具体时间参照[此处](.github/workflows/main.yml)
- [x] **支持订阅**  通过配置`SCKEY`开启订阅，每此执行打卡或签到后将签到结果推送到微信上
- [x] **无需服务器**  通过github Action定时任务，不需要自己部署服务器即可定时执行

## 📐部署

<details>
<summary>查看教程</summary>

### 1. Fork 仓库

- 项目地址：[github/xsyu-wzxy-sign](https://github.com/Liuism/xsyu-wzxy-sign)
- 点击右上角`Fork`到自己的账号下

> ![fork](https://i.loli.net/2020/10/28/qpXowZmIWeEUyrJ.png)

### 2. 获取 token

抓包教程为利用Fiddler抓包配置教程

参考文章：
https://blog.csdn.net/fajing_feiyue/article/details/111569537


#### 2.1、下载Fiddler

下载最新版fiddler ，可以在官网下载：https://www.telerik.com/download/fiddler

百度云链接：链接：https://pan.baidu.com/s/1LqqJCMlBfQgB5C0_lU4r8g 提取码：whyi 


#### 2.2、安装及配置Fidder

 ① 正常安装，下一步，下一步，可以修改软件安装地址，安装完毕后，打开软件。按下图图进行配置勾选

![Fiddler01.png](https://upload-images.jianshu.io/upload_images/14926374-b6432d6c9fffa9ce.png)

![Fiddler02.png](https://upload-images.jianshu.io/upload_images/14926374-0fc4c65359a1d77d.png)

![Fiddler03.png](https://upload-images.jianshu.io/upload_images/14926374-24794af241fd5afa.png)

**下面两个图是配置证书，如果之前没有自动弹出来的话，最好手动配置一下，否则无法抓包https请求**

![Fiddler04.png](https://img-blog.csdnimg.cn/2020122300105644.png)

![Fiddler05.png](https://img-blog.csdnimg.cn/20201223000546457.png)

配置操作完毕后重启Fiddler


 ② 重新打开fiddler，就可以在电脑上进行https抓包了。如果不成功请看参考文章解决

![20201202170319](https://img-blog.csdnimg.cn/20201223001229945.png)

#### 2.3、获取token值

登录电脑端微信，打开我在校园日检日报  
留意最下方出现的 `student.wozaixiaoyuan.com` 双击打开  

![20201202170352](http://img.chaney.top/img/20201202170352.png)

出现的这一串token字符串值就是我们需要的了，第一步任务已经实现。如果后续登录失效了，重新抓包获取这个值即可，如果不出现特殊情况这个登录能保持四天左右。

![20201202095745](http://img.chaney.top/img/20201202095745.png)


### 3. 添加 token 至 Secrets

- 回到项目页面，依次点击`Settings`-->`Secrets`-->`New secret`

> ![new-secret.png](https://i.loli.net/2020/10/28/sxTuBFtRvzSgUaA.png)

- 建立名为`TOKEN`的 secret，值为`步骤2.3`中获取的`token`内容，最后点击`Add secret`

- secret 名字必须为`TOKEN`！

> ![add-secret](https://i.loli.net/2020/10/28/sETkVdmrNcCUpgq.png)

### 4. 启用 Actions

> Actions 默认为关闭状态，Fork 之后需要手动执行一次，若成功运行其才会激活。

返回项目主页面，点击上方的`Actions`，再点击左侧的`xsyu-wzxy-sign`，再点击`Run workflow`
    
> ![run](https://i.loli.net/2020/10/28/5ylvgdYf9BDMqAH.png)

</details>

至此，部署完毕。

## 🔍结果

当你完成上述流程，可以在`Actions`页面点击`xsyu-wzxy-sign`-->`build`-->`Run sign`查看结果。

<details>
<summary>查看结果</summary>

无论成功或失败都会输出相应的信息：
```
2021-03-05T03:24:21 INFO 自动打卡签到结果 : code = 0
2021-03-05T03:24:22 INFO 推送消息成功: {"errno":0,"errmsg":"success","dataset":"done"}
```

如果失败，你还会收到一封来自GitHub、标题为`Run failed: xsyu-wzxy-sign - master`的邮件。

</details>

## 🔔订阅

若开启订阅推送，无论成功与否，都会收到微信通知。

- 使用 GitHub 登录 [sc.ftqq.com](http://sc.ftqq.com/?c=github&a=login) 创建账号
- 点击「[发送消息](http://sc.ftqq.com/?c=code)」，获取`SCKEY`
- 点击「[微信推送](http://sc.ftqq.com/?c=wechat&a=bind)」，完成微信绑定
- 建立名为`SCKEY`的 secret，并添加获取的 SCKEY 值，开启订阅推送

## ❗️协议

使用 xsyu-wzxy-sign 即表明，您知情并同意：

- 本项目初衷是为经常忘记打卡或懒人提供方便，请勿使用本项目进行上报虚假定位信息等违规操作
- 由于使用本项目造成的一切后果，包括但不限于 打卡执行失败、被学校请去喝茶等，概不负责
