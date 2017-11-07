#!/usr/bin/python
# coding:utf-8
# base.py

import sys
import json
import logging
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

Config = {}

def load_conf(conf = "config.json"):
	f = open(conf, "r")
	text = f.read()
	config = json.loads(text)
	f.close()
	nece_keys = ["token", "message"]
	for key in nece_keys:
		if not key in config.keys():
			print("Config file error")
			sys.exit(1)
	return config
	
def start(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text=Config["message"])
	
def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)
	
def main():
	Config = load_conf()
	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
	updater = Updater(token=Config["token"])
	dispatcher = updater.dispatcher
	start_handler = CommandHandler('start', start)
	dispatcher.add_handler(start_handler)
	echo_handler = MessageHandler(Filters.text, echo)
	dispatcher.add_handler(echo_handler)
	updater.start_polling()
	
if __name__ == "__main__":
    main()
