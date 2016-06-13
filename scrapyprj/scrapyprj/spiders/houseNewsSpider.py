# -*- coding: utf-8 -*-
import os
import sys
import scrapy
import time
from scrapyprj.items import HouseNewsItem
from scrapyprj.utils import safe_extract, extract_article, extract_url
import json


class HousenewsspiderSpider(scrapy.Spider):

    name = "houseNewsSpider"
    # allowed_domains = ["weixinyidu.com","aiweibang.com","toutiao.com","taogonghao.com","mp.weixin.qq.com","wtoutiao.com","vccoo.com",]

    def start_requests(self):
        baseUrlStr = 'http://toutiao.com/search_content/?offset={offset}&format=json&keyword={keyword}&autoload=true&count=20'
        seedUrlList = []
        keywordsList = [
            '房产',
            '购房',
            '二手房',
            '房贷',
            '房价',
            '公积金',
            '限购',
            '学区房',
            '装修']
        offsetList = [20, 40, 60, 80, 100]
        for keyword in keywordsList:
            for offset in offsetList:
                url = baseUrlStr.format(offset=offset, keyword=keyword)
                seedUrlList.append(url)
                yield scrapy.Request(url, callback=self.parse_seed)

            # weixinyidu
                # {'url':'http://www.weixinyidu.com/a_958','name':'丁祖昱评楼市','source':'dzypls'},
                # {'url':'http://www.weixinyidu.com/a_970','name':'真叫卢俊的地产观','source':'zhenjiaolujun'},
                # {'url':'http://www.weixinyidu.com/a_2650','name':'地产八卦女','source':'dichanbaguanv'},
                # {'url':'http://www.weixinyidu.com/a_87979','name':'上海楼典','source':'shanghailord'},

      # #       #aiweibang
      #       {'url':'http://top.aiweibang.com/u/203962','name':'地产大哥','source':'dichandage'},
      #       {'url':'http://top.aiweibang.com/u/10380','name':'深圳地产通','source':'shenzhendichantong'},

      #       {'url':'http://toutiao.com/m6188273732/','name':'梵高先生','source':'Mrvangogh1989'},

      #       {'url':'http://www.taogonghao.com/wemedia/detail/1486.html','name':'房产头条','source':'jinrongtegong'},

      #       {'url':'http://www.wtoutiao.com/author/szlujz.html','name':'陆家嘴','source':'szlujz'},

      #       {'url':'http://www.vccoo.com/a/jg2w6','name':'地产大爆炸','source':'dichandabaozha'},
        #]

        # for seed in seedUrlList:
                # yield scrapy.Request(seed['url'],
                # callback=self.parse_seed,meta = seed)

    def parse_seed(self, response):
        jsonResponse = json.loads(response.body_as_unicode())
        dataList = jsonResponse['data']
        for news in dataList:
            yield scrapy.Request(news['article_url'], callback=self.parse_article_toutiao, meta=news)

    def parse_article_toutiao(self, response):
        newsItem = HouseNewsItem()
        contentJson = response.meta
        url = response.url
        keywords = contentJson['keywords']
        title = contentJson['title']
        id = contentJson['id']
        # 处理图片
        if contentJson['has_image']:
            imageStr = contentJson['middle_image']
            imageUrlList = []
            if 'url_list' in imageStr:
                urlList = imageStr['url_list']
                for jsonUrl in urlList:
                    try:
                        str = json.loads(jsonUrl)['url']
                        if str not in imageUrlList:
                            imageUrlList.append(str)
                    except Exception as e:
                        self.logger.error('url: %s, imageStr: %s' % (url, imageStr))
            else:
                imageUrlList.append(imageStr)

            newsItem['images'] = imageUrlList

        publishTime = contentJson['datetime']
        source = contentJson['source']
        sourceUrl = 'http://toutiao.com' + contentJson['item_source_url']
        articleAbs = contentJson['abstract']
        likeCount = contentJson['favorite_count']
        commentCount = contentJson['comment_count']

        article = extract_article(raw_html=response.body)
        newsItem['url'] = url
        newsItem['news_id'] = id
        newsItem['keywords'] = keywords
        newsItem['title'] = title
        newsItem['release_time'] = publishTime
        newsItem['source_name'] = source
        newsItem['source_url'] = sourceUrl
        newsItem['summary'] = articleAbs
        newsItem['thumb_count'] = likeCount
        newsItem['comment_count'] = commentCount
        newsItem['content'] = article['cleaned_text']
        yield newsItem


# http://toutiao.com/search_content/?offset=0&format=json&keyword=%E5%85%AC%E7%A7%AF%E9%87%91&autoload=true&count=20
    # def parse_seed(self,response):
        # paramData = response.meta
        # if 'weixinyidu' in response.url:
        #     #处理四个微信易读
        # urlList = response.xpath("//div[@class='news_content']//li/a/@href").extract()
        # for url in urlList:
        # yield
        # scrapy.Request('http://www.weixinyidu.com'+url,callback=self.parse_detail,meta
        # = paramData)

        # elif 'aiweibang' in response.url:
        #     #处理爱微帮
        #     articleList = response.xpath("//div[@id ='hot_article_list']//div[@class='article']//a/@href").extract()
        #     for article in articleList:
        #         # url = article.xpath("//a/@href").extract()[0]
        #         # print url ,'asdfd'
        #         # viewCount = article.xpath("//span[@class='text-right']//text()").extract()[0]
        #         # thumbCount = article.xpath("//span[@class='text-right']//text()").extract()[1]
        #         # paramData['viewCount'] = viewCount
        #         # paramData['thumbCount'] = thumbCount
        # yield
        # scrapy.Request(article,callback=self.parse_detail_aliweibang,meta =
        # paramData)

        # elif 'toutiao' in response.url:
        #     articleList = response.xpath("//div[@class='pin']")
        #     for article in articleList:
        #         url = article.xpath("//h3/a/@href").extract()[0]
        #         viewCount = article.xpath("/div[@class='pin-content']//tr/td[1]/text()").extract()
        #         commentCount = article.xpath("div[@class='pin-content']//tr/td[2]/text()").extract()
        #         paramData['viewCount'] = viewCount
        #         paramData['commentCount'] = commentCount
        # yield scrapy.Request(url,callback=self.parse_detail_toutiao,meta =
        # paramData)

        # elif 'taogonghao' in response.url:
        #     urlList = response.xpath("//ul[@class='recent_article']//li/a/@href").extract()
        #     for url in urlList:
        # yield scrapy.Request(url,callback=self.parse_detail_taogonghao,meta =
        # paramData)

        # elif 'wtoutiao' in response.url:
        #     urlList = response.xpath("//div[@class='news-header']//a/@href").extract()
        #     for url in urlList:
        # yield scrapy.Request(url,callback=self.parse_detail_wtoutiao,meta =
        # paramData)

        # elif 'vccoo' in response.url:
        #     urlList = response.xpath("//div[@class='classify-list']//h3/a/@href").extract()
        #     for url in urlList:
        # yield scrapy.Request(url,callback=self.parse_detail_vccoo,meta =
        # paramData)

    # generate newsItem from detail
    def parse_detail(self, response):
        # 获取参数
        paramData = response.meta

        article = extract_article(raw_html=response.body)

        houseNews = HouseNewsItem()

        houseNews['url'] = response.url
        houseNews['source_name'] = paramData['source']
        houseNews['author'] = paramData['name']
        # 标题
        houseNews['title'] = response.xpath(
            "//h1[@class='news_title']/text()").extract()[0]
        # 时间
        houseNews['release_time'] = response.xpath(
            "//span[@class='news_time']/text()").extract()[0]
        # 阅读量
        houseNews['read_count'] = response.xpath(
            "//span[@class ='news_read_no']/text()").extract()[1]
        # 点赞量
        houseNews['thumb_count'] = response.xpath(
            "//span[@class ='news_read_no']/text()").extract()[2]
        # 关键词，热词
        houseNews['keywords'] = safe_extract(
            response.xpath("//a[@class='hot_txt']/text()"))
        # 爬取时间
        houseNews['crawl_time'] = time.time()
        houseNews['content'] = article['cleaned_text']
        # dom文本
        houseNews['html_document'] = safe_extract(
            response.xpath("//div[@class = 'news_content']"))
        yield houseNews

    def parse_detail_aliweibang(self, response):
        # 获取参数
        paramData = response.meta
        houseNews = HouseNewsItem()
        # houseNews['thumb_count'] = paramData['thumbCount']
        # houseNews['read_count'] = paramData['viewCount']
        houseNews['url'] = response.url
        houseNews['source_name'] = paramData['source']
        # 标题
        houseNews['title'] = safe_extract(
            response.xpath("//h1[@class='title']/text()"))
        # 时间
        houseNews['release_time'] = safe_extract(
            response.xpath("//span[contains(@class,'activity')]/text()"))

        tmpAuthor = safe_extract(response.xpath(
            "//span[contains(@class,'activity')]/text()"))

        if tmpAuthor:
            houseNews['author'] = paramData['name'] + " - " + tmpAuthor
        else:
            houseNews['author'] = paramData['name']

        article = extract_article(raw_html=response.body)

        houseNews['crawl_time'] = time.time()
        houseNews['content'] = article['cleaned_text']
        # dom文本
        houseNews['html_document'] = safe_extract(
            response.xpath("//div[@id='article-inner']"))
        yield houseNews

    def parse_detail_toutiao(self, response):
        # 获取参数
        paramData = response.meta

        houseNews = HouseNewsItem()

        houseNews['url'] = response.url
        houseNews['source_name'] = paramData['source']
        houseNews['author'] = paramData['name']
        # houseNews['read_count'] = paramData['viewCount']
        # houseNews['comment_count'] = paramData['commentCount']

        # 标题
        houseNews['title'] = safe_extract(response.xpath("//h1/text()"))
        # 时间
        houseNews['release_time'] = safe_extract(
            response.xpath("//span[@class='time']/text()"))
        # 类目
        houseNews['source_category'] = '房产'
        # safe_extract(response.xpath("//div[@class ='curpos']/a[2]/text()"))

        article = extract_article(raw_html=response.body)

        houseNews['crawl_time'] = time.time()
        houseNews['content'] = article['cleaned_text']
        # dom文本
        houseNews['html_document'] = safe_extract(
            response.xpath("//div[@class='detail-main']"))
        # houseNews.html_document =
        #houseNews['read_count'] =response.xpath("//span[@class ='news_read_no']/text()").extract()[1]
        # 点赞量
        #houseNews['thumb_count'] =response.xpath("//span[@class ='news_read_no']/text()").extract()[2]
        # 关键词，热词
        #houseNews['keywords'] = response.xpath("//a[@class='hot_txt']/text()").extract()
        yield houseNews

    def parse_detail_taogonghao(self, response):

        # 获取参数
        paramData = response.meta

        houseNews = HouseNewsItem()

        houseNews['url'] = response.url
        houseNews['source_name'] = paramData['source']
        houseNews['author'] = paramData['name']
        houseNews['source_category'] = '房产头条'
        #
        # 标题
        houseNews['title'] = response.xpath(
            "//h2[@id='activity-name']/text()").extract()[0]
        # 时间
        houseNews['release_time'] = response.xpath(
            "//em[@id='post-date']/text()").extract()[0]

        article = extract_article(raw_html=response.body)

        houseNews['crawl_time'] = time.time()
        houseNews['content'] = article['cleaned_text']
        # dom文本
        houseNews['html_document'] = safe_extract(
            response.xpath("//div[@id='page-content']"))
        yield houseNews

    def parse_detail_wtoutiao(self, response):
        # 获取参数
        self.logger.info('==========%s ' % response.url)
        paramData = response.meta

        houseNews = HouseNewsItem()

        houseNews['url'] = response.url
        houseNews['source'] = paramData['source']
        houseNews['author'] = paramData['name']
        # 标题
        houseNews['title'] = response.xpath("//h1/text()").extract()[0]
        # 关键词，热词
        houseNews['keywords'] = response.xpath(
            "//p[@class='news-tag']/a/text()").extract()

        tmpStr = response.xpath(
            "//div[@class='article_header']/p[2]/text()").extract()[0]
        if tmpStr:
            pubTime = tmpStr.split('.')[1].strip()
            houseNews['release_time'] = pubTime

        article = extract_article(raw_html=response.body)
        houseNews['crawl_time'] = time.time()
        houseNews['content'] = article['cleaned_text']
        # dom文本
        houseNews['html_document'] = safe_extract(
            response.xpath("//div[@class='article_view']"))
        yield houseNews

    def parse_detail_vccoo(self, response):
        # 获取参数
        paramData = response.meta

        houseNews = HouseNewsItem()

        houseNews['url'] = response.url
        houseNews['source_name'] = paramData['source']
        houseNews['author'] = paramData['name']
        # 标题
        houseNews['title'] = response.xpath(
            "//h1[@class='article-title']/a/text()").extract()[0]
        # 时间
        houseNews['release_time'] = response.xpath(
            "//div[@class='author-name']/text()").extract()[1]

        article = extract_article(raw_html=response.body)
        houseNews['crawl_time'] = time.time()
        houseNews['content'] = article['cleaned_text']
        # dom文本
        houseNews['html_document'] = safe_extract(
            response.xpath("//div[@class='article-container']"))
        yield houseNews
