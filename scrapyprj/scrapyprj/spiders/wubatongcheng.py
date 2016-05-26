# -*- coding: utf-8 -*-
import scrapy
import os
import sys
import time
from scrapyprj.items import AreaStaticEntity
from scrapyprj.utils import safe_extract, extract_article, extract_url, trim, getProvince_City
import json
import hashlib
import re
reload(sys)
sys.setdefaultencoding('utf-8')

class WubatongchengSpider(scrapy.Spider):
    name = "wubatongcheng"
    allowed_domains = ["58.com"]
    existList = ['bj','zh','sh','sz','cs','cq','gz','hrb','nj','sy','tj','wh']
    prefixUrl = 'sy'
    def start_requests(self):
        listMap = getProvince_City('/Users/xueliang.xl/web-crawlers/scrapyprj/scrapyprj/province_city_name.txt')
        for provinceJson in listMap:
            provinceJson = json.dumps(provinceJson)
            jsonObj = json.loads(provinceJson)
            province =  jsonObj['province']
            cityList =  jsonObj['cityList']
            for cityJson in cityList:
                cityJson = json.dumps(cityJson)
                city =  json.loads(cityJson)
                cityName = city['city']
                cityCode = city['code']
                param = {}
                param['province'] = province
                param['cityCode'] = cityCode
                param['cityName'] = cityName
                if cityCode in self.existList:
                    print 'city ',cityName ,'already done'
                else:
                    url = 'http://'+cityCode+'.58.com/xiaoqu/pn_1'
                    yield scrapy.Request(url,callback = self.parse_nextAndSub,meta = param)

    def parse_nextAndSub(self, response):
        urlList = response.xpath("//ul/li[@class='tli1']/a/@href").extract()
        #满20页，可以进行下一页
        if (urlList and  len(urlList) > 2):
            nextPage = response.url.split('_')[1]
            if '/' in nextPage:
                nextPage = nextPage.replace('/', '').strip()
            num = int(nextPage)
            num += 1
            nextUrl = 'http://'+response.meta['cityCode']+'.58.com/xiaoqu/pn_'+str(num)
            yield scrapy.Request(nextUrl, callback = self.parse_nextAndSub, meta = response.meta)
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
            metaData['province'] = response.meta['province']
            metaData['cityCode'] = response.meta['cityCode']
            metaData['cityName'] = response.meta['cityName']
            yield scrapy.Request(url, callback = self.parse_detail,meta = metaData)

   #解析detail
    def parse_detail(self,response):
        if "404" in response.url:
            return
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
        province = response.meta['province']
        city = response.meta['cityName']
        longitude = ''
        latitude = ''
        locationStr = re.search(r'xiaoqu:({.*?})', response.body).group(1)
        result['province'] = province
        result['city'] = city
        if locationStr:
            result['name'] = re.search(r'name:\'(.*?)\'',locationStr).group(1)
            result['longitude'] = re.search(r'lat:\'(.*?)\'',locationStr).group(1)
            result['latitude'] = re.search(r'lon:\'(.*?)\'',locationStr).group(1)
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
        #小区邮编的unicode编码
        postcode = safe_extract(response.xpath(u"//dd/span[contains(text(),'小区邮编')]/parent::dd/text()"))
        result['address'] = trim(address) #小区地址
        result['post_code'] = postcode #邮政编码
        #小区标签
        tagList = safe_extract(response.xpath("//div[@class='assessList']/span//text()"))
        if tagList:
            result['tags'] = tagList.replace('\t',',')

	#建筑年代和类型，unicode编码
	year_type = safe_extract(response.xpath(u"//dd/span[contains(text(),'建筑年代')]/parent::dd/text()"))
        year = ''
        # btype = ''
        if year_type:
            ylist = year_type.split(",")
            for i in (range(0,len(ylist))):
                if i == 0:
                    year = trim(trim(ylist[0]).split(" ")[0])
                # if i == 1:
                    # btype = ylist[1]
        #建筑年代和类型
        result['build_year'] = trim(year)
        # result['build_type'] = trim(btype)

        #物业费
        wuyeMoney = safe_extract(response.xpath(u"//dd/span[contains(text(),'物业费')]/parent::dd/span[@class='ddinfo']/text()"))
        if wuyeMoney:
            wuyeMoney = wuyeMoney.split("/")[0]
            result['prop_price'] = trim(wuyeMoney.replace('元',''))

	#开发商、物业公司
        kaifashang = safe_extract(response.xpath(u"//dd/span[contains(text(),'开发商')]/parent::dd/text()"))
        wuyeCompany = safe_extract(response.xpath(u"//dd/span[contains(text(),'物业公司')]/parent::dd/text()"))
        if kaifashang:
            result['developer'] = trim(kaifashang)
        if wuyeCompany:
            result['prop_company'] = trim(wuyeCompany)

        #幼儿园、小学、大学
        kindergarden = safe_extract(response.xpath(u"//div[@class='peitaoDiv']/ul/li/span[contains(text(),'幼儿园')]/text()"))
        # school = safe_extract(response.xpath(u"//div[@class='peitaoDiv']/ul/li/span[contains(text(),'小学')]/text()"))
        # college = safe_extract(response.xpath("//div[@class='peitaoDiv']/ul/li/span[contains(text(),'\u5927\u5b66')]/text()"))
        if kindergarden:
            result['kindergarden'] = trim(kindergarden)
        # if school:
            # result['middle_school'] = trim(school)
        # if college:
        #     result['college'] = college

        # #公交
        bus = safe_extract(response.xpath(u"//div[@id='peitao_2']/ul/li/span[contains(text(),'公')]/parent::li/span[@class='liinfo']/text()"))
        if bus:
            result['bus'] = bus
        #地铁
        subway = safe_extract(response.xpath(u"//div[@id='peitao_2']/ul/li/span[contains(text(),'地')]/parent::li/span[@class='liinfo']/text()"))
        if subway:
            result['subway'] = subway

        #配套信息的document
        peitaoDocument = safe_extract(response.xpath("//div[contains(@class,'peitaoInfo')]"))
        result['facility_dom'] = peitaoDocument

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

        description = safe_extract(response.xpath("//div[@id='peitao_4']/p/text()"))
        if description:
            result['description'] = description

        yield result

    def parse(self, response):
        pass
