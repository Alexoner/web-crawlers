# -*- coding: utf-8 -*-
import os
import sys
import scrapy
from scrapyprj.items import HouseNewsItem

reload(sys)
sys.setdefaultencoding('utf-8')

class HousenewsspiderSpider(scrapy.Spider):
    
    name = "houseNewsSpider"
    allowed_domains = ["weixinyidu.com"]

   	# start_urls = [
    #    'http://www.weixinyidu.com/a_958',
    #    'http://www.weixinyidu.com/a_970',
    #    'http://www.weixinyidu.com/a_2650',
    #    'http://www.weixinyidu.com/a_87979'
    # ]

    def start_requests(self):
    	seedUrlList = ['http://www.weixinyidu.com/a_958','http://www.weixinyidu.com/a_970','http://www.weixinyidu.com/a_2650','http://www.weixinyidu.com/a_87979']
    	for url in seedUrlList:
    		yield scrapy.Request(url, callback=self.parse_seed)
    
    # def parse(self, response):
    # 	sel = scrapy.Selector(response)
    #  	for url in response.xpath("//div[@class='news_content']//li/a/@href").extract():
    #  		yield scrapy.Request(url, callback=self.parse_seed)
       

    def parse_seed(self,response):
    	"""parse seed to generate sublist"""
    	#get news list
    	urlList = response.xpath("//div[@class='news_content']//li/a/@href").extract()
    	for url in urlList:
    		yield scrapy.Request('http://www.weixinyidu.com'+url,callback=self.parse_detail)

    #generate newsItem from detail 
    def parse_detail(self,response):
    	houseNews = HouseNewsItem()
    	#标题
    	houseNews['title'] = response.xpath("//h1[@class='news_title']/text()").extract()[0]
    	print houseNews['title']
    	#时间
    	#houseNews['releaseTime'] = response.xpath("//span[@class='news_time']/text()").extract()[0]
    	#阅读量
    	#houseNews['readCount'] =response.xpath("//div[@class='left']/span[@class = 'news_read_no'][2]").extract()[0]
    	#点赞量
    	#houseNews['thumbCount'] =response.xpath("//div[@class='right']/span[@class = 'news_read_no'][1]").extract()[0]
    	#关键词，热词
    	#houseNews['keywords'] = response.xpath("//a[@class='hot_txt']/text()").extract()
    	yield houseNews


