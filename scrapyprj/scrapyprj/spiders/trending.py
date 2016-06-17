# -*- coding: utf-8 -*-
import scrapy
import os
import sys
from scrapyprj.items import TrendUser, TrendTag
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
        #{'url': 'https://chicisimo.com/', 'tag': 'chicisimo'},
        # {'url':'http://proxy.ipcn.org/proxya.html','tag':'proxya'}
        #
        {'url':'https://chicisimo.com/popular','tag':'chicisimo'}
        ]
        for url in urlMap:
            if url['tag']=='chicisimo':
                yield scrapy.Request(url['url'], callback = self.parse_chicisimo_detailseed)

    def parse_chicisimo(self, response):
        hrefList  = response.xpath("//ul[@class='trends']/li/a")
        for i in range(0,len(hrefList)):
            url = safe_extract(hrefList[i].xpath("@href"))
            tag = safe_extract(hrefList[i].xpath("text()"))
            param ={'tag':tag}
            print ('home->generate:https://chicisimo.com',url)
            yield scrapy.Request("https://chicisimo.com"+url, callback = self.parse_chicisimo_detailseed, meta=param)

    def parse_chicisimo_detailseed(self, response):
        detailList = response.xpath("//div[contains(@class,'look')][@data-id]/@data-link").extract()
        if len(detailList) < 1:
            return

        #first generate url for detailpage
        for  i in range(0,len(detailList)):
            print ("generate detail ->>>>",detailList[i])
            yield scrapy.Request("https://chicisimo.com"+detailList[i], callback = self.parse_chicisimo_detail, meta = response.meta)

        #then generate next page
        seed = detailList[len(detailList)-1]
        print ('--------------last seed is :',seed)
        seed = seed.split("/")[2]
        url = response.url
        if 'limit' in response.url:
            url = url.split("?limit=")[0]
        url = url + "?limit=12&last="+seed
        print ("generate next page is :",url)
        yield scrapy.Request(url,callback = self.parse_chicisimo_detailseed,meta = response.meta)

    def parse_chicisimo_detail(self, response):
        #user usrl
        url = safe_extract(response.xpath("//div[@class='look-author-details']/a/@href"))
        if url:
            yield scrapy.Request("https://chicisimo.com"+url, callback = self.parse_chicisimo_user)
        else:
            return
        timeStr = safe_extract(response.xpath("//time[@class='date']/@datetime"))
        timeStr = timeStr.replace("T"," ")
        timeStr = timeStr.replace("Z","")
    	timeStamp = time.mktime(datetime.strptime(timeStr,'%Y-%m-%d %H:%M:%S').timetuple())
        tags = response.xpath("//div[@class='hashtags']//a/text()").extract()
    	brands = response.xpath("//div[@class='hashtags-brands']//a/text()").extract()
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
        print ("tags to be formate",tags)
    	tags = joinList(tags)
    	brands = joinList(brands)
    	pictureUrl = safe_extract(response.xpath("//img[@class='look-photo']/@src"))
        name = response.xpath("//p[@class='look-caption']/text()").extract()
        print ("first ->",name)
        nameStr = ''
        if name:
            nameStr = name[0]
        else:
            name = response.xpath("//p[@class='look-caption']//a/text()").extract()
            print ("second name->",name)
            nameStr = joinList(name)
        print ("nameStr->>>",nameStr)
        result = TrendTag()
        result['db_name'] = 'trendtag'
        result['user_name'] =  url.split("/")[1]
        result['last_time'] = time.time()
        result['tags'] = tags
        result['brands'] = brands
        result['picture_urls'] = pictureUrl
        result['like_count'] = likeCount
        result['save_count'] = saveCount
        result['id'] = hashlib.md5(response.url).hexdigest()
        result['name'] = nameStr
        result['url'] = response.url
        yield result

    def parse_chicisimo_user(self, response):
    	followers = safe_extract(response.xpath("//a[contains(@href,'followers')]/text()"))
    	following = safe_extract(response.xpath("//a[contains(@href,'following')]/text()"))
    	followers = re.search(r'([\d]+)',followers).group(1)
    	following = re.search(r'([\d]+)',following).group(1)
    	username = response.xpath("//h3/text()").extract()
    	userStr = ''
    	if username:
    		userStr = username[0]
        result = TrendUser()
        result['name'] = userStr
        result['id'] = hashlib.md5(response.url).hexdigest()
        result['followers'] = followers
        result['followings'] = following
        result['url'] = response.url
        yield result










