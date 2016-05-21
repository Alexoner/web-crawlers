# -*- coding: utf-8 -*-
import scrapy
import os
import sys
import time
from scrapyprj.items import AreaStaticEntity
from scrapyprj.utils import safe_extract,extract_article,extract_url
import json

reload(sys)
sys.setdefaultencoding('utf-8')

class WubatongchengSpider(scrapy.Spider):
    name = "wubatongcheng"
    allowed_domains = ["58.com"]
    start_urls = (
        'http://www.58.com/',
    )
    def start_requests(self):
        start = 'http://sz.58.com/xiaoqu/pn_1'
        yield scrapy.Request(start,callback = self.parse_nextAndSub)

    def parse_nextAndSub(self,response):
        urlList = response.xpath("//ul/li[@class='tli1']/a/@href").extract()
        #满20页，可以进行下一页
        if (urlList and  len(urlList)==20):
            nextPage = response.url.split('_')[1]
            num = int(nextPage)
            num +=1
            nextUrl = 'http://sz.58.com/xiaoqu/pn_'+str(num)
            yield scrapy.Request(nextUrl,callback = self.parse_nextAndSub)
        #详细内容
        areaList = response.xpath("//table[@class='tbimg']//tr").extract()
        for blockinfo in areaList:
            url = blockinfo.xpath("//ul/li[@class='tli1']/a/@href").extract()
            second_num = blockinfo.xpath("//ul/li[@class='tli3'][1]/span[1]/text()").extract()
            rend_num = blockinfo.xpath("//ul/li[@class='tli3'][1]/span[1]/text()").extract()
            money = blockinfo.xpath("//p/b[@class='money']/text()").extract()
            metaData = {}
            metaData['second_num'] = second_num
            metaData['rend_num'] = rend_num
            money ['money'] = money
            yield scrapy.Request(url,callback = self.parse_detail,meta = metaData)

   #解析detail
    def parse_detail(self,response):
        param = response.meta
        url = response.url
        second_num = param['second_num']
        rend_num = param['rend_num']
        money = param['money']
        name = safe_extract(response.xpath("//h1[@class='xiaoquh1']/text()"))
        alias_name = safe_extract(response.xpath("//h1[@class='xiaoquh1']/span/text()"))
        if alias_name:
            alias_name = alias_name.replase('(',"")
            alias_name = alias_name.replase(')',"")
            alias_name = alias_name.strip()
	#省市和坐标
        locationInfo = safe_extract(response.xpath("//meta[@name='location']/@content"))
        province = '广东'
        city = '深圳'
        longitude = ''
        latitude = ''
        if locationInfo:
            tmpList = locationInfo.split(";")
            for i in (range(0,len(tmpList))):
                if i == 0:
                    province = tmpList[0].split("=")[1]
                if i == 1:
                    city = tmpList[1].split("=")[1]
                if i == 2:
                    longitude = tmpList[2].split('=')[1].split(",")[0]
                    latitude = tmpList[2].split('=').split(",")[1]

	#区和小区
	area = ''
        subarea = ''
        areaList = safe_extract(response.xpath("//dl[@class='bhrInfo']/dd[2]//a[contains(@href,'xiaoqu')]/text()"))
        if areaList:
            for i in range(0,len(areaList)):
                if i== 0:
                    area = areaList[0]
                if i == 1:
                    subarea = areaList[1]
                    break
	# 地址和邮编
        address = safe_extract(response.xpath("//span[@class='ddinfo']/a[contains(@href,'xiaoqu')]/parent::span/text()"))
        postcode = safe_extract(response.xpath("//dd/span[contains(text(),'小区邮编')]/parent::dd/text()"))

	#建筑年代和类型
	year_type = safe_extract(response.xpath("//dd/span[contains(text(),'建筑年代')]/parent::dd/text()"))
        year = ''
        type = ''
        if year_type:
            for i in (range(0,len(year_type))):
                if i == 0:
                    year = year_type[0]
                if i == 1:
                    type = year_type[1]

	#物业费
        wuyeMoney = safe_extract(response.xpath("//dd/span[contains(text(),'物业费')]/parent::dd/span[@class='ddinfo']/text()"))
        if wuyeMoney:
            wuyeMoney = wuyeMoney.split("/")[0]

	#开发商、物业公司
        kaifashang = safe_extract(response.xpath("//dd/span[contains(text(),'开发商')]/parent::dd/text()"))
        wuyeCompany = safe_extract(response.xpath("//d/span[contains(text(),'物业公司')]/parent::dd/text()"))





    def parse(self, response):
        pass
