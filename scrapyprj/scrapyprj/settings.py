# -*- coding: utf-8 -*-

# Scrapy settings for scrapyprj project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'scrapyprj'

SPIDER_MODULES = ['scrapyprj.spiders']
NEWSPIDER_MODULE = 'scrapyprj.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scrapyprj (+http://www.yourdomain.com)'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS=512

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY=0.45
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN=16
CONCURRENT_REQUESTS_PER_IP=128

# Disable cookies (enabled by default)
#COOKIES_ENABLED=False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED=False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'scrapyprj.middlewares.MyCustomSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    #  'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    #  'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
    'scrapyprj.middlewares.ProxyDownloaderMiddleware': 543,
    'scrapyprj.middlewares.fakeproxy.FakeProxyMiddleware': 544,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
  'scrapyprj.pipelines.JsonWithEncodingPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
#  AUTOTHROTTLE_ENABLED=True
# The initial download delay
#  AUTOTHROTTLE_START_DELAY=1.5
# The maximum download delay to be set in case of high latencies
#  AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
#  AUTOTHROTTLE_DEBUG=True

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED=True
#HTTPCACHE_EXPIRATION_SECS=0
#HTTPCACHE_DIR='httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES=[]
#HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'

RETRY_TIMES = 16
DUPEFILTER_DEBUG = True

import os
import time

#  DIRNAME = os.path.dirname(__file__)
DIRNAME = '{}/work/getter/{}'.format(os.path.expanduser('~'), time.strftime('%Y-%m-%d', time.localtime()))
try:
    os.mkdir(DIRNAME)
    os.mkdir('{}/log'.format(DIRNAME))
    os.mkdir('{}/output'.format(DIRNAME))
except Exception as e:
    pass
PROXY_LIST = '{}/proxies.getter.txt'.format(DIRNAME)
PROXY_LIST_ANONYMOUS = '{}/proxies.tor.txt'.format(DIRNAME)

#  LOG_FILE = '{}/log/{}-{}.log'.format(DIRNAME, BOT_NAME, time.strftime('%Y-%m-%d', time.localtime(time.time())))

OUTPUT_FILE = '{}/output/output_utf8'.format(DIRNAME)
