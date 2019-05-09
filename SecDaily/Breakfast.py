#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
@author: d00ms(--)
@file: MorningPaper.py
@time: 2019-5-9 9:59
@desc: 如梦地迷恋你一场
@func: 从 先知、安全客、嘶吼、freebuf 四大平台上爬取当日的新文章
'''

# 概要：访问阿里云先知平台，并抄录当日发布的新文章
# xpath语法技巧：[]内代表判断条件，@代表节点属性
# 写Xpath最简单的办法是用Chrome浏览器的右键功能^_^

# author: lilinfeng
# function: search xz.aliyun.com for everyday udpates!

import requests
import datetime
from lxml import etree

target = "https://xz.aliyun.com"
scope = list()
now = datetime.datetime.now()
week = now.strftime("%a")
scope.append(now.strftime("%Y-%m-%d"))
# 如果今天是周一，则顺便爬取上周末的文章
if week == "Mon":
    last =  now - datetime.timedelta(days=1)
    scope.append(last.strftime("%Y-%m-%d"))
    last =  now - datetime.timedelta(days=2)
    scope.append(last.strftime("%Y-%m-%d"))

header = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/72.0.3626.121 Safari/537.36",
    "Accept":"text/html,application/xhtml+xml,application/xml",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }
proxy= {"https":"http://127.0.0.1:8080"}
repl = requests.get(target, headers=header, verify=False)

print(repl.status_code)
print("---------------")

docs= etree.HTML(repl.content.decode(repl.encoding))

# some xpath expression to locate your elements
# but firstly, we construct an Article class

class Aritcle:
    def __init__(self,t,h,a,c,d):
        self._title= t
        self._href= h
        self._author= a
        self._type= c
        self._date= d

    def __repr__(self):
        return """Post informaiton:
            Title:{} 
            Author:{} Type:{} Date:{} Link: {}
        """.format(self._title,self._author,self._type,self._date,self._href)

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

