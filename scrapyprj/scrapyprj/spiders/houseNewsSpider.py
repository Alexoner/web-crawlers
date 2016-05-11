# -*- coding: utf-8 -*-
import scrapy
from scrapyprj.items import HouseNewsItem


class HousenewsspiderSpider(scrapy.Spider):
    name = "houseNewsSpider"
    start_urls = (
        'http://www.weixinyidu.com/a_958',
        'http://www.weixinyidu.com/a_970',
        'http://www.weixinyidu.com/a_2650',
        'http://www.weixinyidu.com/a_87979',
    )
    def parse(self, response):
        pass
