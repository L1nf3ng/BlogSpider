#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@author: d00ms(--)
@file: testWater2.py
@time: 2019-7-1 17:49
@desc: login zoomeye and search for seeyon keyword, then get the urls
"""
import asyncio
from pyppeteer.launcher import  launch

# a redirect url
redirect_url = "https://api.weibo.com/oauth2/authorize?client_id=1496756796&response_type=code&redirect_uri=https://sso.telnet404.com/oauth/callback/weibo?service=https://www.zoomeye.org/login"
zoom_url = 'https://www.zoomeye.org/searchResult?q=seeyon%20%2bcountry:%22CN%22&t=all'
# I hard coded here, so what?
weibo_username = "964997188@qq.com"
weibo_password = "liqiuxuan"
# TMD, you must click some buttons for a while
click_delay_time = 500


async def main():
    browser = await launch(devtools= True, args=["--start-maximized"])
    tabs = await browser.pages()
    tab = tabs[0]

    # Login Part
    await tab.goto(redirect_url)
#    userIdButton = await tab.querySelector('input#userId')
#    passWdButton = await tab.querySelector('input#passwd')
#    await userIdButton.type(weibo_username)
#    await passWdButton.type(weibo_password)

    # 另一种写法
    await tab.type('input#userId', weibo_username)
    await tab.type('input#passwd', weibo_password)
    asyncio.wait([await tab.click('a[action-type="submit"]',delay= 500),
        await tab.waitForNavigation(waitUntil='load')])


    # Search Part
    tab2 = await browser.newPage()
    await tab2.goto(zoom_url)
#    searchText = await tab2.waitForXPath('//input[@type="text"]')
#    await searchText.type('seeyon')
#    await tab2.keyboard.down('Enter')

    # record the navigation information:
    await tab2.setViewport(dict(width=1200, height=900))
    results, ips = [], []
    page_num =20

    while len(ips) ==0 :
        await tab2.reload(waitUntil='load')
        ips = await tab2.evaluate('''()=>{
            var ips = new Array();
            rooms = document.querySelectorAll('.search-result-item-title');
            for( var x=0;x<rooms.length;x++){
                if( !rooms[x].href.startsWith('https://www.zoomeye.org')){
                    ips.push(rooms[x].href);
                }
            }
            return ips;
        }''')
    results.extend(ips)

    while page_num != 0:
        nextButton = await tab2.waitForSelector('.ant-pagination-next')
        await nextButton.click(delay= click_delay_time)
        while len(ips) ==0:
            beforeButton = await tab2.waitForSelector('.ant-pagination-prev')
            await beforeButton.click()
            nextButton = await tab2.waitForSelector('.ant-pagination-next')
            await nextButton.click(delay=click_delay_time)
            ips = await tab2.evaluate('''()=>{
                var ips = new Array();
                rooms = document.querySelectorAll('.search-result-item-title');
                for( var x=0;x<rooms.length;x++){
                    if( !rooms[x].href.startsWith('https://www.zoomeye.org')){
                        ips.push(rooms[x].href);
                    }
                }
                return ips;
            }''')
        results.extend(ips)
        page_num -= 1
    # the next page
    s = '\n'.join(results)
    with open('url.txt', 'w') as file:
        file.write(s)

    print(tab2.url)
    """
    await asyncio.gather(
        tab.waitForNavigation(),
        submitButton.click(),
    )
    await tab.evaluate('''()=>{
        var login = document.querySelector('a[action-type="submit"]');
        login.click();
    }''')
    status = await tab.waitForFunction('''()=>{
        var login = document.querySelector('a[action-type="submit"]');
        login.click();  
    }''')

    if button is None:
        button = await tab.waitForXPath('//div[@class="header-login"]')
    await button.click()
    """

    await browser.close()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait([main()]))
