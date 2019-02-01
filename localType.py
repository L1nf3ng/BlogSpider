# encoding: utf-8
#

from urlparse import urlparse
from datetime import datetime
from sqlalchemy import String,Column,Integer,DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

###################
#   异常类：
#       没有定义，仅仅通知url格式错误
###################
class UrlFormatError(Exception):
    def __repr__(self):
        return 'Source URL format error!(Maybe unsupported sheme).'

###################
#   源url类：
#       用于存储国外安全公司、大佬的网站地址，后续会有个字段存储站内博客网址
###################
class sourceUrl(Base):

    # 第二张表，表名：urls，主要记录：文章来源网址及分析结果
    __tablename__ = 'URLs'
    #
    _no = Column('Id',Integer, primary_key=True)
    # 文章所属网站域名
    _url = Column('Domains',String(80), nullable=False)
    # 文章原始url
    _blog_url = Column('Original_urls',String(200), nullable=True)
    # 获取的博客、情报级目录
    _source_path = Column('Blog_path',String(150),nullable=True)


    def __init__(self, urlstring):
        urlstring = urlstring.strip()
        if urlstring.startswith('http://') or urlstring.startswith('https://'):
            self._blog_url = urlstring
            self._url = urlparse(urlstring).netloc
        else:
            print '[-] Error Url: '+urlstring
            self._url = ''
            raise UrlFormatError

    def __eq__(self, other):
        if isinstance(other, sourceUrl):
            return (self._url == other._url)
        else:
            return False

    def __ne__(self, other):
        return (not self.__eq__(other))

    def __hash__(self):
        return hash(self._url)

    def getUrl(self):
        return self._url

###################
#   作者类：
#       用于存储国内几大平台的翻译作者信息，后续会建立与url类的关联
###################
class Author(Base):

    # 首张表，表名：authors，主要记录：安全客作者信息
    __tablename__ = 'Authors'
    #
    _no = Column('id',Integer, primary_key=True)
    # 作者姓名
    _name =  Column('name',String(40), nullable=False)
    # 作者在安全客个人页网址
    _url = Column('url',String(80), nullable=False)
    # 作者注册时间
    _reg_date = Column('reg_time',DateTime(),nullable=False)
    # 作者粉丝数
    _follower_count = Column('followers',Integer, nullable=True)
    # 发表文章数
    _post_count = Column('posts',Integer, nullable=True)

    def __init__(self,name,id,reg_date,post_count,follower_count):
        self._name, self._id, self._reg_date, self._post_count, self._follower_count = name, id, reg_date, post_count, follower_count
        self._reg_date = datetime.strptime(self._reg_date, '%Y-%m-%d %H:%M:%S')
        self._url = 'https://www.anquanke.com/member/'+str(self._id)
        self._api = 'https://api.anquanke.com/data/v1/posts?size=10&author='+str(self._id)

    def __str__(self):
        string = 'name:{}  reg_date:{} posts:{} followers:{}'.format(self._name.encode('utf8'), self._reg_date, self._post_count,self._follower_count)
        return string

    def __eq__(self, other):
        if isinstance(other, Author):
            return ((self._name == other._name) and (self._reg_date == other._reg_date))
        else:
            return False

    def __ne__(self, other):
        return (not self.__eq__(other))

    def __hash__(self):
        return hash(self._name) + hash(self._id)

    def getAPI(self,pageNo):
        return self._api+'&page='+str(pageNo)


###################
#   功能函数：
#       通过engine参数生成表结构
###################
def createTable(engine):
    Base.metadata.create_all(engine)

