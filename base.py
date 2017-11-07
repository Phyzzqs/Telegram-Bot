#!/usr/bin/python
# coding:utf-8
# base.py

import sys
import json
import logging
import requests
import hashlib
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

Config = {}

class Tuling:
    key = ""
    api = "http://www.tuling123.com/openapi/api"
    
    def __init__(self, key):
        self.key = key
    
    def get_message(self, info, user_name):
        md5obj = hashlib.md5()
        md5obj.update(user_name.encode())
        userid = md5obj.hexdigest()
        data = {"key": self.key, "info": info, "userid": userid}
        re = requests.post(self.api, data = data).json()
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

def load_conf(conf = "config.json"):
    f = open(conf, "r")
    text = f.read()
    config = json.loads(text)
    f.close()
    nece_keys = ["token", "message", "tuling"]
    for key in nece_keys:
        if not key in config.keys():
            logging.error("Config file error.")
            sys.exit(1)
    return config
    
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=Config["message"])
    
def echo(bot, update):
    key = Config.get("tuling")
    tuling = Tuling(key)
    text = tuling.get_message(update.message.text, update.message.from_user.username)
    if isinstance(text, str):
        bot.send_message(chat_id=update.message.chat_id, text=text)
    
def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    Config = load_conf()
    updater = Updater(token=Config["token"])
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    echo_handler = MessageHandler(Filters.text, echo)
    dispatcher.add_handler(echo_handler)
    updater.start_polling()
    
if __name__ == "__main__":
    main()
