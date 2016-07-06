# -*- coding: utf-8 -*-
import scrapy
import os
import sys
from scrapyprj.items import ProxyInfo
from scrapyprj.utils import safe_extract, extract_url, trim
import json
import hashlib
import re
import time
from  datetime import datetime

class ProxySpider(scrapy.Spider):
    name = "proxy"
    allowed_domains = ["66ip.cn","ip.zdaye.com"]
    dayStr = time.localtime(time.time()).tm_mday
    hourStr = time.localtime(time.time()).tm_hour

    def start_requests(self):
        urlMap = [
        {'url': 'http://www.66ip.cn/1.html', 'tag': 'ip66'},
        # {'url': 'http://ip.zdaye.com/?ip=&port=&adr=&checktime=1%D0%A1%CA%B1%C4%DA&sleep=&cunhuo=&nport=&nadr=&dengji=&https=&yys=&gb=&post=&px=','tag':'zdaye'}
        {'url':'http://www.free-proxy-list.net/','tag':'free-proxy-list'},
        {'url':'http://proxy.ipcn.org/proxya.html','tag':'proxya'}
        ]
        for url in urlMap:
            if url['tag']=='ip66':
                yield scrapy.Request(url['url'], callback = self.parse_ip66)
            if url['tag'] == 'free-proxy-list':
                yield scrapy.Request(url['url'], callback = self.parse_freeproxy)
            if url['tag'] == 'proxya':
                yield scrapy.Request(url['url'], callback = self.parse_proxya)

            # if [url['tag'] == 'zdaye']:
            #     yield scrapy.Request(url['url'], callback = self.parse_zdaye)
    #fuck zdaye use image to show port into ,what a fuck
    # def parse_zdaye(self, response):
    #     length = len(response.xpath("//table[@id='ipc']//tr").extract())
    #     for i in range(2,length+1):
    #         ip = safe_extract(response.xpath("//table[@id='ipc']//tr["+str(i)+"]/td[1]/text()"))
    #         port = safe_extract(response.xpath("//table[@id='ipc']//tr["+str(i)+"]/td[2]/text()"))
    #         location = safe_extract(response.xpath("//table[@id='ipc']//tr["+str(i)+"]/td[4]/text()"))
    #         level = safe_extract(response.xpath("//table[@id='ipc']//tr["+str(i)+"]/td[3]/text()"))

    #         proxy = ProxyInfo()
    #         proxy['name'] = ip+":"+port
    #         proxy['ip'] = ip
    #         proxy['port'] = port
    #         proxy['level'] = level.replace(u'代理','').strip()
    #         proxy['position'] = location

    #         proxy['head_type'] = '-'
    #         proxy['method_type'] = '-'
    #         proxy['last_time'] = time.time()
    #         proxy['speed'] = '1'
    #         yield proxy
    def parse_ip66(self, response):
        lastTime = safe_extract(response.xpath("//div[@align='center']//table//tr[last()]//td[last()]//text()"))
        lastTime = trim(lastTime)
        if len(lastTime) == 0:
            return
        day = re.search(u'([\d]+)日', lastTime).group(1)
        hour= re.search(u'([\d]+)时', lastTime).group(1)
        print ( day,hour )
        if day.startswith('0'):
            day = day.replace('0','').strip()
        if hour =='00':
            hour = '0'
        else:
            if hour.startswith('0'):
                hour = hour.replace('0','').strip()
        #最后一条满足条件那么翻页
        print ( 'crawl day and hour is ',self.dayStr,self.hourStr,'proxy site is',day,hour )
        if self.dayStr==day and abs(int(self.hour)-int(Strhour))<=1:
            pageNo =  re.search(r'([\d]+).html',response.url).group(1)
            nextPage = int(pageNo)+1
            newUrl = 'http://www.66ip.cn/'+str(nextPage)+".html"
            yield scrapy.Request(newUrl, callback=self.parse_ip66)
        #提取本页面的信息
        length = len(response.xpath("//div[@align='center']//tr").extract())
        for i in range(2,length+1):
            ip = safe_extract(response.xpath("//div[@align='center']//tr["+str(i)+"]/td[1]/text()"))
            port = safe_extract(response.xpath("//div[@align='center']//tr["+str(i)+"]/td[2]/text()"))
            location = safe_extract(response.xpath("//div[@align='center']//tr["+str(i)+"]/td[3]/text()"))
            level = safe_extract(response.xpath("//div[@align='center']//tr["+str(i)+"]/td[4]/text()"))
            validTime = safe_extract(response.xpath("//div[@align='center']//tr["+str(i)+"]/td[5]/text()"))
            timeList = re.findall(r'([\d]+)',validTime)
            timeStr = timeList[0]+"-"+timeList[1]+"-"+timeList[2]+" "+timeList[3]+":00:00"
            timeStame = time.mktime(datetime.strptime(timeStr,'%Y-%m-%d %H:%M:%S').timetuple())
            proxy = ProxyInfo()
            proxy['db_name'] = 'proxy'
            proxy['ip'] = ip
            proxy['port'] = port
            proxy['level'] = level.replace(u'代理','').strip()
            proxy['head_type'] = '-'
            proxy['method_type'] = '-'
            proxy['position'] = location
            proxy['last_time'] = timeStame
            proxy['speed'] = '1'
            proxy['name'] = ip+":"+port
            yield proxy

    def parse_freeproxy(self, response):
        timeList = safe_extract(response.xpath("//table[@id='proxylisttable']//tbody/tr/td[8]/text()"))

        for  i in range(1,len(timeList)+1):
            #只处理一个小时内的
            if 'hour' in timeList[i-1]:
                continue
            ip = safe_extract(response.xpath("//table[@id='proxylisttable']//tbody/tr["+str(i)+"]/td[1]/text()"))
            port = safe_extract(response.xpath("//table[@id='proxylisttable']//tbody/tr["+str(i)+"]/td[2]/text()"))
            country = safe_extract(response.xpath("//table[@id='proxylisttable']//tbody/tr["+str(i)+"]/td[3]/text()"))
            level = safe_extract(response.xpath("//table[@id='proxylisttable']//tbody/tr["+str(i)+"]/td[5]/text()"))
            https = safe_extract(response.xpath("//table[@id='proxylisttable']//tbody/tr["+str(i)+"]/td[7]/text()"))
            proxy = ProxyInfo()
            proxy['db_name'] = 'proxy'
            proxy['ip'] = ip
            proxy['port'] = port
            proxy['name'] = ip+":"+port
            proxy['level'] = level
            proxy['position'] = country
            if 'yes' == https:
                proxy['head_type'] = 'https'
            else:
                proxy['head_type'] = 'http'
            proxy['method_type'] = '-'
            proxy['last_time'] = time.time()
            proxy['speed'] = '1'
            if ip:
                yield proxy

    def parse_proxya(self, response):
        proxyList = re.findall(r'([\d]+\.[\d]+\.[\d]+\.[\d]+\:[\d]+)' , response.body)
        for  i in range(0,len(proxyList)):
            proxy = ProxyInfo()
            proxy['db_name'] = 'proxy'
            proxy['ip'] = proxyList[i].split(":")[0]
            proxy['port'] = proxyList[i].split(":")[1]
            proxy['name'] = proxyList[i]
            proxy['level'] = '-'
            proxy['position'] = 'CN'
            proxy['head_type'] = 'http'
            proxy['method_type'] = '-'
            proxy['last_time'] = time.time()
            proxy['speed'] = '1'
            if proxy['ip']:
                yield proxy

    def parse(self, response):
        pass
