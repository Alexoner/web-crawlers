#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import requests

host = "http://www.europerail.cn"
index_req = {}
index_req['url'] = "{0}/timetable/indexsearch_result.aspx".format(host)
index_req['param'] = [
    [ 'fs', 'PARIS-巴黎(法国)' ],
    [ 'ts', 'MUNICH-慕尼黑(德国)' ],
    [ 'f', 'FRPAR|FR68600' ],
    [ 't', 'DEMUC|8000261' ],
    [ 'date', '2016-03-08' ],
    [ 'time', '01:00,23:00' ],
    [ 'anum', '1' ],
    [ 'ynum', '1' ],
    [ 'cnum', '0' ],
    [ 'snum', '0' ],
    [ 'pass', 'false' ],
]

def test_search():
    url = 'http://www.europerail.cn/timetable/inc/PTPSearch.aspx'
    params = [
        [ 'sid','20160308110920JyvF' ],# sid: 20160308110920JyvF
        [ 'f','FRPAR|FR68600', ], # from:
        [ 't','DEMUC|8000261', ], # to:
        [ 'date','2016-03-08', ], # departure date:yyyy-MM-dd
        [ 'time','01:00,23:00', ], # Time interval: 01:00,23:00
        [ 'anum','1', ], # adult number
        [ 'ynum','1', ], # youth number
        [ 'cnum','1', ], # child number
        [ 'snum','1', ], # senior number
        [ 'pass','false', ], # pass(TBD): false
        [ '_',int(1000*time.time()), ], # timestamp: 1457408226200
    ]
    response = requests.get(url, params, )
    print(response.text)

if __name__ == "__main__":
    test_search()
