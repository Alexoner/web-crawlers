# -*- coding: utf-8 -*-
import time
import scrapy

from scrapyprj.utils import *
from scrapyprj.items import HouseNewsItem

class SzhomeSpider(scrapy.Spider):
    name = "szhome"
    allowed_domains = ["szhome.com", "news.szhome.com"]
    start_urls = (
        #  'http://www.szhome.com/',
        'http://news.szhome.com/list/1030',
    )

    def __init__(self, name=None, **kwargs):
        super(SzhomeSpider, self).__init__(name, **kwargs)

    def parse(self, response):
        next_page = response.xpath(
            '//*[@id="netpage"]/span[3]/following-sibling::a[1]/@href')
        articles = response.xpath('//*[@id="dtlNews_ctl00_hlnkSubject"]/@href')
        self.logger.info(response)
        if next_page:
            yield scrapy.Request(extract_url(response, next_page),
                                 callback=self.parse)
        for article in articles:
            yield scrapy.Request(
                extract_url(response, article),
                callback=self.parse_detail,
                meta={
                    'item': {
                    },
                }
            )
        pass

    def parse_detail(self, response):
        article = extract_article(raw_html=response.body)
        next_page = response.xpath(
            '//*[@id="divPager"]/ul/li/span/parent::*/following-sibling::*[1]/a/@href')
        #  import ipdb
        #  ipdb.set_trace()
        item = response.meta.get('item').get('item')
        if item:
            item['content'] = item.get('content') + article['cleaned_text']
        else:
            source_name = extract_after_colon_ch(safe_extract(
                response.xpath('//*[@id="news_main"]/div[1]/div[1]/div/div[1]/span[2]/text()')))

            keywords = extract_after_colon_ch(safe_extract(response.xpath(
                '//*[@id="news_main"]/div[1]/div[1]/div/div[1]/span[1]/text()')))
            author = extract_after_colon_ch(safe_extract(response.xpath(
                '//*[@id="news_main"]/div[1]/div[1]/div/div[1]/span[3]/text()'
            )))
            pub_time = extract_after_colon_ch(safe_extract(response.xpath(
                '//*[@id="news_main"]/div[1]/div[1]/div/div[2]/span[1]/text()')))

            #  item = HouseNewsItem()
            item = {}
            item['url'] = [response.url]
            item['author'] = author
            item['crawl_time'] = time.time()
            item['release_time'] = pub_time
            item['title'] = article['title']
            item['summary'] = safe_extract(
                response.xpath('//p[@id="fzy"]/text()'))
            item['content'] = article['cleaned_text']
            item['source_name'] = source_name
            item['source_url'] = None
            item['keywords'] = keywords

        if next_page:
            yield scrapy.Request(
                extract_url(response, next_page),
                callback=self.parse_detail,
                meta={
                    'item': {
                        'item': item,
                    },
                }
            )
            pass
        else:
            yield item
        pass
