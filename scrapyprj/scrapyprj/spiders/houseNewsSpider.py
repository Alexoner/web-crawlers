# -*- coding: utf-8 -*-
import os
import sys
import scrapy
import time
from scrapyprj.items import HouseNewsItem
from scrapyprj.utils import safe_extract,extract_article

reload(sys)
sys.setdefaultencoding('utf-8')

class HousenewsspiderSpider(scrapy.Spider):
    
    name = "houseNewsSpider"
    allowed_domains = ["weixinyidu.com"]

   	# start_urls = [
    #    'http://www.weixinyidu.com/a_958',
    #    'http://www.weixinyidu.com/a_970',
    #    'http://www.weixinyidu.com/a_2650',
    #    'http://www.weixinyidu.com/a_87979'
    # ]

    def start_requests(self):
    	seedUrlList = [
            #weixinyidu
    		{'url':'http://www.weixinyidu.com/a_958','name':'丁祖昱评楼市','source':'dzypls'},
    		# {'url':'http://www.weixinyidu.com/a_970','name':'真叫卢俊的地产观','source':'zhenjiaolujun'},
    		# {'url':'http://www.weixinyidu.com/a_2650','name':'地产八卦女','source':'dichanbaguanv'},
    		# {'url':'http://www.weixinyidu.com/a_87979','name':'上海楼典','source':'shanghailord'},

      #       #aiweibang
      #       {'url':'http://top.aiweibang.com/u/203962','name':'地产大哥','source':'dichandage'},
      #       {'url':'http://top.aiweibang.com/u/10380','name':'深圳地产通','source':'shenzhendichantong'},

      #       {'url':'http://toutiao.com/m6188273732/','name':'梵高先生','source':'Mrvangogh1989'},
            
      #       {'url':'http://www.taogonghao.com/wemedia/detail/1486.html','name':'房产头条','source':'jinrongtegong'}
            
      #       {'url':'http://www.wtoutiao.com/author/szlujz.html','name':'陆家嘴','source':'szlujz'}
            
      #       {'url':'http://www.vccoo.com/a/jg2w6','name':'地产大爆炸','source':'dichandabaozha'}

    	]
    	for seed in seedUrlList:
    		return scrapy.Request(seed['url'], callback=self.parse_seed,meta=seed)

       

    def parse_seed(self,response):
    	"""parse seed to generate sublist"""
    	#get news list
    	paramData = response.meta
        
        if 'weixinyidu' in response.url:
            #处理四个微信易读
    	   urlList = response.xpath("//div[@class='news_content']//li/a/@href").extract()
    	   for url in urlList:
    		   yield scrapy.Request('http://www.weixinyidu.com'+url,callback=self.parse_detail,meta = paramData)
        
        elif 'aiweibang' in response.url:
            #处理爱微帮
            urlList = response.xpath("//div[@id = 'hot_article_list']//a/@href").extract()
            for url in urlList:
               yield scrapy.Request(url,callback=self.parse_detail_aliweibang,meta = paramData)

        elif 'toutiao' in response.url:

            articleList = response.xpath("//div[@class='pin']")
            for article in articleList:
                url = article.xpath("//h3/a/@href")
                viewCount = article.xpath("/div[@class='pin-content']//tr/td[1]/text()")
                commentCount = article.xpath("div[@class='pin-content']//tr/td[2]/text()")
                paramData['viewCount'] = viewCount
                paramData['commentCount'] = commentCount
                yield scrapy.Request(url,callback=self.parse_detail_toutiao,meta = paramData)

        elif 'taogonghao' in response.url:
            urlList = response.xpath("//ul[@class='recent_article']//li/a/@href").extract()
            for url in urlList:
               yield scrapy.Request(url,callback=self.parse_detail_taogonghao,meta = paramData)

        elif 'wtoutiao' in response.url:
            urlList = response.xpath("//div[@class='news-header']//a/@href").extract()
            for url in urlList:
               yield scrapy.Request('http://www.wtoutiao.com/'+url,callback=self.parse_detail_wtoutiao,meta = paramData)
        
        elif 'vccoo' in response.url:
            urlList = response.xpath("//div[@class='classify-list']//h3/a/@href").extract()
            for url in urlList:
               yield scrapy.Request(url,callback=self.parse_detail_vccoo,meta = paramData)

    #generate newsItem from detail 
    def parse_detail(self,response):
    	#获取参数
    	paramData = response.meta

    	houseNews = HouseNewsItem()

    	houseNews['url'] = response.url
    	houseNews['source'] = paramData['source']
    	houseNews['author'] = paramData['name']
    	#标题
    	houseNews['title'] = response.xpath("//h1[@class='news_title']/text()").extract()[0]
    	#时间
    	houseNews['release_time'] = response.xpath("//span[@class='news_time']/text()").extract()[0]
    	#阅读量
    	houseNews['read_count'] =response.xpath("//span[@class ='news_read_no']/text()").extract()[1]
    	#点赞量
    	houseNews['thumb_count'] =response.xpath("//span[@class ='news_read_no']/text()").extract()[2]
    	#关键词，热词
    	houseNews['keywords'] = response.xpath("//a[@class='hot_txt']/text()").extract()
        #爬取时间
        houseNews.crawl_time = time.time()
        article = extract_article(raw_html=response.body)

        #文本内容
        houseNews.content = article['cleaned_text']        
        houseNews['keywords'] = houseNews['keywords']+ article['meta']['keywords']

        #dom文本
        houseNews.html_document = response.xpath("//div[@class = 'news_content']").extract()
    	yield houseNews


    def parse_detail_aliweibang(self,response):
        #获取参数
        paramData = response.meta

        houseNews = HouseNewsItem()

        houseNews['url'] = response.url
        houseNews['source'] = paramData['source']
        #标题
        houseNews['title'] = response.xpath("//h1[@class='title']/text()").extract()[0]
        print houseNews['title']
        #时间
        houseNews['release_time'] = response.xpath("//span[contains(@class,'activity')]/text()").extract()[0]
        houseNews['author'] = paramData['name'] + response.xpath("//span[contains(@class,'activity')]/text()").extract()[1]

        #阅读量
        #houseNews['read_count'] =response.xpath("//span[@class ='news_read_no']/text()").extract()[1]
        #点赞量
        #houseNews['thumb_count'] =response.xpath("//span[@class ='news_read_no']/text()").extract()[2]
        #关键词，热词
        #houseNews['keywords'] = response.xpath("//a[@class='hot_txt']/text()").extract()
        yield houseNews

    def parse_detail_toutiao(self,response):
        #获取参数
        paramData = response.meta

        houseNews = HouseNewsItem()

        houseNews['url'] = response.url
        houseNews['source'] = paramData['source']
        houseNews['author'] = paramData['name']
        houseNews['view_count'] = paramData['viewCount']
        houseNews['comment_count'] = paramData['commentCount']

        #标题
        houseNews['title'] = safe_extract(response.xpath("//h1/text()"))
        #时间
        houseNews['release_time'] = safe_extract(response.xpath("//span[@class='time']/text()"))
        #类目
        houseNews.source_category = safe_extract(response.xpath("//div[@class ='curpos']/a[2]/text()"))
        #内容
        houseNews.content = safe_extract(response.xpath("//div[@class='article-content']//text()"))
        #houseNews.html_document = 
        #houseNews['read_count'] =response.xpath("//span[@class ='news_read_no']/text()").extract()[1]
        #点赞量
        #houseNews['thumb_count'] =response.xpath("//span[@class ='news_read_no']/text()").extract()[2]
        #关键词，热词
        #houseNews['keywords'] = response.xpath("//a[@class='hot_txt']/text()").extract()
        yield houseNews

    def parse_detail_taogonghao(self,response):
        #获取参数
        paramData = response.meta

        houseNews = HouseNewsItem()

        houseNews['url'] = response.url
        houseNews['source'] = paramData['source']
        houseNews['author'] = paramData['name']
        #标题
        houseNews['title'] = response.xpath("//h1[@class='news_title']/text()").extract()[0]
        print houseNews['title']
        #时间
        houseNews['release_time'] = response.xpath("//span[@class='news_time']/text()").extract()[0]
        #阅读量
        houseNews['read_count'] =response.xpath("//span[@class ='news_read_no']/text()").extract()[1]
        #点赞量
        houseNews['thumb_count'] =response.xpath("//span[@class ='news_read_no']/text()").extract()[2]
        #关键词，热词
        houseNews['keywords'] = response.xpath("//a[@class='hot_txt']/text()").extract()
        yield houseNews
    def parse_detail_wtoutiao(self,response):
        #获取参数
        paramData = response.meta

        houseNews = HouseNewsItem()

        houseNews['url'] = response.url
        houseNews['source'] = paramData['source']
        houseNews['author'] = paramData['name']
        #标题
        houseNews['title'] = response.xpath("//h1[@class='news_title']/text()").extract()[0]
        print houseNews['title']
        #时间
        houseNews['release_time'] = response.xpath("//span[@class='news_time']/text()").extract()[0]
        #阅读量
        houseNews['read_count'] =response.xpath("//span[@class ='news_read_no']/text()").extract()[1]
        #点赞量
        houseNews['thumb_count'] =response.xpath("//span[@class ='news_read_no']/text()").extract()[2]
        #关键词，热词
        houseNews['keywords'] = response.xpath("//a[@class='hot_txt']/text()").extract()
        yield houseNews
    def parse_detail_vccoo(self,response):
        #获取参数
        paramData = response.meta

        houseNews = HouseNewsItem()

        houseNews['url'] = response.url
        houseNews['source'] = paramData['source']
        houseNews['author'] = paramData['name']
        #标题
        houseNews['title'] = response.xpath("//h1[@class='news_title']/text()").extract()[0]
        print houseNews['title']
        #时间
        houseNews['release_time'] = response.xpath("//span[@class='news_time']/text()").extract()[0]
        #阅读量
        houseNews['read_count'] =response.xpath("//span[@class ='news_read_no']/text()").extract()[1]
        #点赞量
        houseNews['thumb_count'] =response.xpath("//span[@class ='news_read_no']/text()").extract()[2]
        #关键词，热词
        houseNews['keywords'] = response.xpath("//a[@class='hot_txt']/text()").extract()
        yield houseNews