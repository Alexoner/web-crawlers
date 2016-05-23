# -*- coding: utf-8 -*-
import scrapy
import os
import sys
import time
from scrapyprj.items import AreaStaticEntity
from scrapyprj.utils import safe_extract, extract_article, extract_url, trim
import json
import hashlib
import re
reload(sys)
sys.setdefaultencoding('utf-8')

import scrapy
class ChuzuSpider(scrapy.Spider):
    name = "chuzu"
    allowed_domains = ["58.com"]

    prefix = 'hz'
    def start_requests(self):
        start = 'http://'+prefix+'.58.com/chuzu/0/pn1/'
        yield scrapy.Request(start, callback = self.parse_nextAndSub)

    def parse_nextAndSub(self, response):
        urlList = response.xpath("//tr/td/a[@class='t']/@href").extract()
        if (urlList and len(urlList) > 2):
            nextPage = re.search(r'/pn(\d+)/',response.url).group(1)
            num = int(nextPage)
            num += 1
            nextUrl = 'http://' + prefix+'.58.com/chuzu/0/pn'+str(num)
            yield scrapy.Request(nextUrl,callback = self.parse_nextAndSub)
        for i in range(1,len(urlList)+1):
            url =  safe_extract(response.xpath("//tr["+str(i)+"]/td/a[@class='t']/@href"))
            title = safe_extract(response.xpath("//tr["+str(i)+"]/td/a[@class='t']/text()"))
    def parse_detail(self, response):
        #坐标
        localList = re.search(r'locallist:\[({.*?)\]',response.body).group(1)
        if localList:
            localList = '['+ localList + ']'
            localList = re.sub(r'(,?)(\w+?)\s*?:', r'\1"\2":',localList)
            localList = json.dumploas(localList)








