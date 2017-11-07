#!/usr/bin/python
# coding:utf-8
# app/config.py

import json
import logging
import glob

def load(conf = "config.json"):
    f = open(conf, "r")
    text = f.read()
    config = json.loads(text)
    f.close()
    return config

def get_config(conf = "config.json"):
    default = load(conf)
    config = default.copy()
    json_list = list(glob.glob("conf.d/*.json"))
    for json in json_list:
        user = load(json)
        config.update(user)
    return config
