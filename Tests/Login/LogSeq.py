#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@author: d00ms(--)
@file: LogSeq.py
@time: 2019-7-12 9:31
@desc: Log on sequences
"""


##########################################
#   功能点1：登录/cookie填充（并不万能）
##########################################

async def logOn1(page, path, userId, passWd):
    #    await asyncio.gather(page.waitForNavigation(),page.goto(url+'/#/'+anchor))
    await page.goto(path)
    input1 = await page.waitForSelector('input#email')
    input2 = await page.waitForSelector('input#password')
    button = await page.waitForSelector('button#loginButton')
    await input1.type(userId)
    await input2.type(passWd)
    await button.click()
    # left server some time to finish authorization.
    await page.waitFor(3000)
    #    await asyncio.gather(page.waitForNavigation(), page.goto(url))


async def logOn2(page, path, userId, passWd):
    #    await asyncio.gather(page.waitForNavigation(),page.goto(url+'/#/'+anchor))
    await page.goto(path)
    input1 = await page.waitForSelector('input.loginInput')
    input2 = await page.waitForSelector('input[name="password"]')
    button = await page.waitForSelector('input[type="submit"]')
    await input1.type(userId)
    await input2.type(passWd)
    await button.click()
    # left server some time to finish authorization.
    await page.waitFor(3000)
    #    await asyncio.gather(page.waitForNavigation(), page.goto(url))
