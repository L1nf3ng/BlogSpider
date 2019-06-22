# BlogSpider

写一个类似于scrapy的爬虫框架，目标主要针对博客类文章。

## 结构

项目由两个爬虫组成：

一、针对安全客作者信息的爬虫，搜集最近发表文章的作者的文章来源，从中提取有用的大站博客目录、个人博客域名

二、针对上一步爬到的有用信息，在VPS上部署一个通用型爬虫，定期爬取新鲜博客，并以邮件方式发送提醒

## 进度

第一个爬虫已经完成

第二个爬虫的设想是对不同的站点做不同的规则库，每日爬取时都从对应的库中读取规则并解析，此时需要一个数据库来缓存上一段时间的数据（比较得出新写的文章）；
目前暂停这一步工作，在SecDaily这个目录下我试水了以xpath表达式作为爬取规则，并对爬取+分析过程做了一定的容错，感觉效果不错，后期可以考虑引入这种方式。
但接下来应该不会花费大量时间去翻译博客了，有太多更值得去做的事！

判断规则如下：

1. 第一次运行时先爬取一遍当前最新文章作为初始数据，如果有近两日文章出现则做一次提醒
2. 第二次运行时爬取文章后和旧数据比较，日期有更新则做一次提醒

## 其他用途

这个repo只用来放爬虫可惜了。决定在这里放一些自写的、扒别人的小脚本，以及一个POCs文件夹专门用来记录自己验证过的漏洞细节。

## Reading Lists

* [https://blog.csdn.net/he_and/article/details/77963446]()
* [https://www.jianshu.com/p/ecab9fc8d746]()
> pyppeteer官方API文档
* [https://miyakogi.github.io/pyppeteer/reference.html]()
> 别人的试水帖
* [https://lightless.me/archives/first-glance-at-chrome-headless-browser.html]()
* [https://lightless.me/archives/chrome-headless-second.html]()
> Chrome DevTools Protocol
* [https://chromedevtools.github.io/devtools-protocol/tot]()
> 关于库本身
* [https://www.anquanke.com/post/id/103350]()
> StackOverflow
* [https://stackoverflow.com/questions/53945876/telethon-python-asyncio-typeerror-coroutine-object-is-not-callable#]()
> 有用的经验
* [http://blog.fatezero.org/2018/03/05/web-scanner-crawler-01/]()
* [http://blog.fatezero.org/2018/04/09/web-scanner-crawler-02/]()
* [http://blog.fatezero.org/2018/04/15/web-scanner-crawler-03/]()


