#!/usr/bin/Python
import urllib.request
from lib.libmysql import MYSQL
import lib.mod_config

catemap = {
    'oi': 'http://hq.sinajs.cn?list=OI2105',
    'p': 'http://hq.sinajs.cn?list=P2105',
    'rb': 'http://hq.sinajs.cn?list=RB2105',
    'jd01': 'http://hq.sinajs.cn?list=JD2201',
    'jd05': 'http://hq.sinajs.cn?list=JD2105',
    'jd09': 'http://hq.sinajs.cn?list=JD2109',
    'fg05': 'http://hq.sinajs.cn?list=FG2105',
    'fg09': 'http://hq.sinajs.cn?list=FG2109',
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
        print(str(dataOI['pc']) + ' ' + str(dataP['pc']) + ' ' + str(pc))

        data = {
            'pc': pc,
            'tid': tid,
        }
        return str(self.dbconn.insert(table='oip', data=data))

    def RunJD01(self, tid):
        data = Run('jd01', tid)
        return str(self.dbconn.insert(table='jd01', data=data))

    def RunJD05(self, tid):
        data = Run('jd05', tid)
        return str(self.dbconn.insert(table='jd05', data=data))

    def RunJD09(self, tid):
        data = Run('jd09', tid)
        return str(self.dbconn.insert(table='jd09', data=data))

    def RunJD(self, tid):
        dataJD01 = Run('jd01', tid)
        dataJD05 = Run('jd05', tid)
        dataJD09 = Run('jd09', tid)

        self.dbconn.insert(table='jd01', data=dataJD01)
        self.dbconn.insert(table='jd05', data=dataJD05)
        self.dbconn.insert(table='jd09', data=dataJD09)

        pc = float(dataJD09['pc']) - float(dataJD05['pc'])
        print(str(dataJD09['pc']) + ' ' + str(dataJD05['pc']) + ' ' + str(pc))

        data = {
            'pc': pc,
            'tid': tid,
        }
        return str(self.dbconn.insert(table='jd59', data=data))

    def RunFG(self, tid):
        dataFG05 = Run('fg05', tid)
        dataFG09 = Run('fg09', tid)


        self.dbconn.insert(table='fg05', data=dataFG05)
        self.dbconn.insert(table='fg09', data=dataFG09)

        pc = float(dataFG09['pc']) - float(dataFG05['pc'])
        print(str(dataFG09['pc']) + ' ' + str(dataFG05['pc']) + ' ' + str(pc))

        data = {
            'pc': pc,
            'tid': tid,
        }
        return str(self.dbconn.insert(table='fg59', data=data))