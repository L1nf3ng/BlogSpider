# coding:utf-8
# test instance from github

import asyncio
import json
import websockets
from urllib.parse import urlparse
from urllib.request import urlopen
from pyppeteer.launcher import launch, connect

################################################################
#  API文档：https://miyakogi.github.io/pyppeteer/reference.html
################################################################

########################
# Crawler function list：
# 1.    TreeWalker节点遍历
# 2.    表单查询（填入数据）
# 3.    DOM0事件触发
# 4.    Js代码注入及请求拦截
# 5.    DOM2事件触发
# 6.    节点变更查询
# 7.    session分离控制
#########################
# Fuzzer function list:
# 1.    Payload注入与检测
# 2.    请求Url去重
# 3.    记录请求/响应
##########################



# target = 'https://hz.fang.com'
# target = 'http://10.10.10.108/test/365.html'
target = 'http://10.10.10.108/bodgeit/'


def retrieve(port,path):
    target = 'http://127.0.0.1:'+str(port)+path
    response = urlopen(target)
    return response.read().decode('utf-8')


async def main():

    # launch()还有好多有用的参数：
    # {'args': ['--proxy-server=127.0.0.1:1080']}
    # 开启devtools选项，默认会关闭headless
    browser = await launch({"ignoreHTTPSErrors": True, "devtools":True,
                            "args": [
                                "--disable-gpu",
                                "--disable-web-security", "--disable-xss-auditor",
                                "--no-sandbox", "--disable-setuid-sandbox",
                            ]})
#   "executablePath": "C:/Users/lenovo/.pyppeteer/local-chromium/543305/chrome-win32/Chrome.exe"  "--window-size=1366,850"   "--start-maximized",

    """
#    browser = await connect({'browserWSEndpoint':browser.wsEndpoint})
    wsUrl = browser.wsEndpoint
    print('CDP监听端口：',wsUrl)
    urlElements = urlparse(wsUrl)

    # step1, record the blank page id, shutdown it when open a new tab
    metas = json.loads(retrieve(urlElements.port, '/json/list'))
    for page in metas:
        if page['type']=='page':
            blankPageId = page['id']

    ws = await websockets.connect(wsUrl)
    await ws.send(json.dumps({"id":0,"method": "Target.createTarget", "params": {'url': 'https://xz.aliyun.com'}}))
    reply = await ws.recv()
    targetId1 = json.loads(reply)['result']['targetId']

    retrieve(urlElements.port, '/json/close/{}'.format(blankPageId))

    pageWsUrl  = json.loads(retrieve(urlElements.port, '/json/new'))['webSocketDebuggerUrl']
    ws = await websockets.connect(pageWsUrl)

    await ws.send(json.dumps({"id":1,"method": "Page.navigate", "params": {"url":"https://www.anquanke.com"}}))
    reply3 = await ws.recv()
    """

    # newePage()新打开一个tab，返回Page类
    page = await browser.newPage()

    async def recordAndGo(req):
        print(req.url)
        await req.abort()

    await page.exposeFunction('hello', lambda name:print(name))
#    await page.setRequestInterception(True)
#    page.on('request', lambda request: asyncio.ensure_future(recordAndGo(request)))

    await page.goto(url=target)
    # pyppeteer提供多种检索方法：
    # J->querySelector
    # JJ->querySelectorAll
    # Jeval->querySelectorEval
    # JJeval->querySelectorAllEval
    # Jx->xpath
    # evaluate函数的参数是一段待执行的javascript代码!
    # 例如：这里定义个匿名函数，参数element，返回element.src属性，通过外部i传值
    # titles = await page.evaluate('(element)=>{return element.src}',i)

    await page.evaluate("""() => {
        var treeWalker = document.createTreeWalker(
        document.body, NodeFilter.SHOW_ELEMENT,
        { acceptNode: function(node) { return NodeFilter.FILTER_ACCEPT; } },false );
        
        while(treeWalker.nextNode()) {
            var element = treeWalker.currentNode;
            console.log(element);
            if (element.nodeName.startsWith('on')) {
            console.log(element.nodeName, element.nodeValue);
            }
        };   
    }""")


    await page.evaluate('''()=>{
        XMLHttpRequest.prototype.__originalOpen = XMLHttpRequest.prototype.open;
        XMLHttpRequest.prototype.open = function(method, url, async, user, password) {
            console.log("Open: "+method+":"+url+"|");
            return this.__originalOpen(method, url, async, user, password);
        }
        XMLHttpRequest.prototype.__originalSend = XMLHttpRequest.prototype.send;
        XMLHttpRequest.prototype.send = function(data) {
            console.log("Data: "+data);
            return this.__originalSend(data);
        }    
    }''')


    events = await page.evaluate("""()=>{
        results = [];
        /*
        nodes = document.all;
        for(j = 0;j < nodes.length; j++) {
            attrs = nodes[j].attributes;
            for(k=0; k<attrs.length; k++) {
                if (attrs[k].nodeName.startsWith('on')) {
                    results.push({
                        nodeName: attrs[k].nodeName,
                        nodeValue: attrs[k].nodeValue
                    })
                }
            }
        }*/

        for(var i=0;i<document.forms.length;i++){
            form = document.forms[i];
            console.log(form.method, form.action)
            for(var j=0;j<form.length;j++){
                input = form[j];
                results.push({
                    nodeName: input.nodeName,
                    inputType: input.type,
                    inputName: input.name
                })
            }
        }
        return results;
    }
    """)

    await browser.close()
    # return targetId1, reply3, events
    return events

if __name__ =='__main__':
    task = asyncio.ensure_future(main())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(task)
    events = task.result()
    for item in events:
        print(item)
