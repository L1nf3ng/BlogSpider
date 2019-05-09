#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@author: 如梦地迷恋你一场
@file: MorningPaper.py
@time: 2019-5-9 9:59
@desc: 从 先知、安全客、嘶吼、freebuf 四大平台上爬取当日的新文章
"""


# 小技巧：
# xpath语法技巧：[]内代表判断条件，@代表节点属性
# 写Xpath最简单的办法是用Chrome浏览器的右键功能^_^


import requests
import datetime
from lxml import etree


# 以下是一些会用到的结构

# 文章类，记录标题、链接、作者、分类、发布日期等重要信息
class Aritcle:
    def __init__(self,title, link, author, category, date):
        self._title= title
        self._href= link
        self._author= author
        self._type= category
        self._date= date

    # 输出函数，要么重载，要么自写。输出格式到文件，按模板形式输出为html、csv等
    def __repr__(self):
        return """\
            Post informaiton:
            Title:{} 
            Author:{} Type:{} Date:{} Link: {}
        """.format(self._title,self._author,self._type,self._date,self._href)


# 目标类，记录目标的爬取指标：链接、解析时的xpath语法
class Target:
    def __init__(self, url, xpath):
        self._url = url
        self._expr = xpath

    @property
    def url(self):
        return self._url

    @property
    def expr(self):
        return self._expr


# 收集器类，负责测试连接、请求、解析文档、处理异常等
class Collector:
    def __init__(self, target, proxy= False):
        self._target = target
        self._headers = { "User-Agent":"Mozilla/5.0 Chrome/72.0.3626.121 Safari/537.36",
                          "Accept":"text/html,application/xhtml+xml,application/xml",
                          "Accept-Encoding": "gzip, deflate, br",
                          "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8" }
        self._proxy = {"https":"http://127.0.0.1:8080"}
        # set_proxy label shows whether turn on the proxy
        self._set_proxy = proxy
        # default charset is utf-8
        self._charset = 'utf-8'

    def get_blog(self):
        if self._set_proxy:
            reply = requests.get(self._target.url, headers= self._headers, proxies= self._proxy)
        else:
            reply = requests.get(self._target.url, headers=self._headers)
        if reply.status_code != 200:
            print('Cannot connect {} just now. Try it later or check the network...'.format(self._target.url))
            return None
        


target = "https://xz.aliyun.com"
scope = []
now = datetime.datetime.now()
week = now.strftime("%a")
scope.append(now.strftime("%Y-%m-%d"))
# 如果今天是周一，则顺便爬取上周末的文章
if week == "Mon":
    last =  now - datetime.timedelta(days=1)
    scope.append(last.strftime("%Y-%m-%d"))
    last =  now - datetime.timedelta(days=2)
    scope.append(last.strftime("%Y-%m-%d"))


repl = requests.get(target, headers=header, verify=False)

print(repl.status_code)
print("---------------")

docs= etree.HTML(repl.content.decode(repl.encoding))

# some xpath expression to locate your elements


# 1st expression, get the post lists
articles = docs.xpath("//td")
Today_Articles = list()

# 2nd expression, get detailed information by class
for element in articles:
    title = element.xpath("./p[1]/a[@class='topic-title']")[0].text
    title = title.strip('\r\n').strip()
    href = target + element.xpath("./p[1]/a[@class='topic-title']/@href")[0]
    author = element.xpath("./p[2]/a[1]")[0].text
    type = element.xpath("./p[2]/a[2]")[0].text
    date = element.xpath("./p[2]/text()")[2]
    date = date.strip('\r').strip('\n').strip(' /').strip()

    # very simple logics
    for day in scope:
        if day == date:
            Today_Articles.append(Aritcle(title,href,author,type,date))

if len(Today_Articles)==0:
    print("今天还没更新，半小时后再来")
else:
    for element in Today_Articles:
        print(element)

