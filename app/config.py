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
    config = load(conf)
    json_list = list(glob.glob("conf.d/*.json"))
    for json in json_list:
        user = load(json)
        config = {**config, **user}
    return config
