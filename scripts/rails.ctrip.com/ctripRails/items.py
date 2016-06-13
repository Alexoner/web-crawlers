# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CtriprailsItem(scrapy.Item):
    # define the fields for your item here like:
    BookingData = scrapy.Field()
    LastTimeLow = scrapy.Field()
    NoResult = scrapy.Field()
    ShowHtml = scrapy.Field()
    productsCount = scrapy.Field()
    showBackHtml = scrapy.Field()
    startCityCode = scrapy.Field()
