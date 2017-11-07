#!/usr/bin/python
# coding:utf-8
# base.py

import sys
import config
import logging
from tuling import Tuling
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

Config = config.get_config()
    
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=Config["message"])
    
def echo(bot, update):
    key = Config["tuling"]
    tuling = Tuling(key)
    text = tuling.get_message(update.message.text, update.message.from_user.username)
    if isinstance(text, str):
        bot.send_message(chat_id=update.message.chat_id, text=text)
    
def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    updater = Updater(token=Config["token"])
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    echo_handler = MessageHandler(Filters.text, echo)
    dispatcher.add_handler(echo_handler)
    updater.start_polling()
    
if __name__ == "__main__":
    main()
