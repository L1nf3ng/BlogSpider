#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@author: d00ms(--)
@file: pyNC.py
@time: 2019-5-22 10:21
@desc: 公司杀软居然杀netcat，天理何在，决定空闲时间写一写py版的nc
"""

import sys
import getopt
import socket


def Usage(simple):
    # 这里和标准版不太一样，-h选项出一个简化版的帮助菜单（带实例），--help/--h选项出完整版的帮助菜单
    # 还有一点就是暂时使用getopt模块实现，故不支持-lvnp这样参数的连写，后期可以考虑自己实现解析
    simple_usage='''usage: nc [-46CDdFhklNnrStUuvZz] [-I length] [-i interval] [-M ttl]
        [-m minttl] [-O length] [-P proxy_username] [-p source_port]
        [-q seconds] [-s source] [-T keyword] [-V rtable] [-W recvlimit] [-w timeout]
        [-X proxy_protocol] [-x proxy_address[:port]] 	  [destination] [port]
    Command Summary:
        -4		Use IPv4
        -6		Use IPv6
        -b		Allow broadcast
        -C		Send CRLF as line-ending
        -F		Pass socket fd
        -h		This help text
        -l		Listen mode, for inbound connects
        -n		Suppress name/port resolutions
        -P proxyuser	Username for proxy authentication
        -p port		Specify local port for remote connects
        -r		Randomize remote ports
        -S		Enable the TCP MD5 signature option
        -s source	Local source address
        -t		Answer TELNET negotiation
        -U		Use UNIX domain socket
        -u		UDP mode
        -v		Verbose
        -w timeout	Timeout for connects and final net reads
        -X proto	Proxy protocol: "4", "5" (SOCKS) or "connect"
        -x addr[:port]	Specify proxy address and port
        Port numbers can be individual or ranges: lo-hi [inclusive]
    Example:
        pyNC.py -l -n -v -p 5555
        '''

    complex_usage='''usage: nc [-46CDdFhklNnrStUuvZz] [-I length] [-i interval] [-M ttl]
        [-m minttl] [-O length] [-P proxy_username] [-p source_port]
        [-q seconds] [-s source] [-T keyword] [-V rtable] [-W recvlimit] [-w timeout]
        [-X proxy_protocol] [-x proxy_address[:port]] 	  [destination] [port]
    Command Summary:
        -4		Use IPv4
        -6		Use IPv6
        -b		Allow broadcast
        -C		Send CRLF as line-ending
        -D		Enable the debug socket option
        -d		Detach from stdin
        -F		Pass socket fd
        -h		This help text
        -I length	TCP receive buffer length
        -i interval	Delay interval for lines sent, ports scanned
        -k		Keep inbound sockets open for multiple connects
        -l		Listen mode, for inbound connects
        -M ttl		Outgoing TTL / Hop Limit
        -m minttl	Minimum incoming TTL / Hop Limit
        -N		Shutdown the network socket after EOF on stdin
        -n		Suppress name/port resolutions
        -O length	TCP send buffer length
        -P proxyuser	Username for proxy authentication
        -p port		Specify local port for remote connects
        -q secs		quit after EOF on stdin and delay of secs
        -r		Randomize remote ports
        -S		Enable the TCP MD5 signature option
        -s source	Local source address
        -T keyword	TOS value
        -t		Answer TELNET negotiation
        -U		Use UNIX domain socket
        -u		UDP mode
        -V rtable	Specify alternate routing table
        -v		Verbose
        -W recvlimit	Terminate after receiving a number of packets
        -w timeout	Timeout for connects and final net reads
        -X proto	Proxy protocol: "4", "5" (SOCKS) or "connect"
        -x addr[:port]	Specify proxy address and port
        -Z		DCCP mode
        -z		Zero-I/O mode [used for scanning]
        Port numbers can be individual or ranges: lo-hi [inclusive]
        '''
    if simple:
        print(simple_usage)
    else:
        print(complex_usage)
    sys.exit(0)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hlvnp:')
    except getopt.GetoptError as ext:
        print(ext)
        Usage(True)

    for k,v in opts:
        if k in ('-h'):
            Usage(True)
        elif k in ('-l'):
            server_mode = True
        elif k in ('-n'):
            suppress_solution = True
        elif k in ('-p'):
            port = int(v)
        elif k in ('-v'):
            verbose = True
        else:
            # 大概是最简单的抛出异常方式
            assert 1==2, "Unhandled Options: {}".format(k)
    # 发送模式，处理一下后面的ip和port
    if len(args)>0:
        if len(args)== 1:
            dst_port = 80
        else:
            dst_port = args[1]
        dst_ip = args[0]
        def check_ip(address):
            dotnum = 0
            left = address
            while left.find('.')!=-1 :
                dotnum +=1
                left = left[left.find('.')+1:]
            if dotnum == 3:
                return True
            else:
                return False
        assert check_ip(dst_ip), "Wrong address."


if __name__ == '__main__':
    main()
