#!/usr/bin/python
# coding:utf-8
# app/plugin/execute.py

import logging
import os
import sys
import signal
from telegram.ext import CommandHandler
from ..main import Bot

@Bot.plugin_register('execute')
class Execute:
    
    def run(self, bot, update):
        command = update.message.text.lstrip("/run")
        if os.fork() > 0:
            return
        os.chdir("/")
        os.umask(0)
        os.setsid()
        if os.fork() > 0:
            sys.exit(0)
        try:
            pid = os.getpid()
            text = "程序已经开始运行，PID=" + str(pid)
            bot.send_message(chat_id = update.message.chat_id, text = text)
            os.chdir(self.work_dir)
            os.system(command)
            text = "程序运行结束，PID=" + str(pid)
            bot.send_message(chat_id = update.message.chat_id, text = text)
        except:
            text = "Unexpected error:", sys.exc_info()[0]
            bot.send_message(chat_id = update.message.chat_id, text = text)
            logging.error(text)
            sys.exit(1)
        sys.exit(0)
    
    def kill(self, bot, update):
        try:
            pid = int(update.message.text.lstrip("/kill"))
            os.kill(pid, signal.SIGKILL)
            bot.send_message(chat_id = update.message.chat_id, text = "程序已停止运行")
        except OSError as e:
            text = "OS Error: {0}".format(e)
            bot.send_message(chat_id = update.message.chat_id, text = text)
            logging.error(text)
        except:
            text = "Unexpected error:", sys.exc_info()[0]
            bot.send_message(chat_id = update.message.chat_id, text = text)
            logging.error(text)
    
    def init(self, updater, dispatcher, config):
        self.work_dir = config.get("work_dir", os.getcwd())
        run_handler = CommandHandler("run", self.run)
        dispatcher.add_handler(run_handler)
        kill_handler = CommandHandler("kill", self.kill)
        dispatcher.add_handler(kill_handler)
