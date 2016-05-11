# -*- coding: utf-8 -*-
import scrapy


class SznewsSpider(scrapy.Spider):
    handle_httpstatus_list = [400, 404, 407, 502]
    name = "sznews"
    allowed_domains = ["dc.sznews.com"]
    start_urls = (
        'http://dc.sznews.com/node_204507.htm',
    )

    def __init__(self, name=None, **kwargs):
        super(SznewsSpider, self).__init__(name, **kwargs)

    def parse(self, response):
        article_titles = response.xpath(
            '/html/body/div[8]/div[1]/div/h3/a/text()').extract()
        for i, article_title in enumerate(article_titles):
            yield scrapy.Request(article_title,
                                 callback=None,
                                 headers={},
                                 meta={
                                     'item': {
                                         'uid': 'detail',
                                     },
                                     'dont_merge_cookies': True,
                                     'cookiejar': i,
                                 })
        pass

    def parse_detail(self, response):
        pass
