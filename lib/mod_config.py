#!/usr/bin/env python
# encoding: utf-8
import configparser
import os

conf_file = '/conf/qh.conf'


# 获取config配置文件
def getConfigOne(section, key):
    config = configparser.ConfigParser()
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config.read(path + conf_file)
    return config.get(section, key)


# 获取config配置文件
def getConfig():
    config = configparser.ConfigParser()
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config.read(path + conf_file)
    return config
