#!/usr/bin/env python2
# -*- encoding:utf-8 *-*

import urllib
import urllib2
import time
from bs4 import BeautifulSoup

url_search = 'http://wiki.963110.com.cn/index.php?search-default'
url_news = 'http://www.963110.com.cn/wcm/index.php?m=content&c=index&a=lists&catid=7'

def query_crop(name=""):
    """
        查询农作物信息
    """
    #try:
    if name == "":
        return
    data = {"searchtext":"","full":"1"}
    data["searchtext"] = name
    payload = urllib.urlencode(data)
    req = urllib2.urlopen(url_search,payload)
    line = req.read()
    dump2file(line,"/tmp/log")
    extract_article(line)
    #except BaseException,e:
        #print e

def extract_article(page):
    if page is None:
        return None

    soup = BeautifulSoup(page)
    #print(soup.prettify().encode('utf-8'))
    wordcut = soup.find("div", {"class":"l w-710 o-v"}).find(
        "div",{"class":"content_1 wordcut"})
    article = wordcut.getText()
    print unicode(article)

def get_latest_news():
    req = urllib2.urlopen(url_news)
    page = req.read()
    dump2file(page,"/tmp/log")
    return extract_news(page)

def extract_news(page):
    if page is None:
        return None
    # build soup data structure of the page
    soup = BeautifulSoup(page)
    tag_ul = soup.find("ul",{"class":"list lh24 f14"})
    tags_li = tag_ul.find_all("li")
    results = []
    # time format codes according to "time" library
    time_format = "%Y-%m-%d %H:%M:%S"
    day_format = "%Y-%m-%d"
    date_day = time.strftime(day_format,time.localtime())
    for tag_li in tags_li:
        #print tag_li
        try:
            tag_span = tag_li.find("span")
            str_time = tag_span.get_text()
            time_stmp = time.strptime(str_time,time_format)
            tag_date = time.strftime(day_format,time_stmp)
            print tag_date,date_day
            if tag_date == date_day:
                results.append(repr(tag_li.find("a")))
            print tag_li.find("a")
        except BaseException as e:
            print e
    return results


def dump2file(data,filename):
    if data is not None and filename is not None:
        with open(filename,"w") as fp:
            fp.write(data)

if __name__ == "__main__":
    #query_crop("香蕉")
    for i in get_latest_news():
        print i
