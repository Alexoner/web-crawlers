#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Cookie
import datetime
import json
import random
import re
import time
import urllib
import scrapy
from ctripRails.spiders import utils
from ctripRails.items import  CtriprailsItem


class CtripSpider(scrapy.Spider):
    handle_httpstatus_list = [400, 404]
    name = "ctrip"
    allowed_domains = ["rails.ctrip.com"]
    start_urls = (
        'http://rails.ctrip.com/ptp/FRPAR-DEMUC?departureDate=2016-03-15&starttime=06:00-24:00&searchType=0&pageStatus=0&passHolders=0&adult=2&child=0&youth=0&seniors=0',
    )

    def parse(self, response):
        with open('/tmp/a.html', 'w') as f:
            f.write(response.body.decode(response.encoding).encode('utf-8'))

        print(response.headers)
        cookie = dict(response.headers)['Set-Cookie']
        ctripBFA = CtripBFA()
        print('bfa cookie: ', ctripBFA.bfa)
        cookie = '{};{}'.format(';'.join(cookie), ctripBFA.cookie)
        cookie = re.sub(
            r"(;expires=[^;]+)|(;domain=[^;]*)|(; ?path=[^;]*)|(HttpOnly;)",
            '',
            cookie)
        print('new cookie: {}'.format(cookie))
        #  self.logger.info('new pages\'cookie is {}'.format(cookie), '')
        simpleCookie = Cookie.SimpleCookie()
        simpleCookie.load(cookie)
        cookieDict = {}
        for key, morsel in simpleCookie.items():
            cookieDict[key] = morsel.value

        request = scrapy.FormRequest(
            'http://rails.ctrip.com/international/Ajax/PTPProductListHandler.ashx?Action=GetPTPProductList'.format(),
            formdata={'value': '{"adults":"2","children":"0","seniors":"0","youth":"0","departureDate":"2016-03-15","departureTimeHigh":"24:00","departureTimeLow":"06:00","fromCityCode":"FRPAR","toCityCode":"DEMUC","arriveDate":"","startCityName":"巴黎","destCityName":"慕尼黑","backTimeHigh":"12:00","backTimeLow":"06:00","passHolders":"0","searchType":"0","pageStatus":"0","data":null}'},
            callback=self.parse_item,
            method='POST',
            headers={
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                #  'Content-Length': 366, # computed wrong, don't use this header yet
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                #  'Cookie': 'ASP.NET_SessionSvc=MTAuOC45Mi4xNzJ8OTA5MHxqaW5xaWFvfGRlZmF1bHR8MTQ0OTEzNzUxNzEwMg; ASP.NET_SessionId=ofldmiolbnioxpjvjzon0v22; _bfa=1.1457853128485.3ik6k8.1.1457853128485.1457853128485.1.1; _bfs=1.1',
                'Host': 'rails.ctrip.com',
                'If-Modified-Since': 'Thu, 01 Jan 1970 00:00:00 GMT',
                'Origin': 'http://rails.ctrip.com',
                'Pragma': 'no-cache',
                'Referer': 'http://rails.ctrip.com/ptp/FRPAR-DEMUC?departureDate=2016-03-15&starttime=06:00-24:00&searchType=0&pageStatus=0&passHolders=0&adult=2&child=0&youth=0&seniors=0',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
            },
            cookies=cookieDict,
            #  meta=None,
            #  encoding='utf-8'
        )

        self.logger.info('', request)

        return request

    def parse_item(self, response):
        self.logger.info("Visited %s", response.url)
        data = response.body.decode(response.encoding).encode('utf-8')
        with open('/tmp/item.json', 'w') as f:
            f.write(data)

        item = CtriprailsItem(json.loads(data))

        return item


class CtripBFA(object):

    class C(object):

        @classmethod
        def getRand(cls):
            return (str(random.random()))[-8:]

        def CLI_getHash(self):
            q = 2  # f.history.length
            navigator = {
                'appCodeName': "Mozilla",
                'appName': "Netscape",
                'appVersion': "5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36",
                'cookieEnabled': 'true',
                'doNotTrack': 'null',
                'language': 'en-US',
                'platform': 'MacIntel',
                'userAgent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"
            }
            screen = {
                'width': 1920,
                'height': 1080,
            }
            page = {
                'cookie': '',
                'referer': '',
            }
            language = 'en-us'
            navigator_javaEnabled = 0
            d = '24-bit'
            n = ''.join(
                [
                    str(x) for x in
                    [
                        navigator['appName'],
                        navigator['appVersion'],
                        language,
                        navigator['platform'],
                        navigator['userAgent'],
                        navigator_javaEnabled,
                        screen['width'] + screen['height'],
                        d,
                        page['cookie'],
                        page['referer'],
                    ]
                ]
            )
            g = len(n)
            while q > 0:
                q -= 1
                g += 1
                n += str(q ^ g)

            return self.hash(n)

        @classmethod
        def hash(cls, a):
            b = 1
            d = 0
            if a:
                b = 0
                for e in range((len(a) - 1), -1, -1):
                    d = ord(a[e])
                    b = (b << 6 & 268435455) + d + (d << 14)
                    d = b & 266338304
                    b = (d and b ^ d >> 21 or b)

            return b

    def __init__(self):
        self.enterTime = int(time.time() * 1000)
        self.cookie = ''
        self.c = CtripBFA.C()
        self.bfa = []
        self.bfs = []

        self.readBfa()
        self.sessRead()
        #  self.readBfi()

    def uniqueId_(self):
        return int(self.c.getRand()) ^ self.c.CLI_getHash() & 2147483647

    def readBfa(self):
        a = self.enterTime
        self.bfa = [1, a, utils.str_base(self.uniqueId_(), 36), 1, a, a, 0, 0]
        return self.bfa

    def sessRead(self):
        self.bfs = [1, 1]
        self.bfa[4] = self.bfa[5]
        self.bfa[5] = self.enterTime
        self.bfa[6] = self.bfa[6] + 1
        self.bfa[7] = int(str(self.bfa[7]), 10) + 1
        self.sessWrite()

    def sessWrite(self):
        self.setItem('_bfa', '.'.join([str(x) for x in self.bfa]), 63072E6)
        self.setItem('_bfs', '.'.join([str(x) for x in self.bfs]), 18E5)

    def setItem(self, key, value, d):
        isSupportedCookie = 'key is Supported Cookie'
        if isSupportedCookie:
            self.setCookie(key, value, d)

    def setCookie(self, key, value, d):
        domain = ';domain=crip.com'
        if d >= 0:
            expire = ';expires=' + \
                datetime.datetime.utcfromtimestamp(time.time()).strftime(
                    "%a, %d %b %Y %H:%M:%S GMT")
        if self.cookie:
            self.cookie += ';' + key + '=' + \
                urllib.quote(value) + domain + ';path=/' + expire
        else:
            self.cookie = key + '=' + \
                urllib.quote(value) + domain + ';path=/' + expire
