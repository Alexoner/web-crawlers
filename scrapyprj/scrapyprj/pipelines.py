# -*- coding: utf-8 -*-

import json
import codecs

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class JsonWithEncodingPipeline(object):

    def __init__(self, settings):
        self.output_file_name = settings.get('OUTPUT_FILE')
        #  if self.output_file_name:
            #  self.file = codecs.open(self.output_file_name, 'a+', encoding='utf-8')

        # name: output_file dictionary
        self.output_files = {}

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(settings)

    def process_item(self, item, spider):
        if not self.output_files.get(spider.name):
            self.output_files[spider.name] = codecs.open('%s.%s.json' % (self.output_file_name,spider.name ), mode='a+', encoding='utf-8')
        output_file = self.output_files[spider.name]
        if output_file:
            line = json.dumps(dict(item), ensure_ascii=False) + "\n"
            output_file.write(line)
            return item

    def spider_closed(self, spider):
        #  self.file.close()
        for output_file in self.output_files.values():
            output_file and output_file.close()
