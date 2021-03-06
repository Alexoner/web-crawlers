#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import requests
import random
import re
import json
import pickle
import urllib
import time
import os
import sys
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

    def get_header(self):
        return [
            'product_id',
            'contest_page_picture',
            'no',
            'localized_price_localized_value',
            'localized_price_currency_code',

            'localized_shipping_localized_value',
            'localized_shipping_currency_code',

            'product_rating',
            'rating_count',

            'name',
            'ships_from',

            'min_shipping_time',
            'max_shipping_time',
            'shipping_time_string',

            'gender',

            'tags'

        ]

    def get_list(self):
        return [
            self.product_id.encode("utf-8"),
            self.contest_page_picture.encode("utf-8"),
            self.no,

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

    def get_from_json(self,item_json=""):
        #p = Item()
        self.contest_page_picture = item["contest_page_picture", u"N/A"]
        self.no = params["offset"] + j
        self.product_id = item["id"]

        var_product = item["commerce_product_info"]["variations"][0]
        self.localized_price_localized_value = var_product.get("localized_price", {}).get("localized_value", -1)
        self.localized_price_currency_code = var_product.get("localized_price", {}).get("currency_code", u"N/A")
        self.localized_retail_price_localized_value = var_product.get("localized_retail_price", {}).get("localized_value", -1)
        self.localized_retail_price_currency_code = var_product.get("localized_retail_price", {}).get("currency_code", u"N/A")
        self.localized_shipping_localized_value = var_product.get("localized_shipping", {}).get("localized_value", -1)
        self.localized_shipping_currency_code = var_product.get("localized_shipping", {}).get("currency_code", u"N/A")
        self.product_rating = item.get("product_rating", {}).get("rating", -1)
        self.rating_count = item.get("product_rating", {}).get("rating_count", -1)
        self.name = item.get("name", u"N/A")
        self.ships_from = var_product.get("ships_from", u"N/A")
        self.min_shipping_time = var_product.get("min_shipping_time", -1)
        self.max_shipping_time = var_product.get("max_shipping_time", -1)
        self.shipping_time_string = var_product.get("shipping_time_string", u"N/A")
        self.gender = item.get("gender", u"N/A")
        self.tags = build_tags_str(item.get("tags", []))
        products_writer.writerow(self.get_list())


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

        self.last_modified = time.time()
        self.state ="started"
        pass


class WishCallback(Callback):
    def __init__(self,data=None,wish=None):
        self.data = data
        self.wish = wish
        Callback.__init__(self)

    def execute(self):
        print "Data passed to me is: ",self.data
        #print self.response.content
        try:
            self.wish.pipeline(self.data,self.response)
        except Exception,e:
            print e
            pass

class Crawler:
    def __init__(self,
                 username="",
                 email="liushuaikobe1993@163.com",
                 password="19930418lskobe",
                 category_filename="categories_2.txt",
                 save_filename="products.json",
                 timeout_seconds=300,
                 output_dir='output',
                 error_dir='error'):
        self.username = username
        self.email = email
        self.password = password
        self.categories = []
        self.api_search_url = ['https://www.wish.com/api/search']
        self.save_filename=save_filename
        self.category_filename=category_filename
        self.save_file=None
        self.category_file=None
        self.category_map={}
        self.task_list = []
        self.rand = random.Random()
        self.timeout_seconds = timeout_seconds
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

        self.output_dir = output_dir
        self.error_dir = error_dir

    def recover_from_file(self,path):
        """
            recover from the file to resume the tasks
        """
        try:
            rec_file = open(path,'rb')
            task_map = pickle.load(rec_file)
            self.task_map = task_map
        except IOError,e:
            print e
        #with open(path,'rb') as rec_file:
            #task_map = pickle.load(rec_file)
        #pass

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
                try:
                    key,value = pattern.findall(pair)[0]
                    self.category_map[value.strip().lower()]=value.strip().lower()
                except Exception,e:
                    print e
        fetched_categories = [  ]
        for key,value in self.category_map.items():
            if not self.is_fetched(key):
                self.task_list.append((key,value))
            else:
                fetched_categories.append(value)
                #print "\033[0;35m {} is fetched!".format(key)

        print "\033[0;35m {} categories are fetched in total!\033[0m".format(len(fetched_categories))
        #self.task_list = self.category_map.items()
        return self.task_list

    def read_invalid_tags(self,error_tags_filep="error/error.txt.0511"):
        """
        get invalid tags
        """
        with open(error_tags_filep,'r') as f:
            for line in f:
                pass

    def add_new_tasks(self):
        """
        add a new task to running map/queue from list of category tuples
        and return the new category name
        """
        try:
            new_tasks = [self.task_list.pop(0)]
            self.add_tasks(new_tasks)
            #self.fetch_category(new_tasks[0][1])
            #print "\033[4;31m new category {0}".format(new_tasks[0][1])
            return new_tasks[0][1]
        except Exception,e:
            print e
            return None


    def add_task_map(self,task):
        """
        add a Task object to task_map
        """
        self.task_map[task.category_name] = task

    def add_tasks(self,tasks=None):
        """
        add tasks from category (id,name) collection
        """
        #split_pattern = re.compile("\s*&\s*")
        #split_pattern = re.compile("\s|&")
        if tasks is None:
            for key,value in self.category_map.iteritems():
                #names = split_pattern.split(value)
                #for name in names:
                    #if not name.isspace():
                        #task = Task(category_id=key,category_name=name)
                        #self.add_task_map(task)
                    #else:
                        #print name+" is space"

                if not value.isspace():
                    task = Task(category_id=key,category_name=value)
                    self.add_task_map(task)
                else:
                    print value+" is space"
        else:
            for key,value in tasks:
                if not value.isspace():
                    task = Task(category_id=key,category_name=value)
                    self.add_task_map(task)
                else:
                    print value+" is space"


    def delete_task(self,task_name,task_id):
        try:
            del self.task_map[task_name]
        except Exception,e:
            print e

    def get(self,url,headers=None,param=None,proxies=None,cookie=None,callback=None):
        """
         send an asynchronous GET request with callback object
        """
        for key in headers:
            self.session.headers[key] = headers[key]
        url_true = url+"?"+urllib.urlencode(param)
        print "GET: "+url+"?"+urllib.urlencode(param)
        print 'Proxy: '+proxies['https']
        #future = self.session.get(url,data=param,proxies=proxies,cookie=cookie,background_callback=callback)
        #future = self.session.get(url_true,proxies=proxies,max_retries=5,background_callback=callback)
        future = self.session.get(url_true,params=None, data=None, headers=None, cookies=None, files=None, auth=None,
                                  timeout=self.timeout_seconds, allow_redirects=True, proxies=proxies,background_callback=callback)
        return future

    def post(self,url,headers=None,param=None,proxies=None,cookie=None,callback=None):
        future = self.session.post(url,headers=headers,data=param,proxies=proxies,cookie=cookie,background_callback=callback)
        return future

    def get_nitems_of_category(self,category_name):
        """
            get total number of items of the very category
            Binary search
        """
        pass

    def is_fetched(self,category_name):
        return os.path.isfile(self.get_category_output_filename(category_name))

    def fetch_category(self,category_name):
        """
            fetch a category's products if its output file is not present,
            otherwise,the category has been fetched,then remove it from task map.
        """
        task = self.task_map[category_name]
        param = []
        param.append(('query',category_name))
        param.append(('start',str(task.start_offset)))
        param.append(('transform','true'))

        headers = HEADERS['api_search']
        cb = WishCallback(data=category_name,wish=self)

        proxies = self.get_proxy()
        return self.get(url=task.api_search_url,headers=headers,param=param,proxies=proxies,cookie=None,callback=cb)

    def fetch_category_sync(self,category_name):
        task = self.task_map[category_name]
        param = []
        param.append(('query',category_name))
        param.append(('start',str(task.start_offset)))
        param.append(('transform','true'))
        cb = WishCallback(data=category_name,wish=self)

        headers = HEADERS['api_search']
        proxies = self.get_proxy()
        while self.task_map.has_key(category_name):
            pass

        print 'finished a category!'
        return self.get(url=task.api_search_url,headers=headers,param=param,proxies=proxies,cookie=None,callback=cb)

    def get_category_output_filename(self,category_name):
        return self.output_dir+"/"+category_name+".txt"

    def write2file(self,category_name,data):
        with open(self.output_dir+"/"+category_name+".txt","a+") as output:
            output.write(data)
            output.write("\n")
            #self.category_file.write(data)

    def is_dead_task(self,task):
        """
        check if a Task object is invalid any more
        """
        time_now = time.time()
        return (time_now - task.last_modified >= self.timeout_seconds)

    def check_dead_tasks(self):
        """
        check dead tasks,remove them,log them,replace them with new tasks
        """
        added_categories = [  ]
        for key in self.task_map.keys():
            if self.is_dead_task(self.task_map[key]):
                with open(self.error_dir+'/timeout.txt','a+') as f:
                    f.write(key+"\n")
                del self.task_map[key]
                category = self.add_new_tasks()
                print "\033[0;33m Oops,this task is dead: {}!\033[0m\nNew task:{} ".format(key,category)
                added_categories.append(category)
                #self.fetch_category(category)

        return added_categories

    def when_zero_received_ext(self,category_name):
        # delete it from task map
        print "\033[4;32mFinished category: ",category_name,"\033[0m"
        try:
            del self.task_map[category_name]
        except:
            pass
        print "\033[4;31m{0} category tasks remaining! \033[0m".format(len(self.task_map))
        if len(self.task_list) > 0:
            try:
                new_tasks = [self.task_list.pop(0)]
                self.add_tasks(new_tasks)
                self.fetch_category(new_tasks[0][1])
                print "\033[4;31m new category {0}".format(new_tasks[0][1])
            except:
                pass
        print "\033[4;31m{0} category tasks remaining! \033[0m".format(len(self.task_map))
        if os.path.isfile(self.output_dir+"/"+category_name+".txt"):
            # finished crawling
            pass
        else:
            # file not created,then tag not fetched at all!
            try:
                error_file = open(self.error_dir+'/error.txt','a+')
                error_file.seek(0,2)
                line_number = error_file.tell()
                error_file.write(str(line_number)+'\t'+category_name+'\n')
            except Exception,e:
                print e
            finally:
                if error_file is not None:
                    error_file.close()

    def when_zero_received(self,category_name):
        # delete it from task map
        print "\033[4;32mFinished category: ",category_name,"\033[0m"
        del self.task_map[category_name]
        print "{0} category tasks remaining! ".format(len(self.task_map))
        if os.path.isfile(self.output_dir+"/"+category_name+".txt"):
            pass
        else:
            # file not created,then tag not fetched at all!
            try:
                error_file = open(self.error_dir+'/error.txt','a+')
                error_file.seek(0,2)
                line_number = error_file.tell()
                error_file.write(str(line_number)+'\t'+category_name+'\n')
            except Exception,e:
                print e
            finally:
                if error_file is not None:
                    error_file.close()

    def pipeline(self,category_name,response):
        json_decoder = json.JSONDecoder()
        result = json_decoder.decode(response.content)
        items = result['data']['results']
        next_offset = result['data']['next_offset']
        num_found = result['data']['num_found']
        num_received = len(items)
        self.task_map[category_name].start_offset = next_offset
        self.task_map[category_name].next_offset = next_offset
        self.task_map[category_name].num_found = num_found
        # update the time stamp of when it is active last time
        self.task_map[category_name].last_modified = time.time()

        if num_received == 0:
            self.when_zero_received_ext(category_name)
        else:
            print 'pipeline: category='+category_name +' number received = ',num_received
            self.write2file(category_name,json.dumps(items))
            with open("output/state.txt","w+") as state_file:
                # with statement deals with Exceptions,may block your code !!!
                pickle.dump(self.task_map,state_file)
                #state_file.write(self.category_map)
                #state_file.flush()

            print 'continuing fetching category = ',category_name
            self.fetch_category(category_name)

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
        proxy = self.proxy_addresses[self.rand.randint(0,self.proxy_number-1)]
        #return {"http":proxy,
                #"https":proxy}
        return {'https':proxy}

    def crawl(self):
        self.read_categories_file()
        #for key,value ()
        pass

def test():
    wish_crawler = Crawler()
    wish_crawler.read_categories_file()
    wish_crawler.add_tasks()
    print wish_crawler.category_map
    #url = "https://www.wish.com/api/search?query=book&start=21&transform=true"
    #wish_crawler.pipeline("luggage & bags",requests.get(url).content)
    wish_crawler.fetch_category('luggage & bags')
    #print requests.get(url).content

def run(wish_crawler):
    """
    Parallelly crawl https:www.wish.com/
    Parallelism:
        1. Simultaneously category fetching
        2. Simultaneously request different partition of a category.
            Set the start offset to control how to partition.We need first
            to get the total number of items of a category
    """
    total_categories = wish_crawler.read_categories_file('tags/tags_2.json.bak')
    #print total_categories
    print "\033[4;32mnumber of categories: ",len(total_categories),"\033[0m"
    sys.stdin.read(1)
    # max concurrent connection number
    max_con = 100
    # add a batch of categories to task map
    i = 0
    tasks = wish_crawler.task_list[i*max_con:(i+1)*max_con]
    wish_crawler.task_list = wish_crawler.task_list[(i+1)*max_con:]
    wish_crawler.add_tasks(tasks)
    # simultaneously fetch the categories
    for category_name in wish_crawler.task_map:
        wish_crawler.fetch_category(category_name)

    while len(wish_crawler.task_map) != 0:
        time.sleep(10)
        print '\033[0;31m************************************************\033[0m'
        print "{0} category tasks remaining! ".format(len(wish_crawler.task_map))
        try:
            added_categories = wish_crawler.check_dead_tasks()
            for added_category in added_categories:
                print "\033[0;35m fetching new category  {}! \033[0m\n".format(added_category)
                wish_crawler.fetch_category(category_name)
        except Exception,e:
            print e

    print "\033[1;33mEntering next pass now!\033[0m"
    print "\033[0;31mExiting!\033[0m"


if __name__ == "__main__":
    wish_crawler = Crawler(output_dir='output/4',error_dir='error')
    run(wish_crawler)
