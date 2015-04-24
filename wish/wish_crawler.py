#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import requests
import random
import re
import json
import urllib
from requests_futures.sessions import FuturesSession
from requests_futures.sessions import Callback
from enum import Enum

HEADERS = {"login":{
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "X-XSRFToken": "cookies['_xsrf']", # to be filled
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36"
        },
    "api_search":{
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36"
    }
}

PARAMETERS = {
    "login":{
                "email": "",
                "password": "",
                "_buckets": "",
                "_experiments": ""
            },
    "search":{
        'query':'',
        'start':'',
        'transform':'true'
    }
}


class Item:
    def __init__(self):
        self.contest_page_picture = ""  # 商品图片URL
        self.no = 0  # 商品排序
        self.localized_price_localized_value = 0  # 产品实际价格（折扣后）
        self.localized_shipping_localized_value = 0  # 运费
        self.product_rating = 0.0  # 商品评分
        self.rating_count = 0  # 参与评分用户数
        self.name = ""  # 商品名称
        self.ships_from = ""  # 发货国家
        self.shipping_time_string = ""  # 预计送达时间
        self.gender = ""  # 商品用户

        self.product_id = ""  # 商品ID
        self.min_shipping_time = 0  # 商品最快预计送达时间
        self.max_shipping_time = 0  # 商品最慢预计送达时间
        self.localized_retail_price_localized_value = 0  # 商品折扣前价格
        self.localized_retail_price_currency_code = ""  # 商品折扣前价格货币代码
        self.localized_price_currency_code = ""  # 商品折扣后价格货币代码
        self.localized_shipping_currency_code = ""  # 商品估计运费货币代码
        self.tags = ""  # 商品标签

    def get_list(self):
        return [
            self.contest_page_picture.encode("utf-8"),
            self.no,
            self.product_id.encode("utf-8"),

            self.localized_price_localized_value,
            self.localized_price_currency_code.encode("utf-8"),

            self.localized_retail_price_localized_value,
            self.localized_retail_price_currency_code.encode("utf-8"),

            self.localized_shipping_localized_value,
            self.localized_shipping_currency_code.encode("utf-8"),

            self.product_rating,
            self.rating_count,

            self.name.encode("utf-8"),
            self.ships_from.encode("utf-8"),

            self.min_shipping_time,
            self.max_shipping_time,
            self.shipping_time_string.encode("utf-8"),

            self.gender.encode("utf-8"),

            self.tags
        ]

class Task:
    def __init__(self,url="https://www.wish.com/api/search",
                 category_id=None,category_name="",start_offset=0,next_offset=0,
                 headers=None,parameters=None):
        self.api_search_url = url
        self.request_url = None

        self.category_id = category_id
        self.category_name = category_name
        self.start_offset = start_offset
        self.next_offset = next_offset

        self.state ="started"
        pass


class WishCallback(Callback):
    def __init__(self,data=None,wish=None):
        self.data = data
        self.wish = wish
        Callback.__init__(self)

    def execute(self):
        print "Data passed to me is: ",self.data,self.wish
        #print self.response.content
        self.wish.pipeline(self.data,self.response)
        pass

class Crawler:
    def __init__(self,
                 username="",
                 email="liushuaikobe1993@163.com",
                 password="19930418lskobe",
                 save_filename="products.json",
                 category_filename="categories_2.txt"):
        self.username = username
        self.email = email
        self.password = password
        self.categories = []
        self.api_search_url = ['https://www.wish.com/api/search']
        self.save_filename=save_filename
        self.category_filename=category_filename
        self.save_file=None
        self.category_file=None
        self.category_map=None
        self.rand = random.Random()
        self.proxy_addresses = [
        "http://50.22.186.84:3128",
        "http://50.22.186.84:3129",
        "http://50.22.186.84:3130",
        "http://50.22.186.84:3131",
        "http://50.22.186.84:3132",
        "http://50.22.186.84:3133",
        "http://50.22.186.84:3134",
        "http://50.22.186.84:3135",
        "http://50.22.186.84:3136",
        "http://50.22.186.84:3137",
        "http://50.22.186.84:3138",
        "http://50.22.186.84:3139",
        "http://50.22.186.84:3140",
        "http://50.22.186.84:3141",
        "http://50.22.186.84:3142",
        "http://50.22.186.84:3143",
        "http://50.22.186.84:3144",
        "http://50.22.186.84:3145",
        "http://50.22.186.84:3146",
        "http://50.22.186.84:3147",
        "http://50.22.186.84:3148",
        "http://50.22.186.84:3149",
        "http://50.22.186.84:3150",
        "http://50.22.186.84:3151",
        "http://50.22.186.84:3152",
        "http://50.22.186.84:3153"
        ]
        self.proxy_number = len(self.proxy_addresses)
        self.url_queue = []
        self.task_map = {}

        self.session = FuturesSession()

    def recover_from_file(self):
        """
            recover from the file to resume the tasks
        """
        pass

    def read_categories_file(self,category_filename="categories_2.txt"):
        """
            get categories to crawl
        """
        self.category_filename=category_filename
        with open(self.category_filename) as self.category_file:
            file_data = self.category_file.read()
            category_pairs = file_data.split("\n")
            category_pairs = category_pairs[1:len(category_pairs)-1]
            self.category_map = dict()
            pattern = re.compile("(\d+)\s(.+)")
            for pair in category_pairs:
                key,value = pattern.findall(pair)[0]
                self.category_map[key.strip().lower()]=value.strip().lower()

        return self.category_map

    def add_task(self,task):
        self.task_map[task.category_name] = task

    def add_tasks(self):
        #split_pattern = re.compile("\s*&\s*")
        split_pattern = re.compile("\s|&")
        for key,value in self.category_map.iteritems():
            names = split_pattern.split(value)
            for name in names:
                if not name.isspace():
                    task = Task(category_id=key,category_name=name)
                    self.add_task(task)
                else:
                    print name+" is space"

    def delete_task(self,task_name,task_id):
        try:
            self.task_map.pop(task_name)
        except Exception,e:
            print e
            pass

    def get(self,url,headers=None,param=None,proxies=None,cookie=None,callback=None):
        for key in headers:
            self.session.headers[key] = headers[key]
        url_true = url+"?"+urllib.urlencode(param)
        print "GET: "+url+"?"+urllib.urlencode(param)
        print 'Proxy: '+proxies['http']
        #future = self.session.get(url,data=param,proxies=proxies,cookie=cookie,background_callback=callback)
        future = self.session.get(url_true,proxies=proxies,background_callback=callback)
        return future

    def post(self,url,headers=None,param=None,proxies=None,cookie=None,callback=None):
        future = self.session.post(url,headers=headers,data=param,proxies=proxies,cookie=cookie,background_callback=callback)
        return future


    def fetch_category(self,category_name):
        """
            fetch a category's products
        """
        task = self.task_map[category_name]
        param = []
        param.append(('query',category_name))
        param.append(('start',str(task.start_offset)))
        param.append(('transform','true'))

        headers = HEADERS['api_search']
        cb = WishCallback(data=category_name,wish=self)

        proxies = self.get_proxy()
        self.get(url=task.api_search_url,headers=headers,param=param,proxies=proxies,cookie=None,callback=cb)


    def write2file(self,category_name,data):
        print 'pipeline: '+category_name
        with open("output/"+category_name+".txt","a+") as output:
            output.write(data)
            #self.category_file.write(data)

    def pipeline(self,category_name,response):
        json_decoder = json.JSONDecoder()
        result = json_decoder.decode(response.content)
        items = result['data']['results']
        self.write2file(category_name,json.dumps(items))
        next_offset = result['data']['next_offset']
        num_found = result['data']['num_found']
        num_received = len(items)
        self.task_map[category_name].start_offset = next_offset
        self.task_map[category_name].next_offset = next_offset
        self.task_map[category_name].num_found = num_found

        if num_received == 0:
            del self.category_map[category_name]

        with open("output/state.txt","w") as state_file:
            state_file.write(self.category_map)

        #for item in items:
            #pass

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

    def parse_products(self,products_in_json):
        pass

    def get_proxy(self):
        return {"http":self.proxy_addresses[self.rand.randint(0,self.proxy_number-1)]}

    def crawl(self):
        self.read_categories_file()
        #for key,value ()
        pass

def test():
    wish_crawler = Crawler()
    print "number of categories: ",len(wish_crawler.read_categories_file())
    wish_crawler.add_tasks()
    #print wish_crawler.task_map
    #url = "https://www.wish.com/api/search?query=book&start=21&transform=true"
    #wish_crawler.pipeline("book",requests.get(url).content)
    #wish_crawler.fetch_category('bags')
    #print requests.get(url).content
    while len(wish_crawler.category_map) != 0:
        for category_name in wish_crawler.task_map:
            wish_crawler.fetch_category(category_name)
        pass

    print "Exiting!"

if __name__ == "__main__":
   test()


