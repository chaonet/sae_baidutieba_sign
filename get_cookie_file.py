#!/usr/bin/env python
# coding: utf-8

import os, sys

import urllib
import urllib2
import cookielib
import rea
import hashlib
import json
import threading
import platform
import time

import ConfigParser

defaultencoding = 'utf-8'

if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

system_env = True

user = ""
password = ""

cookie_get = ""
BDUSS = ""

if os.path.exists('conf.ini'):
    cf = ConfigParser.ConfigParser()
    cf.read('conf.ini')
    user = cf.get('main', 'username')
    password = cf.get('main', 'password')
else:
    user = os.environ.get("username")
    password = os.environ.get("password")

TOKEN = ""
TOKEN_URL = "http://passport.baidu.com/v2/api/?getapi&tpl=pp&apiver=v3"

INDEX_URL = "http://www.baidu.com/"
LOGIN_URL = "https://passport.baidu.com/v2/api/?login"

loginHeaders = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding":"gzip,deflate,sdch",
    "Accept-Language":"en-US,en;q=0.8,zh;q=0.6",
    "Host":"passport.baidu.com",
    'Upgrade-Insecure-Requests':'1',
    "Origin":"http://www.baidu.com",
    "Referer":"http://www.baidu.com/",
    'User-agent':'Mozilla/5.0 (SymbianOS/9.3; Series60/3.2 NokiaE72-1/021.021; Profile/MIDP-2.1 Configuration/CLDC-1.1 ) AppleWebKit/525 (KHTML, like Gecko) Version/3.0 BrowserNG/7.1.16352'
}
# "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36"


bdData = {
    "staticpage":"https://passport.baidu.com/static/passpc-account/html/V3Jump.html",
    "token":"",
    "tpl":"pp",
    "username":user,
    "password":password,
    "loginmerge":"true",
    "mem_pass":"on",
    "logintype":"basicLogin",
    "logLoginType":"pc_loginBasic",
}


def get_cookie_and_bduss():
    global cookie_get,BDUSS
    success = False
    filename = 'cookie.txt'
    cookie = cookielib.MozillaCookieJar(filename)
    n = 1

    while not success and n < 2:
        # cookie = cookielib.CookieJar()
        # cookie = cookielib.MozillaCookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (SymbianOS/9.3; Series60/3.2 NokiaE72-1/021.021; Profile/MIDP-2.1 Configuration/CLDC-1.1 ) AppleWebKit/525 (KHTML, like Gecko) Version/3.0 BrowserNG/7.1.16352')]

        #get TOKEN
        print("Loading...正在获取token:")
        #try:
        data = opener.open(INDEX_URL).read() # 正常获取
        # print data, 0
        data = opener.open(TOKEN_URL).read() # 获取的是错误页面`http://www.baidu.com/search/error.html`
        # print data,1
        
        print type(data)
        "<type 'str'>"
        data = eval(data)
        # print data,2
        print data["data"]["token"]
        TOKEN = data["data"]["token"]
        
        # print re.compile("\"token\"\s+:\s+\"(\w+)\"").findall(str(data))
        # TOKEN = re.compile("\"token\"\s+:\s+\"(\w+)\"").findall(str(data))[0]
        bdData["token"] = TOKEN
        print("token获取成功:" + TOKEN)
        #except:
            #print("网络问题 无法为您获取token,正在退出...")
            #return
        #login
        data = urllib.urlencode(bdData)
        request = urllib2.Request(LOGIN_URL, headers=loginHeaders, data=data)
        # request = urllib2.Request(LOGIN_URL, data=data)
        # request = urllib2.Request(LOGIN_URL, headers=loginHeaders, data=urllib.urlencode(bdData).encode('utf-8'))
        
        print "正在为 %s 进行登录操作" % user
        #try:
        # result = opener.open(request).read()
        result = opener.open(request)
        print result,3
        # <addinfourl at 4354171608 whose fp = <socket._fileobject object at 0x1038540d0>> 3
        # result = json.loads(opener.open("http://tieba.baidu.com/f/user/json_userinfo").read().decode("utf-8"))
        # result = json.loads(opener.open("http://tieba.baidu.com/f/user/json_userinfo").read().decode("ISO-8859-1"))
        cookiesToCheck_dir = {'BDUSS':'', 'PTOKEN':'', 'STOKEN':'', 'SAVEUSERID':''}
        cookiesToCheck_list = ['BDUSS', 'PTOKEN', 'STOKEN', 'SAVEUSERID']
        # print cookie, 4
        success = True
        for ck in cookiesToCheck_list:
            for ck_1 in cookie:
                if ck_1.name == ck:
                    cookiesToCheck_dir[ck] = True
        for ck in cookiesToCheck_list:
            if not cookiesToCheck_dir[ck]:
                success = False


        # print cookie
    for ck in cookie:
        if ck.name == 'BDUSS':
            BDUSS = ck.value 
            # print BDUSS
            cookie_get = cookie

    if not cookie_get or not BDUSS:
        success = False
    
    if success:
        print user + "登录成功!"
        cookie.save(ignore_discard=True, ignore_expires=True)
    else:
        print user + "登录失败，检查用户名和密码!"
        n += 1
    print cookie_get
    print BDUSS
    # return cookie,BDUSS

get_cookie_and_bduss()

