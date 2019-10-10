#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@author: d00ms(--)
@file: testWater3.py
@time: 2019-7-8 16:53
@desc: 测试一下Cookie的装填，可能有些网站的校验会很严格，此时可采用别的登录方式替代。
"""

import asyncio
import datetime
from Tests.Login.LogSeq import logOn1, logOn2
from pyppeteer.launcher import launch
from pyppeteer.network_manager import Request

# url = 'http://118.25.88.94:3000'
# DOMcookie = 'cookieconsent_status=dismiss; language=zh_CN; welcome-banner-status=dismiss'
url = 'http://10.10.10.108/dvwa/'
DOMcookie = "security=low; security_level=0; PHPSESSID=ogc2vmmd8q10mj3m147nnmf3g6; acopendivids=swingset,jotto,phpbb2,redmine; acgroupswithpersist=nada"
fakePhoto = 'SFRUUC8xLjEgMjAwIE9LCkNvbnRlbnQtVHlwZTogaW1hZ2UvcG5nCgqJUE5HDQoaCgAAAA1JSERSAAAAAQAAAAEBAwAAACXbVsoAAAAGUExURczMzP///9ONFXYAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAAKSURBVAiZY2AAAAACAAH0cWSmAAAAAElFTkSuQmCC'
records = []

# DOMcookie= "csrftoken=J2VJVFPPgGgPi4myBkYtMMoR2P6eWJ3wBl8VoOX0rwR991kQUi1vBgfcXUclrSOh; cookieconsent_status=dismiss; language=zh_CN; continueCode=av8Mgk2ym59pwOlxDdzoH2hrcps5iySzuVcnhMgT3wGKrnVePq1jzJbW7XZQ; token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdGF0dXMiOiJzdWNjZXNzIiwiZGF0YSI6eyJpZCI6MTQsInVzZXJuYW1lIjoiIiwiZW1haWwiOiJoamtsQDEyNi5jb20iLCJwYXNzd29yZCI6ImU5ZmQ1ODhiNTg3MjU0M2Q4NmM0NGU3NjMzNTZhNDk1IiwiaXNBZG1pbiI6ZmFsc2UsImxhc3RMb2dpbklwIjoiMC4wLjAuMCIsInByb2ZpbGVJbWFnZSI6ImRlZmF1bHQuc3ZnIiwiY3JlYXRlZEF0IjoiMjAxOS0wNy0wOSAwNTo1NTowOS43NDYgKzAwOjAwIiwidXBkYXRlZEF0IjoiMjAxOS0wNy0wOSAwNTo1NTowOS43NDYgKzAwOjAwIn0sImlhdCI6MTU2MjY1MzIwMSwiZXhwIjoxNTYyNjcxMjAxfQ.l63C1L93avxfJcpqCz8cNWs0ukmHAWnGdziT1O7feX0eOB6fXL-WKFFArMzg303E9fU2_xm2O6WC4SIOog9ikGdJBvbrJZBM0b0B23jVmsSy0hGqUGfB3j7TllssiJyWB55mQd8U9sQ9n7euoc8uUgxCua5DjQZodUhIIRxF8b8"


def cookieHandler(string):
    cookiebar = DOMcookie.split(';')
    result = []
    now = datetime.datetime.now()
    expire = now + datetime.timedelta(days=2)
    for cookie in cookiebar:
        k, v = cookie.strip().split('=')
        result.append(dict(name=k, value=v, expires=expire.timestamp()))
    return result

async def requestHandler(req: Request):
    global records
#    if req.resourceType == 'image':
#        await req.respond(dict(status= 200, body= fakePhoto))
    if req.isNavigationRequest() and not req.frame.parentFrame:
        records.append(dict(Protocol='http', Url=req.url))
        print("We get request-url: "+req.url)
        await req.respond(dict(status= 204))
#    else:
#    await req.continue_()

async def dialogHandler(dialog):
    await dialog.dismiss()


##########################################
#   功能点2：页面初始加载时注入Js
#   1. hook对象有：WebSocket, EventSource, fetch, close, open
#   2. 延时触发对象有：setTimeOut, setInternal
##########################################

async def hookJsOnNewPage(page):
    # in addtion, we inject those functions:
    await page.exposeFunction('PyLogWebSocket',lambda url: records.append(dict(Protocal='ws', Url=url)))
    await page.exposeFunction('PyLogEventSource',lambda url: records.append(dict(Protocal='es', Url=url)))
    await page.exposeFunction('PyLogFetch',lambda url: records.append(dict(Protocal='fetch', Url=url)))
    await page.exposeFunction('PyLogOpen',lambda url: records.append(dict(Protocal='open', Url=url)))
    await page.exposeFunction('PyLogPushState',lambda url: records.append(dict(Protocal='pushState', Url=url)))
    await page.exposeFunction('PyLogReplaceState',lambda url: records.append(dict(Protocal='Replace', Url=url)))


    await page.evaluate('''()=>{
    
        // history.pushState,replaceState可以做到页面内容不动的情况下，更新url
        window.history.pushState = function(a, b, url) { PyLogPushState(url);}
        Object.defineProperty(window.history,"pushState",{"writable": false, "configurable": false});
        
        // 修改这两个方法的属性为不可修改，来防止他人通过Js将代码回改        
        window.history.replaceState = function(a, b, url) { PyLogReplaceState(url);}
        Object.defineProperty(window.history,"replaceState",{"writable": false, "configurable": false});        
    
        var oldWebSocket = window.WebSocket;
        window.WebSocket = function(url, arg) {
            PyLogWs(url);
            // continue the original ws request
            return new oldWebSocket(url, arg);
        }
        Object.defineProperty(window,"WebSocket",{"writable": false, "configurable": false}); 
        
        // EventSource--HTML5特性，网页自动接收来自服务器的更新。
        var oldEventSource = window.EventSource;
        window.EventSource = function(url) {
            PyLogEs(url);
            return new oldEventSource(url);
        }
        Object.defineProperty(window,"EventSource",{"writable": false, "configurable": false}); 
        
        // fetch可以用来代替$.ajax,$.get,$.post
        var oldFetch = window.fetch;
        window.fetch = function(url) {
            PyLogFetch(url);
            return oldFetch(url);
        }
        // Object.defineProperty(window,"fetch",{"writable": false, "configurable": false});
         
        window.close = function() {}
        Object.defineProperty(window,"close",{"writable": false, "configurable": false});
                
        window.open = function(url) { PyLogOpen(url); }
        Object.defineProperty(window,"open",{"writable": false, "configurable": false});
        
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


async def hookClickEvent(page):

    await page.evaluateOnNewDocument('''()=>{
    
    // 一个误区便是window.onclick是DOM0事件，而这一内容一般是直接写HTML文档中的；所以在页面加载完成后无法hook
        function dom0_listener_hook(that, event_name) {
            console.log(that.tagName);
            console.log(event_name);
        }
        
        Object.defineProperties(HTMLElement.prototype, {
            onclick: {set: function(newValue){onclick = newValue;dom0_listener_hook(this, "click");}},
            onchange: {set: function(newValue){onchange = newValue;dom0_listener_hook(this, "change");}},
            onblur: {set: function(newValue){onblur = newValue;dom0_listener_hook(this, "blur");}},
            ondblclick: {set: function(newValue){ondblclick = newValue;dom0_listener_hook(this, "dblclick");}},
            onfocus: {set: function(newValue){onfocus = newValue;dom0_listener_hook(this, "focus");}}
        })         
        
        let old_event_handle = Element.prototype.addEventListener;
        Element.prototype.addEventListener = function(event_name, event_func, useCapture) {
            console.log(arguments, this);
            old_event_handle.apply(this, arguments);
        }
    }''')

async def main():

    global records
    browser = await launch(devtools=True) # args=["--start-maximized"]
    pages = await browser.pages()
    target = pages[0]

    await target.goto(url)

    cookies = cookieHandler(DOMcookie)
#    for cookie in cookies:
#        await target.setCookie(cookie)

#    await logOn1(target, 'login', 'hjkl@126.com', '543210')
    await logOn2(target, url+'/login.php', '1337', 'charley')
#    await hookJsOnNewPage(target)

#    await hookClickEvent(target)
#    await target.evaluateOnNewDocument('window.onbeforeunload = function(event) {event.returnValue = "Anything to stop jump...";}')

    # emit Js function hooked just now.
    # await target.reload()
    await target.setRequestInterception(True)
    target.on('request',lambda request: asyncio.ensure_future(requestHandler(request)))

#    target.on('dialog', lambda dialog: asyncio.ensure_future(dialogHandler(dialog)))

    # click the page sequncilly.
    """
    await target.evaluate('''()=>{
        function sleep(d){for(var t = Date.now();Date.now() - t <= d;);}

        var buttons= document.querySelectorAll('#main_menu_padded > ul:nth-child(2) > li');
        for (var i =0;i< buttons.length; i++){
            buttons[i].click();
        }
    }''')
    """
    buttons = await target.querySelectorAll('#main_menu_padded > ul:nth-child(2) > li')
    for button in buttons:
        await button.click()
    # send a fake request, and turn off the interception
    await target.reload()
    await target.setRequestInterception(False)

    await target.waitFor(5000)
    await browser.close()
    return records


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(main())
    loop.run_until_complete(task)
    print("Records looks like: ")
    print(task.result())
