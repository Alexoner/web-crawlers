# -*- coding: utf-8 -*-
import scrapy
import os
import sys
import time
from scrapyprj.items import AreaStaticEntity
from scrapyprj.utils import safe_extract, extract_article, extract_url, trim, getProvince_City, getExistList
import json
import hashlib
import re
import time
reload(sys)
sys.setdefaultencoding('utf-8')

class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["douban.com"]
    #获取当前月、日、小时
    monthStr = time.localtime(time.time()).tm_mon
    dayStr = time.localtime(time.time()).tm_mday
    hourStr = time.localtime(time.time()).tm_hour 
    #获取小组入后信息
    def start_requests(self):
    	mapList = []
    	group1 ={'url':'https://www.douban.com/group/145219/','name':'杭州 出租 租房 中介免入','city':'杭州'}
    	# group2 ={'url':'https://www.douban.com/group/HZhome/','name':'杭州租房','city':'杭州'}
    	# group3 ={'url':'https://www.douban.com/group/467221/','name':'杭州租房（出租、求租、合租）','city':'杭州'}
    	mapList.append(group1)
    	# mapList.append(group2)
    	# mapList.append(group3)
    	for url in mapList:
    		print url 
    		yield scrapy.Request(url['url'],callback = self.parse_nextAndSub,meta = url)

    #获得detail的数据和下一页，翻页的标准是如果最后更新日期小于小于今天，那么终止
    def parse_nextAndSub(self,response):
    	print 
    	#首先获得时间列表，获得该列表的下级数据做分发
    	timeList = safe_extract(response.xpath("//td[@nowrap = 'nowrap'][@class='time']"))
    	for i in range(1,len(timeList)+1):
    		timeStr = timeList[i - 1]
    		try:
    			#获得最后更新日期数据，抽取出月、日、小时
    			monStr = timeStr.split(" ")[0].strip().split('-')[0].strip()
    			if monStr.startswith('0'):
    				monStr = monStr.replace('0','').strip()
    			dStr = timeStr.split(" ")[0].strip().split('-')[1].strip()
    			if dStr.startswith('0'):
    				dStr = dStr.replace('0','').strip()

    			hStr = timeStr.split(" ")[1].strip().split(':')[0].strip()
    			if hStr.startswith('0'):
    				hStr = hStr.replace('0','').strip()

    			intMonth = int(monStr)
    			intDay = int(dStr)
    			intHour = int(hStr)
    			#只爬取当天和两个小时以内的数据
    			if self.monthStr == intMonth and self.dayStr == intDay:
    				if abs(intHour - self.hourStr) <= 2:

    					#如果最后一条的日期OK，那么翻页，否则不翻页
    					if i == len(timeList):
    						try:
    							if "start" in response.url:
    								offset = re.search(r'start=([\d]*)',response.url).group(1)
    								intOffset = int(offset)
    								intOffset += 25
    								newUrl = response.url.split('=')[0]+'='+str(intOffset)
    							else:
    								newUrl = response.ur +"discussion?start=50"
    							yield scrapy.Request(newUrl,callback = self.parse_nextAndSub,meta = response.meta)
    						except Exception as e:
    							print e
    							print response.url

    					#帖子链接、标题
    					url = safe_extract(response.xpath("//table[@class='olt']//tr["+str(i+1)+"]//td[@class='title']/a/@href"))
    					title = safe_extract(response.xpath("//table[@class='olt']//tr["+str(i+1)+"]//td[@class='title']/a/text()"))

    					#作者
    					author = safe_extract(response.xpath("//table[@class='olt']//tr["+str(i+1)+"]//td[2]/a/text()"))
    					authorUrl = safe_extract(response.xpath("//table[@class='olt']//tr["+str(i+1)+"]//td[2]/a/@href"))

    					#回帖人数
    					replyNum = safe_extract(response.xpath("//table[@class='olt']//tr["+str(i+1)+"]//td[3]/text()"))
    					
    					param ={}
    					param['title'] = title
    					param['author'] = author
    					param['authorUrl'] = authorUrl
    					param['replyNum'] = replyNum
    					param['latestTime'] = timeStr 
    					yield scrapy.Request(url,callback = parse_detail,meta = param)
    				else:
    					continue
    		except Exception as e:
    			print e
    			print response.ur,i


    def parse_detail(self,response):
    	pass