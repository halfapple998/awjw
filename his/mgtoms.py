# coding=utf-8
from pymongo import MongoClient
from lib.libmysql import MYSQL
import lib.mod_config

client = MongoClient('localhost')
db = client['goods']

p = db['p20']
data = p.find()

# oi = db['oi20']
# data = oi.find()

dbconfig = lib.mod_config.getConfig()

# msyql dababase connection info
dbconn = MYSQL(
    dbhost=dbconfig['mysql']['dbhost'],
    dbport=dbconfig['mysql']['dbport'],
    dbuser=dbconfig['mysql']['dbuser'],
    dbpwd=dbconfig['mysql']['dbpwd'],
    dbname=dbconfig['mysql']['dbname'],
    dbcharset=dbconfig['mysql']['dbcharset'])

for v in data:
    dbconn.insert(table='p20', data=v)