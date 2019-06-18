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

target = 'https://hz.fang.com'

async def main():

    # launch()还有好多有用的参数：
    # {'args': ['--proxy-server=127.0.0.1:1080']}
    # 开启devtools选项，默认会关闭headless
    browser = await launch({"ignoreHTTPSErrors": True, "devtools":True,
                            "args": [
                                "--disable-gpu", "--window-size=1366,850",
                                "--disable-web-security", "--disable-xss-auditor",
                                "--no-sandbox", "--disable-setuid-sandbox",
                            ]})
#        "executablePath":"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

#    browser = await connect({'browserWSEndpoint':browser.wsEndpoint})
    wsUrl = browser.wsEndpoint
    print('修改后的CDP监听端口：',wsUrl)
    ws = await websockets.connect(wsUrl)

    await ws.send(json.dumps({"id":0,"method": "Target.createTarget", "params": {'url': 'https://xz.aliyun.com'}}))
    reply = await ws.recv()
    targetId1 = json.loads(reply)['result']['targetId']

#    await ws.send(json.dumps({"id":1,"method": "Target.createBrowserContext", "params": {}}))
#    reply2 = await ws.recv()
#    targetId2 = json.loads(reply2)['result']['browserContextId']

    schema, host, path, _, _, _ = urlparse(wsUrl)
    pageWsUrl = 'http://'+ host +'/json/new'
    reply = urlopen(pageWsUrl)
    pageWsUrl  = json.loads(reply.read())['webSocketDebuggerUrl']
    ws = await websockets.connect(pageWsUrl)

    await ws.send(json.dumps({"id":1,"method": "Page.navigate", "params": {"url":"https://www.anquanke.com"}}))
    reply3 = await ws.recv()


    return targetId1, reply3
    # newePage()新打开一个tab，返回Page类
    """
    page = await browser.newPage()
    dimensions = await page.evaluate('''()=>{
        return {width: document.documentElement.clientWidth,
                height: document.documentElement.clientHeight,
                deviceScaleFactor: window.devicePixelRatio}
    }''')
    await page.goto(url=target)
    # pyppeteer提供多种检索方法：
    # J->querySelector
    # JJ->querySelectorAll
    # Jeval->querySelectorEval
    # JJeval->querySelectorAllEval
    # Jx->xpath
    elements = await page.xpath('//img')
    print('{cc} of superlinks'.format(cc= len(elements)) )

    for i in elements:
        # evaluate函数的参数是一段待执行的javascript代码!
        # 例如：这里定义个匿名函数，参数element，返回element.src属性，通过外部i传值
        titles = await page.evaluate('(element)=>element.src',i)
        print(titles)

    await browser.close()
    return dimensions
    """

if __name__ =='__main__':
    task = asyncio.ensure_future(main())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(task)
    print(task.result())
