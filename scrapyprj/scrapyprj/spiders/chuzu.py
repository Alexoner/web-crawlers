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
            #出租链接
            url =  safe_extract(response.xpath("//tr["+str(i)+"]/td/a[@class='t']/@href"))
            #标题
            title = safe_extract(response.xpath("//tr["+str(i)+"]/td/a[@class='t']/text()"))
            #价格
            price = safe_extract(response.xpath("//tr["+str(i)+"]/td/b[@class='pri']/text()"))
            #列表页显示的几室几厅
            rent_tips = safe_extract(response.xpath("//tr["+str(i)+"]/td/span[@class='showroom']/text()"))
    def parse_detail(self, response):

        #发布时间
        publish_time = safe_extract(response.xpath(u"//span[contains(text(),'更新时间')]/text()"))
        #支付方式，一半付三压一
        payMethod = safe_extract(response.xpath("//span[contains(@class,'pay-method')]/text()"))
        #坐标
        localList = re.search(r'locallist:\[({.*?)\]',response.body).group(1)

        #房屋
        roomList = safe_extract(response.xpath("//div[contains(@class,'house-type')]//text()"))
        if roomList:
            roomList = trim(roomList)
        #地址
        address = safe_extract(response.xpath(u"//li/span[contains(text(),'地址')]/parent::li/div/text()"))
        if address:
            address = trim(address)
        #配置
        peizhi = safe_extract(response.xpath(u"//li/span[contains(text(),'配置')]/parent::li/div/span/text()"))
        if peizhi:
            peizhi = trim(peizhi)
        #图片
        picList = safe_extract(response.xpath("//ul[@id = 'leftImg']//li/img/@src"))

        if localList:
            localList = '['+ localList + ']'
            localList = re.sub(r'(,?)(\w+?)\s*?:', r'\1"\2":',localList)
            localList = json.dumploas(localList)








