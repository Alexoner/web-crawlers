# -*- coding: utf-8 -*-

import urlparse
import scrapy
from goose import Goose
from goose.text import StopWordsChinese


def safe_extract(selectorObj, separator='\t'):
    if isinstance(selectorObj, scrapy.selector.SelectorList):
        return separator.join(selectorObj.extract())
    elif isinstance(selectorObj, scrapy.selector.Selector):
        return selectorObj.extract()
    else:
        return selectorObj

def extract_article(url=None, raw_html=None):
    return extract_article.goose.extract(url=url, raw_html=raw_html).infos
extract_article.goose = Goose({'stopwords_class': StopWordsChinese})

def extract_url(response, selector):
    return urlparse.urljoin(response.url, safe_extract(selector))

def extract_after_colon_ch(uniObj, index):
    try:
        return uniObj and str(uniObj).split('：')[index].strip()
    except IndexError as e:
        return None
def trim(raw_str):
    raw_str = raw_str.replace('\r','')
    raw_str = raw_str.replace('\n','')
    raw_str = raw_str.replace('\t','')
    raw_str = raw_str.strip()
    return raw_str

