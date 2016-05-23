#!/bin/sh

# start ZeroMQ broker
python2 -m frontera.contrib.messagebus.zeromq.broker 1>zeromq.log 2>&1 &
# start DB worker
python2 -m frontera.worker.db --config scrapyprj.frontera.worker_settings 1>db.log 2>&1 &

# start strategy worker
python2 -m frontera.worker.strategy --config scrapyprj.frontera.strategy0 --strategy frontera.worker.strategies.bfs.CrawlingStrategy 1>strategy.log 2>&1 &

# start spiders
#scrapy crawl general -L INFO -s FRONTERA_SETTINGS=scrapyprj.frontera.spider0 -s SEEDS_SOURCE=seeds_es_smp.txt
scrapy crawl sznews -L INFO -s FRONTERA_SETTINGS=scrapyprj.frontera.spider0
#scrapy crawl sznews -L INFO -s FRONTERA_SETTINGS=scrapyprj.frontera.spider1
