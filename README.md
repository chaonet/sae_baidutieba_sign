## 百度贴吧自动签到_SAE 版本

## 功能

之前做了一个[百度贴吧自动签到](https://github.com/chaonet/baidu_tieba_auto_sign)，但每天手动重复运行也麻烦，于是想到用`SAE`。

部署到 SAE，使用`计划任务服务`，每天 0 点和 1 点 自动运行，可以参考[Cron](http://www.sinacloud.com/doc/sae/python/cron.html)

## 开发环境

```
Python 2.7.9
Mac os 10.10.5
virtualenv 13.1.2
pip 8.0.2
```

## 环境配置

```
# 下载源码
git clone git@github.com:chaonet/sae_baidutieba_sign.git
# 或者通过 HTTPS 下载:
git clone https://github.com/chaonet/sae_baidutieba_sign.git

cd sae_baidutieba_sign

# 安装依赖
virtualenv env/
. ./env/bin/activate
pip install -r requirements.txt
```

## 准备

注册[新浪云账号](http://www.sinacloud.com/home/index/faq_detail/doc_id/19.html)，需要通过微博账号登陆，所以，还要注册一个微博……

创建一个`云应用 SAE`，填写`二级域名`，也就是`App name`，输入`应用名称`，运行环境选择`Python 2.7`，代码管理方式使用`git`而不是`svn`

## 使用

- 设置账号、密码

创建`conf.ini`文件，用于保存 百度 账号、密码，以便脚本运行时读取

内容：

```
[main]
username=账号
password=密码
```

或者

在系统的环境变量中设置，方法略……

- 生成`cookie.txt`文件

`python get_cookie_file.py`

- 部署到 SAE

在你应用的git代码目录里，添加一个新的git远程仓库 sae

```
$ git remote add sae https://git.sinacloud.com/应用的二级域名(App name)
```

编辑代码并将代码部署到 `sae` 的版本1。

```
$ git add .
$ git commit -am "make it better"
$ git push sae master:1
```

## change logs

将应用代码放入`index.wsgi`，并在`config.yaml`中完成应用信息配置和`cron`任务

将第三方依赖导入`vendor`目录

安装本地 sae 测试环境`sae-python-dev-guide`

本地测试运行正常，但部署到`SAE`后，获取`token`失败

经过测试，在`SAE`上运行，可以打开`http://www.baidu.com/`，无法获取`https://passport.baidu.com/v2/api/?getapi&tpl=pp&apiver=v3`，返回的是`http://www.baidu.com/search/error.html`

于是，考虑先本地获取并保存`cookie`到应用目录，然后在线上环境加载`cookie`。

成功

在 0 点执行，会出现部分贴吧签到失败的情况，于是添加一个 1 点执行的任务，再次执行签到，避免遗漏

学了一遍 python 爬虫 的知识

