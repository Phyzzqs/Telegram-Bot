#!/usr/bin/python
# coding:utf-8
# app/plugin/tuling.py

import requests
import logging
import sys
from telegram.ext import MessageHandler, Filters, CommandHandler
from ..main import Bot

@Bot.plugin_register('tuling')
class Tuling:
    key = ""
    api = "http://www.tuling123.com/openapi/api"
    botname = ""
    listen_group = False
    
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
            return re.get("text", "你在说什么，我听不清")
        elif re["code"] == 40004:
            logging.warn("The number of requests has been exhausted.")
            return "我累了，明天再聊"
        elif re["code"] == 40007:
            logging.warn("Data format is illegal.")
            return 1
        else:
            logging.warn("Unknown response code" + str(re["code"]))
            return 1
            
    def get_message(self, info, uid):
        userid = str(uid)
        data = {"key": self.key, "info": info, "userid": userid}
        re = requests.post(self.api, data = data).json()
        return self.deal(re)

    def process(self, bot, message, chat_id, uid, head=""):
        text = head + self.get_message(message, uid)
        if sys.version > "3":
            if isinstance(text, str):
                bot.send_message(chat_id=chat_id, text=text)
        else:
            if isinstance(text, unicode):
                bot.send_message(chat_id=chat_id, text=text)
    
    def chat(self, bot, update):
        head = ""
        if update.message.chat.type in ["group", "supergroup"]:
            if isinstance(update.message.from_user.username, str):
                head = "2"+update.message.from_user.username+""
        if update.message.text.find("/chat@"+self.botname) == -1:
            self.process(bot, update.message.text.lstrip("/chat"), 
                update.message.chat_id, 
                update.message.from_user.id,
                head)
        else:
            self.process(bot, update.message.text.lstrip("/chat@"+self.botname), 
                update.message.chat_id, 
                update.message.from_user.id,
                head)
            
    def echo(self, bot, update):
        if update.message.chat.type in ["group", "supergroup"]:
            self.process(bot, update.message.text, 
                update.message.chat_id, 
                update.message.from_user.id)
        elif self.listen_group:
            if isinstance(update.message.from_user.username, str):
                head = "2"+update.message.from_user.username+""
            if update.message.reply_to_message != None:
                if update.message.reply_to_message.from_user.username == self.botname:
                    self.process(bot, update.message.text, 
                        update.message.chat_id, 
                        update.message.from_user.id,
                        head)
            elif update.message.text.find("@"+self.botname) == 0:
                self.process(bot, update.message.text.lstrip("@"+self.botname), 
                    update.message.chat_id, 
                    update.message.from_user.id,
                    head)
        
    def init(self, updater, dispatcher, config):
        self.key = config["key"]
        if config["listen_group"]:
            if config.get("botname", "") == "":
                logging.warn("Bot name is needed to listen group")
            else:
                self.listen_group = True
                self.botname = config["botname"]
        echo_handler = MessageHandler(Filters.text, self.echo)
        dispatcher.add_handler(echo_handler)
        chat_handler = CommandHandler("chat", self.chat)
        dispatcher.add_handler(chat_handler)
