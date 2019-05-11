import unittest
import asyncio
import aiohttp

async def sendReq(url):
    header = {'User-Agent': 'Mozilla/5.0 Chrome/72.0.3626.121 Safari/537.36'}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers= header) as r:
            return await r.text()

async def controller(target):
    num = 4
    while num>0:
        print("Let's start {} requet for {}".format(num,target))
        await sendReq(target)
#        if reply.stauts_code == 200:
        print("we've finished {} requets for {}".format(num, target))
        num -= 1

class Tester(unittest.TestCase):
    def test_something(self):
        targets = ['https://www.4hou.com', 'https://www.anquanke.com']
        loop = asyncio.get_event_loop()
        tasks = [controller(targets[0]), controller(targets[1])]
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()


if __name__ == '__main__':
    unittest.main()
