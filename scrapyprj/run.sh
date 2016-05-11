#!/bin/sh


# run locally
nohup scrapy crawl europerail -o ./scrapyprj/output/items.json

# to deploy to a remote daemon run
# scrapy-deploy
