#!/usr/bin/python
# coding:utf-8

import sys
import json
import logging
from telegram.ext import Updater
from telegram.ext import CommandHandler

def load_conf(conf = "config.json"):
	f = open(conf, "r")
	text = f.read()
	config = json.loads(text)
	f.close()
	if (not "token" in config.keys()):
		print("Config file error")
		sys.exit(1)
	return config
	
def start(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="It's workinng!")
	
def main():
	config = load_conf()
	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
	updater = Updater(token=config["token"])
	dispatcher = updater.dispatcher
	start_handler = CommandHandler('start', start)
	dispatcher.add_handler(start_handler)
	updater.start_polling()
	
if __name__ == "__main__":
    main()
