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
# 0.    Hook住导航，避免页面提前跳转
# 4.    Js代码注入及请求拦截
# 6.    节点变更查询

# 1.    TreeWalker节点遍历
# 2.    表单查询（填入数据）
# 3.    DOM0事件触发
# 5.    DOM2事件触发

# 7.    session分离控制
#########################
# Fuzzer function list:
# 1.    Payload注入与检测
# 2.    请求Url去重
# 3.    记录请求/响应
##########################



# target = 'https://hz.fang.com'
target = 'http://118.25.88.94:3000'
# target = 'https://www.baidu.com'

image_raw_response = ('SFRUUC8xLjEgMjAwIE9LCkNvbnRlbnQtVHlwZTogaW1hZ2UvcG5nCgqJUE5HDQoaCgAAAA1JSERSAAAAAQ'
                      'AAAAEBAwAAACXbVsoAAAAGUExURczMzP///9ONFXYAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAAKSURBVAiZY'
                      '2AAAAACAAH0cWSmAAAAAElFTkSuQmCC')

# some CDP test code

"""
# browser = await connect({'browserWSEndpoint':browser.wsEndpoint})

wsUrl = browser.wsEndpoint
print('CDP监听端口：', wsUrl)
urlElements = urlparse(wsUrl)

# step1, record the blank page id, shutdown it when open a new tab
metas = json.loads(retrieve(urlElements.port, '/json/list'))
for meta in metas:
    if meta['type'] == 'page':
        blankPageId = meta['id']
        
ws = await websockets.connect(wsUrl)
await ws.send(json.dumps({"id":0,"method": "Target.createTarget", "params": {'url': 'https://xz.aliyun.com'}}))
reply = await ws.recv()
targetId1 = json.loads(reply)['result']['targetId']


pageWsUrl  = json.loads(retrieve(urlElements.port, '/json/new'))['webSocketDebuggerUrl']
ws = await websockets.connect(pageWsUrl)

await ws.send(json.dumps({"id":1,"method": "Page.navigate", "params": {"url":"https://www.anquanke.com"}}))
reply3 = await ws.recv()

# pyppeteer大多数类已经通过ws实现了CDP，所以一般功能都可以在API中找到，而无须自己实现
def retrieve(port,path):
    target = 'http://127.0.0.1:'+str(port)+path
    response = urlopen(target)
    return response.read().decode('utf-8')

"""


async def NodeTraversing(Page):
    return await Page.evaluate("""() => {
        // createTreeWalker(root, whatToShow, filter, entityReferenceExpansion) 实体引用扩展
        // TreeWalker内部采用深度优先遍历

        var treeWalker = document.createTreeWalker(
        document.body, NodeFilter.SHOW_ELEMENT,
        { acceptNode: function(node) { return NodeFilter.FILTER_ACCEPT; } },false );

        var inputs = new Array();
        while(treeWalker.nextNode()) {
            var element = treeWalker.currentNode;

            // 加入一些表单处理的函数，参照字典填充字段
            if (element.nodeName == "FORM") {
                for(var i=0; i<element.length;i++){
                    if (element[i].nodeName == "INPUT"){
                        inputs.push({type:element[i].type, 
                        name:element[i].name, 
                        value:element[i].value,
                        id:element[i].id})
                    }
                }            
            }

            if (element.nodeName.startsWith('on')) {
                console.log(element.nodeName, element.nodeValue);
            }
        };
        return inputs;   
    }""")
#    return results


async def InterceptXHR(Page):
    await Page.evaluateOnNewDocument('''()=>{
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
        XMLHttpRequest.prototype.__setRequestHeader = XMLHttpRequest.prototype.setRequestHeader;
        XMLHttpRequest.prototype.setRequestHeader = function (header, value) {
        // 记录 header
            console.log("Headers: "+header+" |Value: "+value);
            return this.__setRequestHeader(header, value);
        }
        // 关闭abort功能
        XMLHttpRequest.prototype.abort = function () {};
    }''')

async def hookEventListener(Page):
    await Page.evaluateOnNewDocument('''()=>{
    _addEventListener = Element.prototype.addEventListener;
    Element.prototype.addEventListener = function() {
        console.log(arguments, this)
        _addEventListener.apply(this, arguments)
    }
    window.__originalAddEventListener = window.addEventListener;
    window.addEventListener = function() {
        console.log(arguments, this)
        window.__originalAddEventListener.apply(this, arguments)
    }
    }''')

async def InterceptWindow(Page):
    await Page.evaluateOnNewDocument('''()=>{
        var oldWebSocket = window.WebSocket;
        window.WebSocket = function(url, arg) {
            console.log("new link: " + url);
            return new oldWebSocket(url, arg);
        }
        var oldEventSource = window.EventSource;
        window.EventSource = function(url) {
            console.log("new link: " + url);
            return new oldEventSource(url);
        }
        var oldFetch = window.fetch;
        window.fetch = function(url) {
            console.log("new link: " + url);
            return oldFetch(url);
        }
        
        window.close = function() {}
        window.open = function(url) { console.log(url); }
        
        window.__originalSetTimeout = window.setTimeout;
        window.setTimeout = function() {
            arguments[1] = 0;
            return window.__originalSetTimeout.apply(this, arguments);
        }
        window.__originalSetInterval = window.setInterval;
        window.setInterval = function() {
            arguments[1] = 0;
            return window.__originalSetInterval.apply(this, arguments);
        }
    }''')


async def main():

    # launch()还有好多有用的参数：
    # {'args': ['--proxy-server=127.0.0.1:1080']}
    # 开启devtools选项，默认会关闭headless
    browser = await launch({"ignoreHTTPSErrors": True, "devtools":True,
                            "args": [
                                "--disable-gpu", "--window-size=1000,800"
                                "--disable-web-security", "--disable-xss-auditor",
                                "--no-sandbox", "--disable-setuid-sandbox",
                            ]})

#    "executablePath": "C:/Users/lenovo/.pyppeteer/local-chromium/543305/chrome-win32/Chrome.exe"
#    "--window-size=1366,850"
#    "--start-maximized",

    # newePage()新打开一个tab，返回Page类
    pageLists = await browser.pages()
    page = pageLists[0]

    async def recordAndGo(req):
        global image_raw_response
#        if req.url.startswith('ws://'):
#            print('Websocket :'+req.url)
#        else:
        print(req.method + "====>" +req.url)
        print(req.headers)
        if req.method == 'POST':
            print(req.postData)
        if req.resourceType == 'image':
            # 返回伪造的图片内容
            await req.respond({'status':200,'body':image_raw_response})
            return
        await req.continue_()

    async def close_dialog(dialog):
        print(dialog.message)
        print(dialog.type)
        await dialog.dismiss()

#    await page.exposeFunction('hello', lambda name:print(name))
    await page.setRequestInterception(True)
    page.on('request', lambda request: asyncio.ensure_future(recordAndGo(request)))
#    page.on('dialog', lambda dialog: asyncio.ensure_future(close_dialog(dialog)))
#    await InterceptXHR(page)
    await InterceptWindow(page)
    await hookEventListener(page)
    await page.goto(url=target)
    # pyppeteer提供多种检索方法：
    # J->querySelector
    # JJ->querySelectorAll
    # Jeval->querySelectorEval
    # JJeval->querySelectorAllEval
    # Jx->xpath
    # evaluate函数的参数是一段待执行的javascript代码!
    # 例如：这里定义个匿名函数，参数element，返回element.src属性，通过外部i传值
    # titles = await page.evaluate('(element)=>{return element.src}', param)

    # then close the tab
#    retrieve(urlElements.port, '/json/close/{}'.format(blankPageId))

    cookies = await page.cookies()

    formNodes = await NodeTraversing(page)

    for input in formNodes:
        if input['type']== 'text':
            expr = '//input[@id="'+input['id']+'"]'
            inputer = await page.xpath(expr)
            await inputer[0].type('hello world')
        if input['type'] == 'submit':
            # locate the element handle
            expr = '//input[@id="'+input['id']+'"]'
            inputer = await page.xpath(expr)
            await inputer[0].click()

    events = await page.evaluate("""()=>{
        results = [];

        nodes = document.all;
        for(j = 0;j < nodes.length; j++) {
            attrs = nodes[j].attributes;
            for(k=0; k<attrs.length; k++) {
                if (attrs[k].nodeName.startsWith('on')) {
                    results.push({
                        EventsName: attrs[k].nodeName,
                        EventsValue: attrs[k].nodeValue
                    })
                }
            }
        }
        return results;
    }
    """)

    await browser.close()
    # return targetId1, events, reply3
    return events

if __name__ =='__main__':
    task = asyncio.ensure_future(main())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(task)
    events = task.result()
    for item in events:
        print(item)
