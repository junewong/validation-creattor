#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------------
# 
# 一个小型的web服务器，启动会打开同目录下的index.html文件
#
# @author junewong<wangzhu@ucweb.com>
# @date 2016-06-22
# --------------------------------------------------------------------------------

import os
import re
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
from mimetypes import types_map

CURRENT_PATH = os.path.dirname( os.path.realpath(__file__) ) 
WEB_PATH = CURRENT_PATH + "/web"
INDEX_FILE = WEB_PATH + "/index.html"
DATA_FILE = CURRENT_PATH + '/../tmp/data.txt'
KEY_DATA_CONTENT = '{{data-content}}'

#HOST = ""
HOST = "localhost"
PORT = 7755
url = ""


def read_file( filename ):
    content = ''
    if not os.path.exists( filename ):
        return content

    f = None
    try:
        f = open( filename, 'r' )
        content = f.read()
    except Exception as e:
        raise e
    finally:
        if f is not None:
            f.close()
    return content


class ServerHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        try:
            html = ''
            is_index = False

            if self.path == "favico.ico":
                return
            if self.path == "/":
                self.path = "/web/index.html"
                is_index = True

            fname, ext = os.path.splitext( self.path )
            if ext in ( ".html", ".css", ".js" ):
                self.send_response( 200 )
                self.send_header( 'Content-type', types_map[ext] )
                self.end_headers()
                html = read_file( CURRENT_PATH + self.path )
                if is_index:
                    data = read_file( DATA_FILE )
                    html = html.replace( KEY_DATA_CONTENT, data )
                self.wfile.write( html )
            return
        except IOError:
            self.send_error(404)
        
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        self._set_headers()
        self.wfile.write("<html><body><h1>提交成功!</h1></body></html>")
        pass
        
class Server():
    @staticmethod
    def run(server_class=HTTPServer, handler_class=ServerHandler, port=PORT):
        server_address = (HOST, port)
        httpd = server_class(server_address, handler_class)
        url = "http://" + HOST + ":" + str(PORT)
        print '启动代码生成器,请打开url:', url
        httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        Server.run(port=int(argv[1]))
    else:
        Server.run()

