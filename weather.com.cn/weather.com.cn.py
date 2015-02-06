#!/usr/bin/env python2
# -*- encoding:utf-8 *-*

import urllib
import urllib2
import time
from bs4 import BeautifulSoup


def set_headers():
    """
    Set up headers to fake as a browser visit
    """
    headers  = [('Host', 'toy1.weather.com.cn'),
                ('Connection', 'keep-alive'),
                ('Accept', '*/*'),
                ('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36'),
                ('Referer', 'http://www.weather.com.cn/'),
                ('Accept-Encoding', 'gzip, deflate, sdch'),
                ('Accept-Language', 'en-US,en;q=0.8')
                ]
    return headers

def search_city_weather(cityname="yangzhou"):
    """
    This is a cross-site request.
    @cityname:search cityname
    @callback:callback function
    @_:time stamp in micro-seconds
    """
    base_url = "http://toy1.weather.com.cn/search?"
    url = "http://toy1.weather.com.cn/search?cityname=%E6%9D%AD%E5%B7%9E&callback=success_jsonpCallback&_="+str(int(time.time()*1000))
    data = [("cityname",cityname),
            ("callback","success_jsonpCallback"),
            ("_",str(int(time.time()*1000)))]
    payload = urllib.urlencode(data)
    url = base_url + "{0}".format(payload)
    headers = set_headers()
    req = urllib2.Request(url,data=None,headers=dict(headers))
    f = urllib2.urlopen(req)
    page = f.read()
    return page


if __name__ == "__main__":
    print search_city_weather("hangzhou")
