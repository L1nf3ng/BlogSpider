#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@author: d00ms(--)
@file: testWater4.py
@time: 2019-10-10 11:46
@desc:
"""

import re
import asyncio
from pyppeteer.launcher import launch
from pyppeteer.errors import NetworkError

original = """\
Discovered open port 80/tcp on 10.0.12.130
Discovered open port 8080/tcp on 10.0.12.153
Discovered open port 8080/tcp on 10.0.12.65
Discovered open port 8080/tcp on 10.0.12.86
Discovered open port 8080/tcp on 10.0.12.170
Discovered open port 8080/tcp on 10.0.12.134
Discovered open port 8080/tcp on 10.0.12.58
Discovered open port 8080/tcp on 10.0.12.45
Discovered open port 8080/tcp on 10.0.12.43
Discovered open port 8080/tcp on 10.0.12.154
Discovered open port 80/tcp on 10.0.12.93
Discovered open port 80/tcp on 10.0.12.65
Discovered open port 80/tcp on 10.0.12.112
Discovered open port 8080/tcp on 10.0.12.42
Discovered open port 80/tcp on 10.0.12.111\
"""


async def main(urls):
    browser = await launch({"ignoreHTTPSErrors": True, "devtools": True,"args": ["--disable-gpu", "--window-size=1000,800"]})
    pList = await browser.pages()
    await pList[0].goto(urls[0])
    for i in range(1,len(urls)):
        page = await browser.newPage()
        try:
            await page.goto(urls[i])
        except NetworkError:
            print(urls[i])

if __name__ == '__main__':
    sentences = original.split('\n')
    URLs = []
    for sq in sentences:
        temp = re.findall( 'port (\d+)/tcp on (.*)',sq)
        port, ip = temp[0]
        URLs.append('http://{}:{}'.format(ip,port))

    task = asyncio.ensure_future(main(URLs))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(task)

    pass
