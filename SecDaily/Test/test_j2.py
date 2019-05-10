#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@author: d00ms(--)
@file: test_j2.py
@time: 2019-5-10 9:51
@desc: test jinja2
"""

#import json
from SecDaily.Breakfast import Article
from jinja2 import Environment, FileSystemLoader

if __name__=='__main__':
    env = Environment(loader= FileSystemLoader('../templates'))
    template = env.get_template('report.j2')

    a1 = Article(['helelo ktity','https://www.fdsfjl.cfd/1234.html','wr','paper','2019-09-10','https://www.zc.dafli'])
    a2 = Article(['hello  ktity','https://www.ff342342.cfd/1234.html','rer','paper','2019-09-10','https://www.3213.dafli'])
    art_list = [a1,a2]

    d1 = {'Origin':'https://xz.aliyun.com', 'Articles':art_list, 'Len':len(art_list)}
    all = [d1]
    #    d2 = {'Origin':'www.freebuf.com', 'Articles':[4,5,6,5,1], 'Len':5}
    #    d3 = {'Origin':'www.4hou.com', 'Articles':[], 'Len':0 }

    content = template.render(results = all, date='2019-5-10')
    with open('output.html','w',encoding='utf-8') as file:
        file.write(content)
