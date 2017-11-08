#!/usr/bin/python
# coding:utf-8
# app/main.py

import logging
import sys
from .config import get_config
from telegram.ext import Updater

class Bot:
    PLUGINS = {}
    Config = {}
    
    @classmethod
    def plugin_register(cls, plugin_name):
        def wrapper(plugin):
            cls.PLUGINS.update({plugin_name:plugin})
            return plugin
        return wrapper
    
    def start_log(self):
        LEVELS = {"debug": logging.DEBUG,
                  "info": logging.INFO,
                  "warning": logging.WARNING,
                  "error": logging.ERROR,
                  "critical": logging.CRITICAL
                  }
        level = LEVELS[self.Config.get("log_level", "info")]
        logging.basicConfig(level=level, 
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
            filename="app.log", 
            filemode="a")
        console = logging.StreamHandler()
        console.setLevel(level)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
    
    def run(self):
        updater = Updater(token=self.Config["token"])
        dispatcher = updater.dispatcher
        for plugin in self.Config.keys():
            config = self.Config[plugin]
            if isinstance(config, dict) and config.get("enabled", True):
                if plugin in self.PLUGINS.keys():
                    self.PLUGINS[plugin]().init(updater, dispatcher, config)
                else:
                    logging.error("Cannot find plugin " + plugin)
                    sys.exit(1)
        updater.start_polling()

    def __init__(self):
        self.Config = get_config()
        self.start_log()
