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
    news_id = scrapy.Field() #自动生成的ID
    soource_category = scrapy.Field() #原来的类目
    pre_cate = scrapy.Field()  #预测的类目
    source_nav = scrapy.Field()  #原来的导航类目
    source_id = scrapy.Field()  #原来的ID
    title = scrapy.Field()  #标题
    release_time = scrapy.Field()  # 发行时间
    source_name = scrapy.Field()  # 来源
    source_url = scrapy.Field()  #来源链接
    url = scrapy.Field()  # URL
    summary = scrapy.Field()  # 摘要
    content = scrapy.Field()  #内容（去掉标签）
    keywords = scrapy.Field()  #关键词
    crawl_time = scrapy.Field()  #爬取时间
    read_count = scrapy.Field()  #阅读量
    click_count = scrapy.Field()  #点击量
    share_count = scrapy.Field()  #分享量
    thumb_count = scrapy.Field()  #点赞量
    comment_count = scrapy.Field() #评论数
    author = scrapy.Field()  #作者
    editor = scrapy.Field()  #编辑
    html_document = scrapy.Field()  # 新闻的html文本
    extend_info = scrapy.Field()  #扩展字段
