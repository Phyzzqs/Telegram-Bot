#!/usr/bin/python
# coding:utf-8
# app/config.py

import json
import logging
import sys
import glob

defaultconf = sys.path[0]+"/config.json"

def load(conf = defaultconf):
    f = open(conf, "r")
    text = f.read()
    config = json.loads(text)
    f.close()
    return config

def get_config(conf = defaultconf):
    default = load(conf)
    config = default.copy()
    json_list = list(glob.glob("conf.d/*.json"))
    for json in json_list:
        user = load(json)
        config.update(user)
    return config
