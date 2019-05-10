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
import unittest

async def sendReq(target):
    header = {'User-Agent':'Mozilla/5.0 Chrome/72.0.3626.121 Safari/537.36'}
    reply =  requests.get(target, headers= header)
    return reply

async def controller(target):
    num = 5
    while num>0:
        print("Let's start {} requet for {}".format(num,target))
        await sendReq(target)
#        if reply.stauts_code == 200:
        print("we've finished {} requets for {}".format(num, target))
        num -= 1


class Tester(unittest.TestCase):
    def testTime(self):
        targets = ['https://www.4hou.com', 'https://www.anquanke.com']
        loop = asyncio.get_event_loop()
        tasks = [controller(targets[0]), controller(targets[1])]
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()


if __name__== '__main__':

    unittest.main()
