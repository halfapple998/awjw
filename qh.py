#!/usr/bin/Python
import urllib.request
from lib.libmysql import MYSQL
import lib.mod_config

catemap = {
    'oi': 'http://hq.sinajs.cn?list=OI2105',
    'p': 'http://hq.sinajs.cn?list=P2105',
    'rb': 'http://hq.sinajs.cn?list=RB2105',
}


def Run(cate, tid):
    url = catemap[cate]

    req = urllib.request.Request(url)

    res_data = urllib.request.urlopen(req)
    res = res_data.read().decode('UTF-8', "ignore").split("\"")[1].split(",")
    return {
        'pc': res[8],
        'pa': res[13],
        'pt': res[14],
        'tid': tid,
    }


class Qh:
    def __init__(self):
        self.dbconfig = lib.mod_config.getConfig()

        # msyql dababase connection info
        self.dbconn = MYSQL(
            dbhost=self.dbconfig['mysql']['dbhost'],
            dbport=self.dbconfig['mysql']['dbport'],
            dbuser=self.dbconfig['mysql']['dbuser'],
            dbpwd=self.dbconfig['mysql']['dbpwd'],
            dbname=self.dbconfig['mysql']['dbname'],
            dbcharset=self.dbconfig['mysql']['dbcharset'])

    def RunTime(self):
        data = {
            't': 1,
        }
        return str(self.dbconn.insert(table='t', data=data))

    def RunOI(self, tid):
        data = Run('oi', tid)
        return str(self.dbconn.insert(table='oi', data=data))

    def RunP(self, tid):
        data = Run('p', tid)
        return str(self.dbconn.insert(table='p', data=data))

    def RunRB(self, tid):
        data = Run('rb', tid)
        return str(self.dbconn.insert(table='rb', data=data))

    def RunOIP(self, tid):
        dataOI = Run('oi', tid)
        dataP = Run('p', tid)

        pc = float(dataOI['pc']) - float(dataP['pc'])
        print(dataOI['pc'])
        print(dataP['pc'])
        print(pc)
        data = {
            'pc': pc,
            'tid': tid,
        }
        return str(self.dbconn.insert(table='oip', data=data))
