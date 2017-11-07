#!/usr/bin/python
# coding:utf-8
# app/main.py

import logging
import sys
from .config import get_config
from telegram.ext import Updater
#from plugins import *

class Bot:
    PLUGINS = {}
    
    Config = {}
    
    @classmethod
    def plugin_register(cls, plugin_name):
        def wrapper(plugin):
            cls.PLUGINS.update({plugin_name:plugin})
            return plugin
        return wrapper
    
    def __init__(self):
        self.Config = get_config()
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        updater = Updater(token=self.Config["token"])
        dispatcher = updater.dispatcher
        for plugin in self.Config.keys():
            config = self.Config[plugin]
            if isinstance(config, dict) and config.get("enabled", True):
                if plugin in self.PLUGINS.keys():
                    self.PLUGINS[plugin]().process(updater, dispatcher, config)
                else:
                    logging.error("Cannot find plugin " + plugin)
                    sys.exit(1)
        updater.start_polling()
