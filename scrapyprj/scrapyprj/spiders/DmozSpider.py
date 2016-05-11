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
        with open(filename, 'wb') as f:
            f.write(response.body)

    #  def start_requests(self):
        #  #  super(DmozSpider, self).start_requests()
        #  for url in self.start_urls:
            #  yield scrapy.Request(url)
