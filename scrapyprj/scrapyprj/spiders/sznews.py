# -*- coding: utf-8 -*-
import random
import time
import urlparse
import scrapy

from scrapyprj.items import HouseNewsItem
from scrapyprj.utils import safe_extract, extract_article


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
            '//div[@class="fl w660-news-index"]/div[@class="list-con"]/h3/a')
        for i, article_title in enumerate(article_titles):
            self.logger.info('article: %s' %
                             (article_title.xpath('./text()')[0].extract()))
            yield scrapy.Request(
                urlparse.urljoin(response.url,
                                 article_title.xpath('./@href')[0].extract()),
                callback=self.parse_detail,
                headers={},
                meta={
                    'item': {
                        'uid': 'detail',
                    },
                    'dont_merge_cookies': True,
                    'cookiejar': 2 * i + 1,
                })

        next_page = response.xpath(
            '//div[@class="fl w660-news-index"]/div/center/span/following-sibling::a[1]/@href')
        yield scrapy.Request(
            urlparse.urljoin(response.url,
                             safe_extract(next_page)),
            callback=self.parse,
            headers={},
            meta={
                'item': {
                    'uid': 'list',
                },
                'dont_merge_cookies': True,
                'cookiejar': random.randint(1, 10000),
            })
        pass

    def parse_detail(self, response):
        # TODO: manybe consider goose or newspaper to deal with article
        # extraction
        #  with open('/tmp/a.html', 'w') as f:
            #  f.write(response.body)
        article = extract_article(raw_html=response.body)
        if response.xpath('//*[@id="source_baidu"]/a'):
            source = response.xpath('//*[@id="source_baidu"]/a')
            source_name = safe_extract(source.xpath('./text()'))
            source_url = safe_extract(source.xpath('./@href'))
        else:
            source = response.xpath('//*[@id="source_baidu"]')
            source_name = str(safe_extract(source.xpath('./text()')).split('：')[1]).strip()
            source_url = None
        yield HouseNewsItem({
            #  'html_document': [safe_extract(response.xpath('//*[@id="PrintTxt"]'))],
            'url': [response.url],
            'title': safe_extract(response.xpath('//*[@id="PrintTxt"]/h2/text()')),
            'crawl_time': time.time(),
            'release_time': safe_extract(response.xpath('//*[@id="pubtime_baidu"]/text()')),
            'summary': safe_extract(response.xpath('//p[@id="fzy"]/text()')),
            #  'content': safe_extract(response.xpath('(//*[@id="PrintTxt"]/div[2]/p/font|//*[@id="PrintTxt"]/div[2]/p)/text()')),
            'content': article['cleaned_text'],
            'source_name': source_name,
            'source_url': source_url,
            'keywords': article['meta']['keywords'],
        })

        # TODO: an article may be separated in two pages, we need to visit the
        # next page
        pass
