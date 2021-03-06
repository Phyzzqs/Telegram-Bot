#!/usr/bin/python
# coding:utf-8
# app/plugins/base.py

from telegram.ext import CommandHandler
from ..main import Bot

@Bot.plugin_register("base")
class Base:
    
    message = ""
        
    def start(self, bot, update):
        bot.send_message(chat_id = update.message.chat_id, text = self.message)
        
    def init(self, updater, dispatcher, config):
        self.message = config["message"]
        start_handler = CommandHandler("start", self.start)
        dispatcher.add_handler(start_handler)
    
