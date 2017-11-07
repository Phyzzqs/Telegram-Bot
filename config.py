#!/usr/bin/python
# coding:utf-8
# config.py

import json
import logging

def load(conf = "config.json"):
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
