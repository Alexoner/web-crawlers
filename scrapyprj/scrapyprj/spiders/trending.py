# -*- coding: utf-8 -*-
import scrapy
import os
import sys
from scrapyprj.items import ProxyInfo
from scrapyprj.utils import safe_extract, extract_url, trim, joinList
import json
import hashlib
import re
import time
from  datetime import datetime

class TrendingSpider(scrapy.Spider):
    name = "trending"
    allowed_domains = ["chicisimo.com"]

    def start_requests(self):
        urlMap = [
        {'url': 'https://chicisimo.com/', 'tag': 'c'},
        # {'url':'http://proxy.ipcn.org/proxya.html','tag':'proxya'}
        ]
        for url in urlMap:
            if url['tag']=='chicisimo':
                yield scrapy.Request(url['url'], callback = self.parse_chicisimo)

    def parse_chicisimo(self, response):
        hrefList  = response.xpath("//ul[@class='trends']/li/a")
        for i in range(0,len(hrefList)):
            url = hrefList[i].xpath("@href").extract()
            tag = hrefList[i].xpath("text()").extract()
            param ={'tag':tag}
            yield scrapy.Request("https://chicisimo.com"+url, callback = self.parse_chicisimo_detailseed, meta=param)

    def parse_chicisimo_detailseed(self, response):
        detailList = safe_extract(response.xpath("//div[contains(@class,'look')][@data-id]/@data-link"))
        if len(detailList) < 1:
            return

        #first generate url for detailpage
        for  i in range(0,len(detailList)):
            yield scrapy.Request("https://chicisimo.com"+detailList[i], callback = self.parse_chicisimo_detail, meta = response.meta)

        #then generate next page
        seed = detailList[len(detailList)-1]
        seed = seed.split("/")[2]
        url = response.url
        if 'limit' in response.url:
            url = url.split("?limit=")
        url = url + "?limit=12&last="+seed
        yield scrapy.Request(url,callback = self.parse_chicisimo_detailseed,meta = response.meta)

    def parse_chicisimo_detail(self, response):
        #user usrl
        url = safe_extract(response.xpath("//div[@class='look-author-details']/a/@href"))
        if url:
            yield scrapy.Request("https://chicisimo.com"+url, callback = self.parse_chicisimo_user)
        else:
            return
        timeStr = safe_extract(response.xpath("//time[@class='date']/@datetime"))
    	timeStamp = time.mktime(datetime.strptime(timeStr,'%Y-%m-%d %H:%M:%S')).timetuple()
        tags = safe_extract(response.xpath("//div[@class='hashtags']//a/text()"))
    	brands = safe_extract(response.xpath("//div[@class='hashtags-brands']//a/text()"))
    	#like count
    	likeStr = safe_extract(response.xpath("//span[@class='message-container']/span[contains(text(),'chics')]/parent::span/span[@class='counter']/text()"))
    	# add to cart count or save count
    	saveStr = safe_extract(response.xpath("//span[@class='message-container']/span[contains(text(),'save')]/parent::span/span[@class='counter']/text()"))
    	likeCount = 0
    	saveCount = 0
    	if likeStr:
    	    likeCount = int(likeStr)
    	if saveStr:
    	    saveStr = re.search(r'([\d]+)',saveStr).group(0)
    	    saveCount = int(saveStr)
    	tags = joinList(tags)
    	brands = joinList(brands)
    	pictureUrl = safe_extract(response.xpath("//img[@class='look-photo']/@src"))

    def parse_chicisimo_user(self, response):
    	followers = safe_extract(response.xpath("//a[contains(@href,'followers')]/text()"))
    	following = safe_extract(response.xpath("//a[contains(@href,'following')]/text()"))
    	followers = re.search(r'([\d]+)',followers)
    	following = re.search(r'([\d]+)',following)
    	username = safe_extract(response.xpath("//h3/text()"))








