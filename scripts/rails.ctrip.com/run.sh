#!/bin/sh

mkdir -p output
scrapy crawl ctrip -o 'output/items.json'
