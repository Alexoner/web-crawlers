# -*- coding: utf-8 -*-
import scrapy
import os
import sys
import time
from scrapyprj.items import RentArticle, CommentReply
from scrapyprj.utils import safe_extract, extract_article, extract_url, trim, getProvince_City, getExistList, isRent
import json
import hashlib
import re
import time

class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["douban.com"]
    # 获取当前月、日、小时
    monthStr = time.localtime(time.time()).tm_mon
    dayStr = time.localtime(time.time()).tm_mday
    hourStr = time.localtime(time.time()).tm_hour

    header = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch, br",
        "Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4",
        "Connection": "keep-alive",
        "Host": "www.europerail.cn",
        "Referer": "http://www.europerail.cn/",
        "cache-control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
    }
    # 获取小组入后信息

    def start_requests(self):
        mapList = []
        group1 = {
            'url': 'https://www.douban.com/group/145219/',
            'name': '杭州 出租 租房 中介免入',
            'city': '杭州'}
        # group2 ={'url':'https://www.douban.com/group/HZhome/','name':'杭州租房','city':'杭州'}
        # group3 ={'url':'https://www.douban.com/group/467221/','name':'杭州租房（出租、求租、合租）','city':'杭州'}
        mapList.append(group1)
        # mapList.append(group2)
        # mapList.append(group3)
        for url in mapList:
            print ('send url ->', url)
            yield scrapy.Request(url['url'], headers=self.header, callback=self.parse_nextAndSub, meta=url)

    # 获得detail的数据和下一页，翻页的标准是如果最后更新日期小于小于今天，那么终止
    def parse_nextAndSub(self, response):
        # 首先获得时间列表，获得该列表的下级数据做分发
        timeList = safe_extract(response.xpath(
            "//td[@nowrap = 'nowrap'][@class='time']"))
        print ('parse timeList->', timeList)
        for i in range(1, len(timeList) + 1):
            timeStr = timeList[i - 1]
            try:
                # 获得最后更新日期数据，抽取出月、日、小时
                monStr = timeStr.split(" ")[0].strip().split('-')[0].strip()
                if monStr.startswith('0'):
                    monStr = monStr.replace('0', '').strip()
                    dStr = timeStr.split(" ")[0].strip().split('-')[1].strip()
                if dStr.startswith('0'):
                    dStr = dStr.replace('0', '').strip()

                hStr = timeStr.split(" ")[1].strip().split(':')[0].strip()
                if hStr.startswith('0'):
                    hStr = hStr.replace('0', '').strip()

                intMonth = int(monStr)
                intDay = int(dStr)
                intHour = int(hStr)
                # 只爬取当天和两个小时以内的数据
                if self.monthStr == intMonth and self.dayStr == intDay:
                    if abs(intHour - self.hourStr) <= 2:
                        # 如果最后一条的日期OK，那么翻页，否则不翻页
                        if i == len(timeList):
                            try:
                                if "start" in response.url:
                                    offset = re.search(
                                        r'start=([\d]*)', response.url).group(1)
                                    intOffset = int(offset)
                                    intOffset += 25
                                    newUrl = response.url.split(
                                        '=')[0] + '=' + str(intOffset)
                                else:
                                    newUrl = response.ur + "discussion?start=50"
                                    yield scrapy.Request(newUrl, headers=self.header, callback=self.parse_nextAndSub, meta=response.meta)
                            except Exception as e:
                                self.logger.error('%s, %s' % (response.url, e))

                        # 帖子链接、标题
                        url = safe_extract(response.xpath(
                            "//table[@class='olt']//tr[" + str(i + 1) + "]//td[@class='title']/a/@href"))
                        title = safe_extract(response.xpath(
                            "//table[@class='olt']//tr[" + str(i + 1) + "]//td[@class='title']/a/text()"))

                        # 作者
                        author = safe_extract(response.xpath(
                            "//table[@class='olt']//tr[" + str(i + 1) + "]//td[2]/a/text()"))
                        authorUrl = safe_extract(response.xpath(
                            "//table[@class='olt']//tr[" + str(i + 1) + "]//td[2]/a/@href"))

                        # 回帖人数
                        replyNum = safe_extract(response.xpath(
                            "//table[@class='olt']//tr[" + str(i + 1) + "]//td[3]/text()"))

                        param = response.meta.copy()
                        param['title'] = title
                        param['user_name'] = author
                        param['user_id'] = re.search(
                            r'people/([\s\S]*)/', authorUrl).group(1)
                        param['reply_count'] = replyNum
                        param['latest_time'] = timeStr
                        yield scrapy.Request(url, headers=self.header, callback=self.parse_detail, meta=param)
                else:
                    continue
            except Exception as e:
                self.logger.error('%s, %s, %s' % (response.url, e, i))

    def parse_detail(self, response):
        # 处理帖子主体内容
        pic_urls = safe_extract(response.xpath(
            "//div[contains(@class,'topic-figure')]/img/@src"))
        article = extract_article(raw_html=response.body)
        content = article['cleaned_text']
        id = hashlib.md5(response.url).hexdigest()
        self.logger.info('id: %s' % (id))
        topic = RentArticle()
        topic['id'] = id
        topic['url'] = response.url
        topic['source_url'] = response.meta['source_url']
        topic['source_name'] = response.meta['source_name']

        topicId = re.search(r'topic/([\s\S]*)/', response.url).group(1)
        topic['topic_id'] = topicId
        topic['title'] = response.meta['title']
        topic['topic_type'] = isRent(response.meta['title'])
        topic['user_id'] = response.meta['user_id']
        topic['user_name'] = response.meta['user_name']
        topic['latest_time'] = response.meta['latest_time']
        topic['reply_count'] = response.meta['reply_count']
        topic['pic_urls'] = pic_urls
        topic['content'] = content
        topic['db_name'] = 'douban_topic'
        yield topic

        # 提取评论信息

        replyUserList = safe_extract(response.xpath(
            "//ul[@class='topic-reply']/li//h4/a/text()"))

        for i in range(1, len(replyUserList) + 1):
            userName = replyUserList[i - 1]
            # 跳过用户自身的回复
            if userName == response.meta['user_name']:
                continue
            commentEntity = CommentReply()
            # 提取回复时间
            repTime = safe_extract(
                response.xpath(
                    "//ul[@class='topic-reply']/li[" +
                    str(i) +
                    "]//h4/span/text()"))
            commentEntity['reply_time'] = repTime
            commentEntity['id'] = hashlib.md5(topicId + repTime).hexdigest()
            commentEntity['outer_id'] = id
            commentEntity['user_url'] = safe_extract(response.xpath(
                "//ul[@class='topic-reply']/li[" + str(i) + "]//h4/a/@href"))
            commentEntity['user_name'] = userName
            replyContent = safe_extract(
                response.xpath(
                    "//ul[@class='topic-reply']/li[" +
                    str(i) +
                    "]//div[contains(@class,'reply-doc')]/p/text()"))
            commentEntity['content'] = replyContent
            commentEntity['db_name'] = 'douban_comment'
            yield commentEntity
