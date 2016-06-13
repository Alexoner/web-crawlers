#!/bin/sh

rsync -av . \
    --include="scrapyprj/middlewares**" \
    --include="scrapyprj/spiders**" \
    --include="scrapyprj/*.py" \
    --include="scrapyprj/proxies.txt" \
    --exclude="scrapyprj/log**" \
    --exclude="scrapyprj/output**" \
    --exclude="work**" \
    --exclude="sync.sh" \
    root@47.89.48.226:/root/crawler/
