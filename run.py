# encoding:utf-8
#
#!/usr/bin/env python
# 
# 功能: 第一次版本尝试
#
# TODO: 1. 爬取安全客翻译作者的资料 & 分析他们的资料来源
# TODO: 2. 将源添入database并更新
# TODO: 3. 每天抓取源的最新文章
# TODO: 4. 抓取先知、freebuf和安全客的最新文章比对 & 列举可以翻译的文章
# TODO: 5. 提醒功能：
# TODO:     - 出现新的源
# TODO:     - 出现新的翻译作者
# TODO:     - 源内出现新文章
# TODO:     - 文章已被翻译过

# METHOD 1
"""
_360url = 'https://www.anquanke.com'
# urlretrieve(_360url,'test.html')

from lxml import etree
def grab_first_page():
    instance_loc = './test.html'
    trees = etree.parse(instance_loc,etree.HTMLParser())
    set1 = trees.xpath('//div[@class="article-info-left"]')
    bitches = set()
    for entry in set1:
        author = entry.xpath('./a/span/text()')[0]
        href = entry.xpath('./a/@href')[0]
        date  = entry.xpath('./span[@class="date"]/span/text()')[1]
        fee = entry.xpath('./span[@class="hide-in-mobile-device"]')
        if len(fee)>0 :
            bitches.add(author)
    for name in bitches:
        print name+' '+date+" "+_360url+href
"""


# METHOD 2
from urllib.request import urlopen
from localType import Author,sourceUrl,createTable
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import create_engine
import os
import json

WRITERS,URLS = set(),set()

_360api = 'https://api.anquanke.com/data/v1/posts?size=20&page='
_tableName = 'storage.db'
engine = create_engine("sqlite://"+"/"+_tableName)
Session = sessionmaker(bind=engine)


####################
#   功能函数1：获取某作者的n页博客链接
####################
def authorPageSearch(pageNo, writer):
    global URLS
    print('\r\n\r\n'+str(writer))
    for pno in range(1, pageNo+1):
        buff = urlopen(writer.getAPI(pno)).read()
        block = json.loads(buff)['data']
        for post in block:
            type,url,title,date = post['type'],post['url'],post['title'],post['date']
            if type == u'origin' and url == u'':
                print('原创文章： {}'.format(title.encode('utf8')))
            elif type == u'translate' and url != u'':
                sUrl = sourceUrl(url)
                URLS.add(sUrl)
                print('翻译文章：发布时间：{} {}'.format(date.encode('utf8'),url.encode('utf8')))
            else:
                print('未分类文章： {}'.format(title.encode('utf8')))
        next = json.loads(buff)['next']
        if next is u'':
            break

####################
#   功能函数2: 从主页开始爬取n页
####################
def mainPageSearch(pageNo):
    global WRITERS
    for pno in range(1,pageNo+1):
        buffer = urlopen(_360api+str(pno)).read()
        content = json.loads(buffer)['data']
        status = u'success' if json.loads(buffer)['success'] is True else u'fail'
        for post in content:
            author_info, title, date, fee, tags = post['author'], post['title'], post['date'], post['fee'], post['tags']
            # 有稿酬的作者，即个人作者
            if fee!= u'' :
                author = Author(author_info['nickname'], author_info['id'], author_info['register_date'], author_info['post_count'], author_info['follower_count'])
                WRITERS.add(author)
    for writer in WRITERS:
        authorPageSearch(2, writer)


####################
#  程序起点
####################
if __name__ == '__main__':
    # 先删表，再建表，避免重复
    os.system("del "+_tableName)
    createTable(engine)
    mainPageSearch(3)
    session1 = Session()
    session1.add_all([ x for x in WRITERS])
    session1.commit()
    session1.close()
    session2 = Session()
    session2.add_all([ x for x in URLS])
    session2.commit()
    session2.close()
