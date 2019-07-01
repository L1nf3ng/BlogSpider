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

zoom_url = "https://www.zoomeye.org"
# so I hard coded here
username = "nuaa_llf@126.com"
password = "123HjKl+"

async def main():
    browser = await launch(devtools= True, args=["--window-size=1366,850"])
    tabs = await browser.pages()
    tab = tabs[0]
    await tab.goto(zoom_url)
#    buttons = await tab.xpath('//div[@class="header-login"]')
#    inputs = await tab.xpath('//input[@type="text"]')
    button = await tab.evaluate("""()=>{
        var login = document.getElementsByClassName('header-login')[0];
        return login;
    }""")
    if button is None:
        buttons = await tab.xpath('//div[@class="header-login"]')
        button = buttons[0]
    await button.click()
    await browser.close()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait([main()]))
