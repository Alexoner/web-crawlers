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
    	seedUrlList = [
    		{'url':'http://www.weixinyidu.com/a_958','name':'丁祖昱评楼市','source':'dzypls'},
    		{'url':'http://www.weixinyidu.com/a_970','name':'真叫卢俊的地产观','source':'zhenjiaolujun'},
    		{'url':'http://www.weixinyidu.com/a_2650','name':'地产八卦女','source':'dichanbaguanv'},
    		{'url':'http://www.weixinyidu.com/a_87979','name':'上海楼典','source':'shanghailord'},
    	]
    	for seed in seedUrlList:
    		yield scrapy.Request(seed['url'], callback=self.parse_seed,meta=seed)
    
    # def parse(self, response):
    # 	sel = scrapy.Selector(response)
    #  	for url in response.xpath("//div[@class='news_content']//li/a/@href").extract():
    #  		yield scrapy.Request(url, callback=self.parse_seed)
       

    def parse_seed(self,response):
    	"""parse seed to generate sublist"""
    	#get news list
    	paramData = response.meta
    	urlList = response.xpath("//div[@class='news_content']//li/a/@href").extract()
    	for url in urlList:
    		yield scrapy.Request('http://www.weixinyidu.com'+url,callback=self.parse_detail,meta = paramData)

    #generate newsItem from detail 
    def parse_detail(self,response):
    	#获取参数
    	paramData = response.meta

    	houseNews = HouseNewsItem()

    	houseNews['url'] = response.url
    	houseNews['source'] = paramData['source']
    	houseNews['author'] = paramData['name']
    	#标题
    	houseNews['title'] = response.xpath("//h1[@class='news_title']/text()").extract()[0]
    	print houseNews['title']
    	#时间
    	houseNews['release_time'] = response.xpath("//span[@class='news_time']/text()").extract()[0]
    	#阅读量
    	houseNews['read_count'] =response.xpath("//span[@class ='news_read_no']/text()").extract()[1]
    	#点赞量
    	houseNews['thumb_count'] =response.xpath("//span[@class ='news_read_no']/text()").extract()[2]
    	#关键词，热词
    	houseNews['keywords'] = response.xpath("//a[@class='hot_txt']/text()").extract()
    	yield houseNews


