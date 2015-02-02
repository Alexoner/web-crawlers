#!/usr/bin/env python2
# -*- encoding:utf-8 *-*

import urllib
import urllib2

url_search = 'http://wiki.963110.com.cn/index.php?search-default'

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

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(page)
    #print(soup.prettify().encode('utf-8'))
    wordcut = soup.find("div", {"class":"l w-710 o-v"}).find(
        "div",{"class":"content_1 wordcut"})
    article = wordcut.getText()
    print unicode(article)



def dump2file(data,filename):
    if data is not None and filename is not None:
        with open(filename,"w") as fp:
            fp.write(data)

if __name__ == "__main__":
    query_crop("香蕉")
