# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from pprint import pformat
import scrapy


class ScrapyprjItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    host = scrapy.Field() # host
    url = scrapy.Field()  # URL
    description = scrapy.Field()
    crawl_time = scrapy.Field()  # 爬取时间
    html_document = scrapy.Field()  # 新闻的html文本

    def __repr__(self):
        """"""
        return pformat({'name': str(self['name'])})
    pass

class TrafficTicketItem(ScrapyprjItem):
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

class HouseNewsItem(ScrapyprjItem):
    news_id = scrapy.Field()  # 自动生成的ID
    soource_category = scrapy.Field()  # 原来的类目
    pre_cate = scrapy.Field()  # 预测的类目
    source_nav = scrapy.Field()  # 原来的导航类目
    source_id = scrapy.Field()  # 原来的ID
    title = scrapy.Field()  # 标题
    release_time = scrapy.Field()  # 发行时间
    source_name = scrapy.Field()  # 来源
    source_url = scrapy.Field()  # 来源链接
    summary = scrapy.Field()  # 摘要
    content = scrapy.Field()  # 内容（去掉标签）
    keywords = scrapy.Field()  # 关键词
    read_count = scrapy.Field()  # 阅读量
    click_count = scrapy.Field()  # 点击量
    share_count = scrapy.Field()  # 分享量
    thumb_count = scrapy.Field()  # 点赞量
    comment_count = scrapy.Field()  # 评论数
    author = scrapy.Field()  # 作者
    editor = scrapy.Field()  # 编辑
    extend_info = scrapy.Field()  # 扩展字段
    images = scrapy.Field() #图片

#小区的基本信息，保存小区的基本信息
class AreaStaticEntity(ScrapyprjItem):
    source_url = scrapy.Field()#来源链接
    source_name = scrapy.Field()#来源名称
    url = scrapy.Field()#链接
    area_id = scrapy.Field()#小区ID
    area_name = scrapy.Field()#小区中文名
    area_name_en = scrapy.Field()#小区英文名
    area_alias = scrapy.Field()#小区别名
    location = scrapy.Field()#地点，详细地址
    coordinate = scrapy.Field()#经纬度坐标
    price  = scrapy.Field()#价格
    picture_urls =  scrapy.Field()#图片
    business_circle = scrapy.Field()#商圈
    developer = scrapy.Field()#开发商
    prop_company = scrapy.Field()#物业公司
    prop_price = scrapy.Field()#物业费
    post_code = scrapy.Field()#邮编
    subway = scrapy.Field()#地铁
    bus = scrapy.Field() #公交
    build_structure = scrapy.Field()#建筑结构
    carports = scrapy.Field()#车位数量
    green_percent = scrapy.Field()#绿化率
    total_area = scrapy.Field()#总建筑面积
    description = scrapy.Field()#描述
    kindergarden = scrapy.Field()#幼儿园
    middle_school = scrapy.Field()#中学
    college = scrapy.Field()#大学
    supermarket = scrapy.Field()#超市、综合体
    hospital = scrapy.Field()#医院
    postoffice = scrapy.Field()#邮局
    bank = scrapy.Field()#银行
    other_facility = scrapy.Field()#其他设施
    tags = scrapy.Field() #小区标签、关键词

    #小区的动态信息，如房价
class AreaDynamicEntity(ScrapyprjItem):
    area_id = scrapy.Field() #小区的ID
    price = scrapy.Field() #当前价格
    prop_price = scrapy.Field() #物业费
    crawl_date = scrapy.Field() #爬取日期，到天级别



    def __repr__(self):
        """only print out attr1 after exiting the Pipeline"""
        return pformat({'title': str(self['title'])})
