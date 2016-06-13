import time
import scrapy
from scrapy.exceptions import NotConfigured

from scrapyprj.items import ScrapyprjItem

class MetaDataMiddleware(object):
    '''
        Meta data middleware.
        Fill the meta data fields of items, such as:
            last modified time
            crawl time
            name
            host
            url
            (html_document)
    '''

    @classmethod
    def from_crawler(cls, crawler):
        # if crawler.settings.getbool('META_DISABLED'):
            # raise NotConfigured
        return cls()

    def process_spider_output(self, response, result, spider):
        def _set_meta(r):
            if not isinstance(r, ScrapyprjItem):
                return r
            if not r['last_modified']:
                pass
            if not r['crawl_time']:
                r['crawl_time'] = time.time()
            if not r['url']:
                r['url'] = response.url
            if not r['host']:
                pass
            return r
        return (_set_meta(r) for r in result or ())
