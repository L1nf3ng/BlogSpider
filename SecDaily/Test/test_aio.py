#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@author: d00ms(--)
@file: test_aio.py
@time: 2019-5-10 16:07
@desc: test the async/await pragma(supported by py3.5)
"""

# 任务是分别请求4hou、安全客5次。利用协程实现异步

import requests
import asyncio

async def sendReq(target):
    num = 5
    header = {'User-Agent':'Mozilla/5.0 Chrome/72.0.3626.121 Safari/537.36'}
    while num>0:
        print("Let's start {} requet for {}".format(num,target))
        reply = await requests.get(target, headers= header)
        if reply.stauts_code == 200:
            print("we've finished {} requets for {}".format(num, target))
        num -= 1
#        await asyncio.sleep(1)


if __name__== '__main__':

    targets = ['https://www.4hou.com', 'https://www.anquanke.com']
    loop = asyncio.get_event_loop()
    tasks = [sendReq(targets[0]), sendReq(targets[1])]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
