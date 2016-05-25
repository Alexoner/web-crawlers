# -*- coding: utf-8 -*-
from frontera.settings.default_settings import MIDDLEWARES

MAX_NEXT_REQUESTS = 512
SPIDER_FEED_PARTITIONS = 2
SPIDER_LOG_PARTITIONS = 1

#--------------------------------------------------------
# Url storage
#--------------------------------------------------------

BACKEND = 'frontera.contrib.backends.sqlalchemy.SQLAlchemyBackend'
# BACKEND = 'frontera.contrib.backends.sqlalchemy.Distributed'


SQLALCHEMYBACKEND_ENGINE = 'sqlite:///url_storage_dist.sqlite'
SQLALCHEMYBACKEND_ENGINE_ECHO = False
SQLALCHEMYBACKEND_DROP_ALL_TABLES = True
SQLALCHEMYBACKEND_CLEAR_CONTENT = True
from datetime import timedelta
SQLALCHEMYBACKEND_REVISIT_INTERVAL = timedelta(days=3)


MIDDLEWARES.extend([
    'frontera.contrib.middlewares.domain.DomainMiddleware',
    'frontera.contrib.middlewares.fingerprint.DomainFingerprintMiddleware'
])

# HBase backend
# BACKEND = 'distributed_frontera.contrib.backends.hbase.HBaseBackend'
# HBASE_DROP_ALL_TABLES = False
# HBASE_THRIFT_PORT = 9090
# HBASE_THRIFT_HOST = 'localhost'

# MIDDLEWARES.extend([
    # 'frontera.contrib.middlewares.domain.DomainMiddleware',
    # 'frontera.contrib.middlewares.fingerprint.DomainFingerprintMiddleware'
# ])

#--------------------------------------------------------
# Logging
#--------------------------------------------------------
LOGGING_EVENTS_ENABLED = False
LOGGING_MANAGER_ENABLED = True
LOGGING_BACKEND_ENABLED = True
LOGGING_DEBUGGING_ENABLED = True

TEST_MODE = True
