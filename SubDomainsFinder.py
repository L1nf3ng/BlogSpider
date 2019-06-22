# encoding:utf-8
# author: T3mple

# commit a simple request and parse all urls in html page.
# 运行环境： python3
# 依赖库： requests, lxml
# the main target is a sitemap page!

import re,sys
import requests
from lxml import etree
from urllib import parse


# the function filter urls according to re rules!
def re_filter(x):
    # filter style: {{ vue.global.data }}
    ptn1= re.compile('\{\{[\w\W]*?\}\}')
    # filter style: javascript:void(0)
    ptn2= re.compile('javascript:')
    # filter style: #
    ptn3= re.compile('^#$')
    # filter style: empty url
    ptn4= re.compile('^$')
    if ptn1.match(x) or ptn2.match(x) or ptn3.match(x) or ptn4.match(x):
        return True
    return False

# the function analysize the structure of domain
def parse_domain(x):
    index= x.find('.')
    if index<0:
        return (0, '')
    pos=list()
    while index!=-1:
        pos.append(index)
        index= x.find('.',index+1)
    if len(pos)+1>2:
        return (len(pos)+1, x[pos[-2]+1:])
    # just two level domains or root domain
    else:
        return (len(pos)+1, x)


def main():

    if len(sys.argv)!=3 or sys.argv[1]!='-u':
        print('Usage: SubDomainsFinder.py -u [url]')
        exit(22)

    base_url = sys.argv[2]

    host_url= parse.urlparse(base_url,'http').netloc
    (level, main_domain)= parse_domain(host_url)

    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    r = requests.get(base_url, headers=header, verify=False)
    if r.status_code != 200:
        print('Status code error:', r.status_code)
        exit(1)

    content = r.content.decode(r.encoding)
    charset = re.search('charset="(.*)"',content).group(1)
    print("Returned status:{}, HTML Encode Form:{}".format(r.status_code,charset))

    html_tree = etree.HTML(content)
    # the result is a set of strings
    res_urls= html_tree.xpath('//@src|//@href')
    counter=0
    subdomains= set()
    for x in res_urls:
        if re_filter(x):
            continue
        # start url analysis and output the subdomains in a set
        domain_url= parse.urlparse(x, 'http').netloc
        (num, domain)= parse_domain(domain_url)
        if domain == main_domain and num==3 :
            subdomains.add(domain_url)
            counter+=1
    print('Totally get useful %d urls, and got %d subdomains.'%(counter,len(subdomains)))
    for y in subdomains:
        print (y)

if __name__=='__main__':
    main()
