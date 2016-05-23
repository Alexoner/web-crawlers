# -*- coding: utf-8 -*-
import scrapy
import os
import sys
import time
from scrapyprj.items import AreaStaticEntity
from scrapyprj.utils import safe_extract, extract_article, extract_url, trim
import json
import hashlib

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
        yield scrapy.Request(start, callback = self.parse_nextAndSub)

    def parse_nextAndSub(self, response):
        urlList = response.xpath("//ul/li[@class='tli1']/a/@href").extract()
        #满20页，可以进行下一页
        if (urlList and  len(urlList) == 20):
            nextPage = response.url.split('_')[1]
            if '/' in nextPage:
                nextPage = nextPage.replace('/', '').strip()
            num = int(nextPage)
            num += 1
            nextUrl = 'http://sz.58.com/xiaoqu/pn_'+str(num)
            yield scrapy.Request(nextUrl, callback = self.parse_nextAndSub)
        #详细内容
        blockList = response.xpath("//table[@class='tbimg']/tbody/tr")
        for  i in range(1, len(blockList)+1):
            url = safe_extract(response.xpath("//table[@class='tbimg']/tbody/tr["+str(i)+"]//ul/li[@class='tli1']/a/@href"))
            second_num = safe_extract(response.xpath("//table[@class='tbimg']/tbody/tr["+str(i)+"]//ul/li[@class='tli3'][1]/span[1]/text()"))
            rend_num = safe_extract(response.xpath("//table[@class='tbimg']/tbody/tr["+str(i)+"]//ul/li[@class='tli3'][1]/span[1]/text()"))
            money = safe_extract(response.xpath("//table[@class='tbimg']/tbody/tr["+str(i)+"]//p/b[@class='money']/text()"))
            metaData = {}
            metaData['second_num'] = second_num
            metaData['rend_num'] = rend_num
            metaData['money'] = trim(money)
            yield scrapy.Request(url, callback = self.parse_detail,meta = metaData)

   #解析detail
    def parse_detail(self,response):
        result = AreaStaticEntity()
        param = response.meta
        url = response.url
        second_num = param['second_num']
        rend_num = param['rend_num']
        money = param['money']
        name = safe_extract(response.xpath("//h1[@class='xiaoquh1']/text()"))
        alias_name = safe_extract(response.xpath("//h1[@class='xiaoquh1']/span/text()"))
        if alias_name:
            alias_name = alias_name.replace('(',"")
            alias_name = alias_name.replace(')',"")
            alias_name = alias_name.strip()

        result['source'] = '58同城' #来源
        result['url'] = url #链接
        result['second_count'] = second_num #二手房数量
        result['rend_count'] = rend_num #出租房数量
        result['price'] = money

        #根据url生成md5
        id = hashlib.md5(url).hexdigest()
        result['id'] = id
        #名称、别名
        if name:
            result['name'] = name
        if alias_name:
            result['area_alias'] = alias_name

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
                    latitude = tmpList[2].split('=')[1].split(",")[1]
        result['province'] = province
        result['city'] = city
        result['longitude'] = longitude
        result['latitude'] = latitude

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
	#区、片区
        #result['area'] = area
        #if subarea:
        #    result['sub_area'] = subarea

        # 地址和邮编
        address = safe_extract(response.xpath("//span[@class='ddinfo']/a[contains(@href,'xiaoqu')]/parent::span/text()"))
        #小区邮编的unicode编码
        # postcode = safe_extract(response.xpath("//dd/span[contains(text(),'\u5c0f\u533a\u90ae\u7f16')]/parent::dd/text()"))
        result['address'] = trim(address) #小区地址
        # result['post_code'] = postcode #邮政编码
        #小区标签
        tagList = safe_extract(response.xpath("//div[@class='assessList']/span//text()"))
        if tagList:
            result['tags'] = tagList.replace('\t',',')

	#建筑年代和类型，unicode编码
        # import ipdb
        # ipdb.set_trace()
        year_type = safe_extract(response.xpath(u"//dd/span[contains(text(), '建筑年代')]/parent::dd/text()"))
 #        year = ''
 #        type = ''
 #        if year_type:
 #            for i in (range(0,len(year_type))):
 #                if i == 0:
 #                    year = year_type[0]
 #                if i == 1:
 #                    type = year_type[1]

 #        #建筑年代和类型
 #        result['build_year'] = year
 #        result['build_type'] = type

        #物业费
        # wuyeMoney = safe_extract(response.xpath("//dd/span[contains(text(),'\u7269\u4e1a\u8d39')]/parent::dd/span[@class='ddinfo']/text()"))
        # if wuyeMoney:
        #     wuyeMoney = wuyeMoney.split("/")[0]
        #     result['prop_price'] = wuyeMoney

	#开发商、物业公司
        # kaifashang = safe_extract(response.xpath("//dd/span[contains(text(),'\u5f00\u53d1\u5546')]/parent::dd/text()"))
        # wuyeCompany = safe_extract(response.xpath("//d/span[contains(text(),'\u7269\u4e1a\u516c\u53f8')]/parent::dd/text()"))
        # if kaifashang:
        #     result['developer'] = kaifashang
        # if wuyeCompany:
        #     result['prop_company'] = wuyeCompany

        #幼儿园、小学、大学
        # kindergarden = safe_extract(response.xpath("//div[@class='peitaoDiv']/ul/li/span[contains(text(),'\u5e7c\u513f\u56ed')]/text()"))
        # school = safe_extract(response.xpath("//div[@class='peitaoDiv']/ul/li/span[contains(text(),'\u5c0f\u5b66')]/text()"))
        # college = safe_extract(response.xpath("//div[@class='peitaoDiv']/ul/li/span[contains(text(),'\u5927\u5b66')]/text()"))
        # if kindergarden:
        #     result['kindergarden'] = kindergarden
        # if school:
        #     result['middle_school'] = school
        # if college:
        #     result['college'] = college

        # #公交
        # bus = safe_extract(response.xpath("//div[@id='peitao_2']/ul/li/span[contains(text(),'\u516c')]/parent::li/span[@class='liinfo']/text()"))
        # if bus:
        #     result['bus'] = bus
        # #地铁
        # subway = safe_extract(response.xpath("//div[@id='peitao_2']/ul/li/span[contains(text(),'\u94c1')]/parent::li/span[@class='liinfo']/text()"))
        # if subway:
        #     result['subway'] = subway

        #配套信息的document
        #peitaoDocument = response.xpath("//div[contains(@class,'peitaoInfo')]")
        #result['facility_dom'] = peitaoDocument.html

        #导航信息
        navList = safe_extract(response.xpath("//div[@class='nav']/a/text()"))
        if navList:
            result['source_nav'] = navList.replace('\t',',')
            tlist = result['source_nav'].split(',')
            for i in range(3,len(tlist)):
                if i == 3:
                    result['area'] = tlist[3]
                if i == 4:
                    result['sub_area'] = tlist[4]

        # 图片
        picList = safe_extract(response.xpath("//ul[@id='phcUl']/li/img/@src"))
        if picList:
            result['picture_urls'] = picList

        # description = safe_extract(response.xpath("//div[contains(@class,'Able-scroll')]/p/text()"))
        # if description:
        #     result['description'] = description

        yield result

    def parse(self, response):
        pass
