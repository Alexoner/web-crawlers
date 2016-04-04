#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Fake a proxy server that forwards requests for others

    Fake fields:
        X-Forwarded-For
        Via
"""

import re
import random
import base64
import logging

logger = logging.getLogger(__name__)

XFF = 'X-Forwarded-For'
VIA = 'Via'

class FakeProxyMiddleware(object):

    def __init__(self, settings):

        logger.debug('loaded %s middleware', __name__)

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(settings)

    def process_request(self, request, spider):
        # Don't overwrite existing valid proxy with a random one (server-side
        # state for IP)
        if request.headers.get(XFF):
            logger.debug('Faked ip: %s' % (request.headers.get(XFF)))
            return
        else:
            random_public_ip = '%s.%s.%s.%s' % (
                random.randint(1, 255),
                random.randint(1, 255),
                random.randint(1, 255),
                random.randint(1, 255))
            request.headers[XFF] = random_public_ip
            request.headers[VIA] = '1.1 %s squid/3.5' % (random_public_ip)
            logger.debug('Faked ip: %s' % (random_public_ip))

    def process_exception(self, request, exception, spider):
        logger.debug('Exception %s with %s address' % (
            exception, request.headers.get(XFF)))
