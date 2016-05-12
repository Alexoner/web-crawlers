# -*- coding: utf-8 -*-
import scrapy
import urlparse


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
            '//div[@id="bd1lfimg"]/div/dl/dd/a')
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
                    'cookiejar': i,
                })
        pass

    def parse_detail(self, response):
        with open('/tmp/a.html', 'w') as f:
            f.write(response.body)
        yield {'html': response.body}
        pass
