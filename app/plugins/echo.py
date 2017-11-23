#!/usr/bin/python
# coding:utf-8
# app/plugin/echo.py

import logging
import os
import io,shutil,urllib
from http.server import HTTPServer,BaseHTTPRequestHandler
from ..main import Bot

@Bot.plugin_register('echo')
class Echo():

    class EchoHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            r_str="Empty Text!"
            if '?' in self.path:
                self.queryString=urllib.parse.unquote(self.path.split('?',1)[1])
                params=urllib.parse.parse_qs(self.queryString)
                if "text" in params:
                    r_str="Succeed"
                    print(type(params["text"][0]))
                    print(params["text"][0])
                    for chat_id in self.user:
                        self.bot.send_message(chat_id = chat_id, text = params["text"][0])
            encoded = ''.join(r_str).encode("UTF-8")
            f = io.BytesIO()
            f.write(encoded)
            f.seek(0)
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=UTF-8")
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            shutil.copyfileobj(f,self.wfile)
    
        def do_POST(self):
            s=str(self.rfile.readline(),"UTF-8")
            print(urllib.parse.parse_qs(urllib.parse.unquote(s)))
            self.send_response(301)
            self.send_header("Location", "/?"+s)
            self.end_headers()

    def init(self, updater, dispatcher, config):
        echo = self.EchoHandler
        echo.user = config.get("user", [])
        echo.bot = updater.bot
        port = config.get("port", 12586)
        if os.fork() > 0:
            return
        httpd = HTTPServer(('0.0.0.0', port), echo)
        httpd.serve_forever()
