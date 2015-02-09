#!/usr/bin/env python2
# -*- encoding:utf-8 -*-

import urllib
import urllib2
import time
from bs4 import BeautifulSoup
import re


def set_headers(base_url):
    """
    Set up headers to fake as a browser visit
    """
    urls = ['http://toy1.weather.com.cn/search?',
            'http://m.weather.com.cn/atad/',
            'http://m.weather.com.cn/data/',
            'http://d1.weather.com.cn/sk_2d/']

    headers  = {'http://toy1.weather.com.cn/search?':{
                        'Host': 'toy1.weather.com.cn',
                        'Connection': 'keep-alive',
                        'Accept': '*/*',
                        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36',
                        'Referer': 'http://www.weather.com.cn/',
                        'Accept-Encoding': 'gzip, deflate, sdch',
                        'Accept-Language': 'en-US,en;q=0.8'
                    },
            'http://m.weather.com.cn/atad/':{
                            'Host': 'm.weather.weather.com.cn',
                            'Connection': 'keep-alive',
                            'Cache-Control':'max-age=0',
                            'Accept': '*/*',
                            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36',
                            #('Referer', 'http://www.weather.com.cn/'),
                            'Accept-Encoding': 'gzip, deflate, sdch',
                            'Accept-Language': 'en-US,en;q=0.8'
            },
            'http://m.weather.com.cn/data/':{
                            'Host': 'm.weather.weather.com.cn',
                            'Connection': 'keep-alive',
                            'Cache-Control':'max-age=0',
                            'Accept': '*/*',
                            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36',
                            #('Referer', 'http://www.weather.com.cn/'),
                            'Accept-Encoding': 'gzip, deflate, sdch',
                            'Accept-Language': 'en-US,en;q=0.8'
            },
            'http://d1.weather.com.cn/sk_2d/':{
                            'Host': 'd1.weather.com.cn',
                            'Connection': 'keep-alive',
                            #('Cache-Control','max-age=0'),
                            'Accept': '*/*',
                            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36',
                            'Referer': 'http://www.weather.com.cn/weather1d/{0}.shtml',
                            'Accept-Encoding': 'gzip, deflate, sdch',
                            'Accept-Language': 'en-US,en;q=0.8'
            }
        }
    return headers[base_url]

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
    headers = set_headers(base_url)
    print "Request URL: "+ url
    req = urllib2.Request(url,data=None,headers=dict(headers))
    f = urllib2.urlopen(req)
    results = f.read()
    cities = parse_city(results)
    # print
    for city in cities:
        print "~".join(city)

    for city in cities:
        if city[6]!="":
            city_code = city[0]
            city_detail = get_city_detail(city_code)
            return city_detail
    return None

def parse_city(results):
    pattern_all = re.compile(r'[^[]*(\[.*\])')
    cities_str = pattern_all.findall(results)[0]
    pattern_cities = re.compile(r'(\{\".+?\":\".+?\"\})')
    cities = pattern_cities.findall(cities_str)
    pattern_city_info = re.compile(r':\"(.+?)\"')
    for i in xrange(len(cities)):
        cities[i] = pattern_city_info.findall(cities[i])[0].split('~')
    return cities

def get_city_detail(city_code):
    #try:
        #base_url = 'http://m.weather.com.cn/data/'
        #url = base_url + city_code + ".html"
        #print "Request URL: "+ url
        #headers = set_headers(base_url)
        ##data = None
        ##payload = urllib.urlencode(data)
        ##url = base_url + "{0}".format(payload)
        #req = urllib2.Request(url,data=None,headers=dict(headers))
        #f = urllib2.urlopen(req)
        #result = f.read()
        #return result
    #except BaseException,e:
        #print e

    print "previous URL doesn't work"
    base_url = "http://d1.weather.com.cn/sk_2d/"
    url = base_url + city_code + ".html?"
    headers = set_headers(base_url)
    headers['Referer'] = headers['Referer'].format(city_code)
    print headers
    data = [("_",str(int(time.time()*1000)))]
    payload = urllib.urlencode(data)
    url = url + "{0}".format(payload)
    print "Request URL: " + url
    req = urllib2.Request(url,data=None,headers=headers)
    f = urllib2.urlopen(req)
    print "HTTP Code: " + str(f.getcode()) + f.msg
    results = f.read()
    with open("/tmp/log","w") as fp:
        fp.write(results)
    return results


if __name__ == "__main__":
    city_detail = search_city_weather("扬州")
    print str(city_detail)
    #print search_city_weather("hangzhou").__class__
