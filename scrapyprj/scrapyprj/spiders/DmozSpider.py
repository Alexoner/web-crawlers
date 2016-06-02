# -*- coding: utf-8 -*-
import scrapy


class DmozSpider(scrapy.spiders.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = (
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    )

    def parse(self, response):
        filename = response.url.split("/")[-2] + '.html'
        yield {'url': response.url,
               'content': response.body[:100],
               }
