#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import random
import base64
import logging

logger = logging.getLogger(__name__)

class ProxyDownloaderMiddleware(object):

    def __init__(self, settings):
        self.proxy_list = settings.get('PROXY_LIST')
        fin = open(self.proxy_list)

        self.proxies = {}
        for line in fin.readlines():
            #parts = re.match(r'(\w+://)(\w+:\w+@)?(.+)', line)
            parts = re.match(r'((\w+://)(\S+(:\w+)?)/)(.*)', line)

            self.proxies[parts.group(1)] = ''

            # Cut trailing @
            #  if parts.group(2):
                #  user_pass = parts.group(2)[:-1]
            #  else:
                #  user_pass = ''

            #  self.proxies[parts.group(1) + parts.group(3)] = user_pass

        fin.close()

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(settings)

    def process_request(self, request, spider):
        # Don't overwrite with a random one (server-side state for IP)
        if 'proxy' in request.meta:
            return

        proxy_address = random.choice(self.proxies.keys())
        proxy_user_pass = self.proxies[proxy_address]

        request.meta['proxy'] = proxy_address
        if proxy_user_pass:
            basic_auth = 'Basic ' + base64.encodestring(proxy_user_pass)
            request.headers['Proxy-Authorization'] = basic_auth

    def process_exception(self, request, exception, spider):
        proxy = request.meta['proxy']
        #  logger.debug('Removing failed proxy <%s>, %d proxies left' % (
            #  proxy, len(self.proxies)))
        try:
            if proxy in self.proxies:
                # don't delete
                #  del self.proxies[proxy]
                pass
        except ValueError:
            pass
