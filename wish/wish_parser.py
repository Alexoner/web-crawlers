#!/usr/bin/env python2
#-*- coding: UTF8 -*-

import json
import os
import sys
from utils import merge_dicts

reload(sys)
sys.setdefaultencoding('utf-8')


def parse_items(line):
    json_decoder = json.JSONDecoder()
    result = json_decoder.decode(line)
    #items = result['data']['results']
    return result

def parse_product(self,item):
        p = Item()
        p.contest_page_picture = item["contest_page_picture", u"N/A"]
        p.no = params["offset"] + j
        p.product_id = item["id"]

        var_product = item["commerce_product_info"]["variations"][0]
        p.localized_price_localized_value = var_product.get("localized_price", {}).get("localized_value", -1)
        p.localized_price_currency_code = var_product.get("localized_price", {}).get("currency_code", u"N/A")
        p.localized_retail_price_localized_value = var_product.get("localized_retail_price", {}).get("localized_value", -1)
        p.localized_retail_price_currency_code = var_product.get("localized_retail_price", {}).get("currency_code", u"N/A")
        p.localized_shipping_localized_value = var_product.get("localized_shipping", {}).get("localized_value", -1)
        p.localized_shipping_currency_code = var_product.get("localized_shipping", {}).get("currency_code", u"N/A")
        p.product_rating = item.get("product_rating", {}).get("rating", -1)
        p.rating_count = item.get("product_rating", {}).get("rating_count", -1)
        p.name = item.get("name", u"N/A")
        p.ships_from = var_product.get("ships_from", u"N/A")
        p.min_shipping_time = var_product.get("min_shipping_time", -1)
        p.max_shipping_time = var_product.get("max_shipping_time", -1)
        p.shipping_time_string = var_product.get("shipping_time_string", u"N/A")
        p.gender = item.get("gender", u"N/A")
        p.tags = build_tags_str(item.get("tags", []))
        products_writer.writerow(p.get_list())

def parse_tags_from_file(path="output/1/computer & office.txt"):
    tags_all = dict()
    decoder = json.JSONDecoder()
    f = None
    try:
        f = open(path,'rb')
        for line in f:
            items = decoder.decode(line)
            for item in items:
                # has tags,then add tags to the
                if item.has_key('tags'):
                    tags = item['tags']
                    for tag in tags:
                        tags_all[tag['id']] = tag
    except Exception,e:
        print 'error occurred when parsing file ',path,' :'
        print e
        return None
    finally:
        if f is not None:
            f.close()
        print 'Finished parsing!'
        return tags_all

def get_files_under_directory(directory='output/1'):
    if os.path.isdir(directory):
        file_paths = [f for f in os.listdir(directory) if os.path.isfile(directory+"/"+f)]
        return file_paths
    return None

def parse_tags(path='output/1'):
    tags_all = []
    file_paths = get_files_under_directory(directory='output/1')
    i = 0
    for file_path in file_paths:
        print 'parsing file: ',file_path
        tags_new = parse_tags_from_file(path=path+"/"+file_path)
        #tags_all.update(parse_tags_from_file(path=path))
        with open('tags/tags_2.json','a+') as out_file:
            for tag in tags_new.values():
                i = i + 1
                out_file.write(unicode(i))
                out_file.write('\t')
                out_file.write(tag['name'].decode('utf8'))
                out_file.write('\n')

        tags_all += tags_new.values()
        #with open('tags/'+file_path+'.json','a') as out_file:
            #out_file.write(json.dumps(tags_new.values()))
        print 'parsed {0} tags: {1}'.format(file_path,len(tags_all))

    with open('tags/tags_all.json','w+') as out_file:
        for tag in tags_all:
            out_file.write(json.dumps(tag))


    return tags_all

def filter_products(input_dir="output/4",output_filep="products/products.json"):
    raw_fileps = os.listdir(input_dir)
    # hold all the id of products
    id_set = set()
    output_file = open(output_filep,'a+')

    for raw_filep in raw_fileps:
        with open(input_dir+"/"+raw_filep) as raw_file:
            for line in raw_file:
                items = parse_items(line)
                for item in items:
                    if item['id'] in id_set:
                        print 'id {} is already in the set'.format(item['id'])
                        continue
                    else:
                        id_set.add(item['id'])
                        output_file.write(json.dumps(item)+'\n')
    print raw_fileps
    #pass



if __name__ == "__main__":
    #parse_tags(path='output/1')
    filter_products()



