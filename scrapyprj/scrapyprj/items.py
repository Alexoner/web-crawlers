# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyprjItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    adults = scrapy.Field()
    children = scrapy.Field()
    seniors = scrapy.Field()
    youth = scrapy.Field()
    departure_date = scrapy.Field()
    start_city_name = scrapy.Field()
    dest_city_name = scrapy.Field()
    site = scrapy.Field()
    train_no = scrapy.Field()
    from_station = scrapy.Field()
    from_city_code = scrapy.Field()
    from_time = scrapy.Field()
    to_station = scrapy.Field()
    to_city_code = scrapy.Field()
    to_time = scrapy.Field()
    time_length = scrapy.Field()
    price = scrapy.Field()
    seat_grade = scrapy.Field()
    seat_type = scrapy.Field()
    segs = scrapy.Field()

class HouseNewsItem(scrapy.Item):
    newsId = scrapy.Field() #自动生成的ID
    soourceCategory = scrapy.Field() #原来的类目
    preCate = scrapy.Field()  #预测的类目
    sourceNav = scrapy.Field()  #原来的导航类目
    sourceId = scrapy.Field()  #原来的ID
    title = scrapy.Field()  #标题
    releaseTime = scrapy.Field()  # 发行时间
    source = scrapy.Field()  # 来源
    sourceUrl = scrapy.Field()  #来源链接
    url = scrapy.Field()  # URL
    summary = scrapy.Field()  # 摘要
    content = scrapy.Field()  #内容（去掉标签）
    keywords = scrapy.Field()  #关键词
    crawlTime = scrapy.Field()  #爬取时间
    readCount = scrapy.Field()  #阅读量
    clickCount = scrapy.Field()  #点击量
    shareCount = scrapy.Field()  #分享量
    thumbCount = scrapy.Field()  #点赞量
    author = scrapy.Field()  #作者
    editor = scrapy.Field()  #编辑
    htmlDocument = scrapy.Field()  # 新闻的html文本
    extendInfo = scrapy.Field()  #扩展字段
