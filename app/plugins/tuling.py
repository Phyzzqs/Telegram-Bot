#!/usr/bin/python
# coding:utf-8
# app/plugin/tuling.py

import requests
import hashlib
import logging
from telegram.ext import MessageHandler, Filters
from ..main import Bot

@Bot.plugin_register('Tuling')
class Tuling:
    
    key = ""
    api = "http://www.tuling123.com/openapi/api"
    
    def deal(self, re):
        if re["code"] == 100000:
            return re["text"]
        elif re["code"] == 200000:
            return re["url"]
        elif re["code"] == 302000:
            return re["text"]
        elif re["code"] == 308000:
            return re["text"]
        elif re["code"] == 40001:
            logging.warn("Invalid API key.")
            return 1
        elif re["code"] == 40002:
            logging.warn("Empty info.")
            return 1
        elif re["code"] == 40004:
            logging.warn("The number of requests has been exhausted.")
            return "我累了，明天再聊。"
        elif re["code"] == 40007:
            logging.warn("Data format is illegal.")
            return 1
        else:
            logging.warn("Unknown response code" + str(re["code"]))
            return 1
            
    def get_message(self, info, user_name):
        md5obj = hashlib.md5()
        md5obj.update(user_name.encode())
        userid = md5obj.hexdigest()
        data = {"key": self.key, "info": info, "userid": userid}
        re = requests.post(self.api, data = data).json()
        return self.deal(re)

        
    def echo(self, bot, update):
        text = self.get_message(update.message.text, update.message.from_user.username)
        if isinstance(text, str):
            bot.send_message(chat_id=update.message.chat_id, text=text)
        
    def process(self, updater, dispatcher, config):
        self.key = config["key"]
        echo_handler = MessageHandler(Filters.text, self.echo)
        dispatcher.add_handler(echo_handler)
