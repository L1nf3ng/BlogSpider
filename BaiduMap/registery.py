#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""
@author: d00ms(--)
@file: registery.py
@time: 2019-9-19 15:06
@desc: for baidu map
"""
import requests
import re
import json
import time

##########################################################
#   在这里设置一些参数:
#       最重要的是等登陆百度按f12找到cookie字段BDUSS的值
#########################################################

# 设置BDUSS的值，找到后替换xxxx
cookieString = "BDUSS=Your BDUSS"
# 设置延时，秒为单位，可以是小数
timeInterval = 0
# 设置获取key的总数
keyNum = 50
# 应用名称
appName = "请君入瓮"

#########################################################
target = 'http://lbsyun.baidu.com/apiconsole/'
# proxy = {'http':'http://127.0.0.1:8080'}

header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"}

if __name__ == "__main__":
    cookie = {}
    H = cookieString.split(';')
    for x in H:
        l = x.index('=')
        k,v = x[:l], x[l+1:]
        cookie.update({k.strip():v.strip()})

    # step1. get the sign
    header.update({"X-Requested-With": "XMLHttpRequest", "Accept":"application/json, text/javascript, */*; q=0.01",
                   "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"})
    reply = requests.get(target+'key', headers= header, cookies= cookie)
    content = reply.content.decode('utf8')
    signature = re.findall('var sign = "(.*)";',content)[0]

    keys,appIds = [],[]
    # step2. request the appkey
    # generate a random application name
    for i in range(keyNum):
        name = appName+ str(i)
        payload = """app_name={}&\
        app_type=1&\
        services=geodata%2Cplace%2Clocation%2Cdirection%2Cstaticimage%2Cpanorama%2Cgeoconv%2Ctrace%2Croutematrix%2Ctimezone%2Cparking%2Crectify%2Ctraffic%2Clightdriving%2Clightriding%2Clightwalking%2Clighttransit%2Cgeocoding%2Creverse_geocoding%2Ctrackmatch&\
        m_scode=&\
        s_ips=0.0.0.0%2F0&\
        s_check_type=0&\
        sign={}""".format(name, signature)

        reply = requests.post(target+'app/create', headers= header, cookies= cookie, data= payload.encode('utf8'))
        text = json.loads(reply.content.decode('utf8'))
        status = text['status']
        if status == 0:
            ak = text["result"]["ak"]
            id = text["result"]["app_id"]
            print('id: ',id,' appkey: ',ak)
            keys.append(ak)
            appIds.append(id)
            time.sleep(timeInterval)
        else:
            print('大概是应用已经达到上限了，别的异常我没处理^)^')
            break

    ## step3, output the keys
    with open('keys.txt','a') as file:
        for key in keys:
            file.write(key+'\n')

    #  we store the appId to delete the key easily.
    with open('appIds.txt','a') as file:
        for id in appIds:
            file.write(str(id)+'\n')

