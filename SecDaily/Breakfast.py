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


# 首先是有用的处理函数


# 以下是一些会用到的结构
# 文章类，记录标题、链接、作者、分类、发布日期等重要信息
class Article:
    # python的特性：只能定义一个构造函数，后期可以用*args的长度改造一下
    # 构造函数改为列表初始化：[title, link, author, category, date, origin]
    def __init__(self, data):
        self._title= data[0]
        self._href= data[1]
        self._author=  data[2]
        self._type= data[3]
        self._date= data[4]
        self._origin = data[5]
        if not self._href.startswith('https://') and not self._href.startswith('http://'):
            self._href = self._origin + self._href

    # 输出函数，要么重载，要么自写。输出格式到文件，按模板形式输出为html、csv等
    def __repr__(self):
        return """Post informaiton:\nTitle:{}\n Author:{} Type:{} Date:{} Link: {}\n""".\
            format(self._title,self._author,self._type,self._date,self._href)


# 目标类，记录目标的爬取指标：链接、解析时的xpath语法
# Target中的表达式数组分别代表（post位置，标题位置、链接位置、作者位置、分类位置、日期位置）
# Target中的坏表达式列表代表要删除的节点，因为这些某些节点的存在该绕了正常的解析过程
# 所以先找到它们，并删除掉
# TODO: ！！！！注意，删除的是找到节点的父节点！！！！
class Target:
    def __init__(self, url, good_xpath, bad_xpath=None):
        self._url = url
        self._expr = []
        self._expr.extend(good_xpath)
        self._bad_expr = bad_xpath

    @property
    def url(self):
        return self._url

    @property
    def expr(self):
        return self._expr

    @property
    def bad_expr(self):
        return self._bad_expr


# 收集器类，负责测试连接、请求、解析文档、处理异常等
class Collector:
    def __init__(self, target, proxy= False):
        self._target = target
        self._headers = { "User-Agent":"Mozilla/5.0 Chrome/72.0.3626.121 Safari/537.36" }
#                          "Accept":"text/html,application/xhtml+xml,application/xml",
#                          "Accept-Encoding": "gzip, deflate, br",
#                          "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8" }
        self._proxy = {"https":"http://127.0.0.1:8080"}
        # set_proxy label shows whether turn on the proxy
        self._set_proxy = proxy
        # default charset is utf-8
        self._charset = 'utf-8'
        self._posts = []

    def get_blog(self):
        if self._set_proxy:
            reply = requests.get(self._target.url, headers= self._headers, proxies= self._proxy)
        else:
            reply = requests.get(self._target.url, headers=self._headers)
        if reply.status_code != 200:
            print('Cannot connect {} just now. Try it later or check the network...'.format(self._target.url))
            return None
        return reply.content.decode(self._charset)

    def parse_blog(self, blog):
        p = etree.HTMLParser()
        doc = etree.fromstring(blog, p)
#        doc = etree.parse(blog, p)
        # last expr defines the rule to delete useless tags
        if self._target.bad_expr!=None:
            for primitive in self._target.bad_expr:
                for tag in eval('doc.'+primitive):
                    super_tag =tag.getparent()
                    super_tag.getparent().remove(super_tag)
        # 1st expr determines the articles elements
        posts = eval('doc.'+self._target.expr[0])
        # left expressions determine posts information
        debug_num = 0
        for post in posts:
            data = []
            try:
                for od in range(1, 6, 1):
                    data.append(eval('post.' + self._target.expr[od]).strip())
            except Exception as ext:
                print(ext,': post number {}'.format(debug_num))
            debug_num += 1
            data.append(self._target.url)
            self._posts.append(Article(data))

    @property
    def posts(self):
        return self._posts


if __name__=='__main__':
    # test with xz.aliyun.com
    # 迫于html文档的复杂性，这里的检测原语全部带上xpath，送入后用eval执行
    # expr顺序对应意义：
    #               post位置
    #               标题位置
    #               链接位置
    #               作者位置
    #               分类位置
    #               日期位置
    #               干扰项规则，用来删除干扰节点，因为可能不止一项，
    aliyun = Target('https://xz.aliyun.com', ["xpath('//td')",
                                         "xpath('./p[1]/a[@class=\\'topic-title\\']')[0].text",
                                         "xpath('./p[1]/a[@class=\\'topic-title\\']/@href')[0]",
                                         "xpath('./p[2]/a[1]')[0].text",
                                         "xpath('./p[2]/a[2]')[0].text",
                                         "xpath('./p[2]/text()')[2]"])

    anquanke = Target('https://www.anquanke.com', ["xpath('//div[@class=\\'article-item common-item\\']')",
                                         "xpath('.//div[@class=\\'title\\']/a')[0].text",
                                         "xpath('.//div[@class=\\'title\\']/a/@href')[0]",
                                         "xpath('.//div[@class=\\'article-info-left\\']/a/span')[0].text",
                                         "xpath('.//div[@class=\\'tags  hide-in-mobile-device\\']/a/div/span')[0].text",
                                         "xpath('.//div[@class=\\'article-info-left\\']/span/span/i')[0].tail"])

    freebuf = Target('https://www.freebuf.com', ["xpath('//div[@class=\\'news_inner news-list\\']')",
                                         "xpath('./div[@class=\\'news-info\\']/dl/dt/a[1]/@title')[0]",
                                         "xpath('./div[@class=\\'news-info\\']/dl/dt/a[1]/@href')[0]",
                                         "xpath('./div[@class=\\'news-info\\']/dl/dd/span[1]/a')[0].text",
                                         "xpath('./div[@class=\\'news-info\\']/div/span/a')[0].text",
                                         "xpath('./div[@class=\\'news-info\\']/dl/dd/span[3]')[0].text"],
                                         ["xpath('//div[@class=\\'column-carousel clearfix  recommendNew\\']')",
                                          "xpath('//div[@class=\\'column-carousel\\']')"])

    _4hou = Target('https://www.4hou.com', ["xpath('//div[@id=\\'new-post6\\']')",
                                         "xpath('.//div[@class=\\'new_con\\']/a/h1')[0].text",
                                         "xpath('.//div[@class=\\'new_con\\']/a/@href')[0]",
                                         "xpath('.//div[@class=\\'avatar_box newtime\\']/a/p')[0].text",
                                         "xpath('.//div[@class=\\'new_img\\']/span')[0].text",
                                         "xpath('.//div[@class=\\'avatar_box newtime\\']/span')[0].text"])

    cl = Collector(_4hou)
    blog = cl.get_blog()
    if blog is None:
        print('the target {} currently not visited!'.format(_4hou.url))
    cl.parse_blog(blog)
    for p in cl.posts:
        print(p)

    '''
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

    print("---------------")
    
    # 1st expression, get the post lists
    articles = docs.xpath("//td")
    
    # 2nd expression, get detailed information by class
    for day in scope:
        if day == date:
            Today_Articles.append(Aritcle(title,href,author,type,date))
    
    if len(Today_Articles)==0:
        print("今天还没更新，半小时后再来")
    else:
        for element in Today_Articles:
            print(element)
    '''
