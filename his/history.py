# coding=utf-8
from __future__ import print_function, absolute_import
from gm.api import *
from pymongo import MongoClient
if __name__ == '__main__':
    token = 'a560536039a194786d5f9d68949a5d97f8f22041'

    set_token(token)
    # DCE.p2105 CZCE.OI105
    datas = history(symbol='DCE.p2005', frequency='60s', start_time='2019-12-05', end_time='2020-05-01',
                   fields='close,high,low,volume,bob,eob', skip_suspended=True, fill_missing=None, adjust=0,
                   adjust_end_time='', df=True)
    # print(datas)
    # print(type(datas))
    data = datas.to_dict(orient='records')
    # print(datas)
    # for data in datas:
    #     print(datas.values.tolist())

    client = MongoClient('localhost')
    db = client['goods']
    p = db['p20']
    result = p.insert_many(data)