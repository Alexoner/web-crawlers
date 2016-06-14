# -*- coding: utf-8 -*-

import sys

PYTHON_VERSION = int(sys.version[0])

if PYTHON_VERSION == 3:
    from urllib.parse import urljoin
    import newspaper
else:
    import urlparse
    from goose import Goose
    from goose.text import StopWordsChinese
import scrapy
import json


# 招租帖子标题包含的关键词
letList = ['合租', '直租', '转租', '押一付三', '押一付一', '出租', '月付', '急转', '转', '招室友']

# 租房帖子题目包含的关键词
rentList = ['求租']
def safe_extract(selectorObj, separator='\t'):
    if isinstance(selectorObj, scrapy.selector.SelectorList):
        return separator.join(selectorObj.extract())
    elif isinstance(selectorObj, scrapy.selector.Selector):
        return selectorObj.extract()
    else:
        return selectorObj

# TODO: need implementation
def extract_article(url=None, raw_html=None):
    if PYTHON_VERSION == 3:
        raise NotImplementedError('Not implemented yet for python3!')
    return extract_article.goose.extract(url=url, raw_html=raw_html).infos
if PYTHON_VERSION == 3:
    pass
else:
    extract_article.goose = Goose({'stopwords_class': StopWordsChinese})

def extract_url(response, selector):
    return urljoin(response.url, safe_extract(selector))

def extract_after_colon_ch(uniObj, index):
    try:
        return uniObj and str(uniObj).split('：')[index].strip()
    except IndexError as e:
        return None
def trim(raw_str):
    raw_str = raw_str.replace('\r', '')
    raw_str = raw_str.replace('\n', '')
    raw_str = raw_str.replace('\t', '')
    raw_str = raw_str.strip()
    return raw_str

# 判断是否是租房帖子
def isRent(raw_str):
    # 招租在标题上包含的关键词
    for letStr in letList:
        if letStr in raw_str:
            return False

    for rentStr in rentList:
        if rentStr in raw_str:
            return True

def getExistList(file_name):
    lines = open(file_name).readlines()
    existList = []
    for line in lines:
        line = json.dumps(line)
        jsonObj = json.loads(line)
        print (jsonObj)
        existList.append(jsonObj['url'])
    print (existList)
    return existList

def getProvince_City(file_name):
    lines = open(file_name).readlines()
    cityList = []
    for line in lines:
        provinceMap = {}
        obj = json.loads(line)
        provinceMap['province'] = obj['provinceName']
        cityObjs = []
        for city in obj['cityList']:
            tmpMap = {}
            tmpMap['city'] = city['cityName']
            tmpMap['code'] = city['cityCode']
            cityObjs.append(tmpMap)
        provinceMap['cityList'] = cityObjs
        cityList.append(provinceMap)
    return cityList

if __name__ == "__main__":
    mapList = getExistList(
        '/Users/xueliang.xl/work/getter/2016-05-24/output/xiaoqu_changsha.json')
    for line in mapList:
        print (line)
        print ('-----------------')
