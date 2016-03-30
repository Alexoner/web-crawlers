# -*- coding: utf-8 -*-

import os
import random
import json
import re
import sys
import time
import itertools
import scrapy

#  from scrapy.loader import ItemLoader
from scrapyprj.items import ScrapyprjItem

# XXX: sys.getdefaultencoding == 'ascii'
reload(sys)
sys.setdefaultencoding('utf-8')

DIRNAME = '{}/../'.format(os.path.dirname(__file__))

try:
    os.mkdir('{}/log'.format(DIRNAME))
    os.mkdir('{}/output'.format(DIRNAME))
except OSError as e:
    pass
file_ok = '{}/log/ok.txt'.format(DIRNAME)
file_error = '{}/log/error.txt'.format(DIRNAME)
file_failed = '{}/log/noline.txt'.format(DIRNAME)
file_pairs = '{}/pairs.txt'.format(DIRNAME)
dir_output = '{}/output'.format(DIRNAME)
go_date_list = [
    '2016-03-30',
    '2016-04-01',
    '2016-04-02',
    '2016-04-03',
    '2016-04-04']
# ['00:00,07:00','07:00,10:00','10:00,14:00','14:00,18:00','18:00,24:00']
time_segments = ['01:00,23:00']
allow_page_turning = True

fwfailed = open(file_failed, 'a')
fwerror = open(file_error, 'a')
fwok = open(file_ok, 'a')

if not os.path.exists(dir_output):
    os.makedirs(dir_output)

#----------------------------------------------------------------------
def read_log_file(filename):
    datasource = []
    if os.path.exists(filename):
        lines = open(filename).readlines()
        for line in lines:
            line = line.strip()
            if line and line.startswith('['):
                pp = line.split()
                fs, f, ts, t, date, time_segment = pp[3:9]
                datasource.append((fs, f, ts, t, date, time_segment))
    return datasource

#----------------------------------------------------------------------
def read_already_got():
    """
        read downloaded requests form log
    """
    dsok = read_log_file(file_ok)
    dserror = read_log_file(file_error)
    dsnoline = read_log_file(file_failed)

    already_got = set()
    already_got = already_got | set(dsok)
    already_got = already_got | set(dsnoline)
    # we are retrying failed requests, so there is no need to exclude
    # error pages when resuming a task
    #  already_got = already_got - set(dserror)

    return already_got

#----------------------------------------------------------------------
def get_sleeptime():
    """
        random sleep
    """
    return random.randint(40, 100)

#----------------------------------------------------------------------
def get_time():
    """
        current time with format
    """
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

#----------------------------------------------------------------------
def read_datasource(filename):
    """
        accumulate seed requests
    """
    print 'loading pairs alreay got ...'
    already_got = read_already_got()
    print 'loaded pairs already got, num = %d' % len(already_got)

    print 'loading datasource ...'
    # element is: (fs,f,ts,t, date, time_segment),
    # example: fs=巴黎&ts=伦敦&f=FRPAR&t=GBLON&date=2016-03-31&time=01:00,23:00
    datasource = []
    pairs = []
    lines = open(filename).readlines()
    for line in lines:
        line = line.strip()  # line format:  巴黎:FRPAR \t 伦敦:GBLON
        if line:
            pp = line.split('\t')
            fs, f = pp[0].split(':')
            ts, t = pp[1].split(':')
            pair = (fs, f, ts, t,)
            pairs.append(pair)

    print('loaded pairs: %d' % len(pairs))

    for go_date in go_date_list:
        for time_segment in time_segments:
            for pair in pairs:
                ds = pair + (go_date, time_segment,)
                if ds not in already_got:
                    datasource.append(ds)
    print 'filtered duplicate ones, datasource num = %d' % len(datasource)
    return datasource

#----------------------------------------------------------------------
def has_train(html):
    """
        got data
    """
    if html.find('没有找到符合您搜索条件的车次') >= 0:
        return False
    else:
        return True

#----------------------------------------------------------------------
def is_error(html):
    """
        error page when IP gets banned by server
    """
    return not html or html.find('ferror') >= 0

RETRY_COOKIEJAR = 4030

class EuroperailSpider(scrapy.Spider):
    handle_httpstatus_list = [400, 404, 407, 502]
    name = "europerail"
    allowed_domains = ["www.europerail.cn"]
    #  start_urls = (
    #  'http://www.www.europerail.cn/',
    #  )

    def __init__(self):
        super(EuroperailSpider, self).__init__()
        self.datasource = read_datasource(file_pairs)

    def start_requests(self):

        i = 0
        # date as the most significant bit, which we iterate over last
        for fs, f, ts, t, date, time_segment in self.datasource:
            url = 'http://www.europerail.cn/timetable/indexsearch_result.aspx?fs=%s&ts=%s&f=%s&t=%s&date=%s&time=%s&anum=1&ynum=0&cnum=0&snum=0&pass=false' % \
                (fs, ts, f, t, date, time_segment)
            self.logger.debug(u'seed url: %s', url)

            i += 1
            yield scrapy.Request(
                url,
                callback=self.parse_seed,
                headers={
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                    "Accept-Encoding": "gzip, deflate, sdch",
                    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,es;q=0.2,pt;q=0.2,ru;q=0.2,zh-TW;q=0.2",
                    "Connection": "keep-alive",
                    "Host": "www.europerail.cn",
                    "Referer": "http://www.europerail.cn/",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",
                },
                meta={
                    'item': {
                        'uid': 'seed',
                        'fs': fs,
                        'ts': ts,
                        'f': f,
                        't': t,
                        'date': date,
                        'time_segment': time_segment,
                    },
                    'dont_merge_cookies': True,
                    'cookiejar': i,
                }
            )

    def parse(self, response):
        pass

    def parse_seed(self, response):
        """ Parse seed urls to generate sequential sub-requests
        @url http://www.europerail.cn/timetable/indexsearch_result.aspx?fs=%E8%92%99%E5%BD%BC%E5%88%A9%E5%9F%83&ts=%E6%B3%A2%E8%8C%A8%E5%9D%A6&f=FRMPL&t=DEXXO&date=2016-03-29&time=01:00,23:00&anum=1&ynum=0&cnum=0&snum=0&pass=false
        @returns items 0 16
        @returns requests 0 0
        @scrapes
        """
        try:
            sid = response.xpath(
                '//html').re("var sid='(.*?)'")[0].encode('utf-8')
        except Exception as e:
            self.logger.error('%s', e)
            return
        opentime = '%d' % (time.time() * 1000)
        extra_info = response.meta['item']
        url = 'http://www.europerail.cn/timetable/inc/PTPSearch.aspx?sid=%s&f=%s&t=%s&date=%s&time=%s&anum=1&ynum=0&cnum=0&snum=0&pass=false&_=%s' % \
            (
                sid,
                extra_info['f'],
                extra_info['t'],
                extra_info['date'],
                extra_info['time_segment'],
                opentime,
            )
        self.logger.info(u'yield detail page: %s', url)
        yield scrapy.Request(
            url,
            callback=self.parse_detail,
            headers={
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, sdch",
                "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,es;q=0.2,pt;q=0.2,ru;q=0.2,zh-TW;q=0.2",
                "Connection": "keep-alive",
                "Host": "www.europerail.cn",
                "Referer": response.url,
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest",
            },
            meta={
                'item': {
                    'sid': sid,
                    'uid': 'detail',
                    'fs': extra_info['fs'],
                    'ts': extra_info['ts'],
                    'f': extra_info['f'],
                    't': extra_info['t'],
                    'date': extra_info['date'],
                    'time_segment': extra_info['time_segment'],
                    'referer': response.url,
                },
                'dont_merge_cookies': False,
                'cookiejar': response.meta.get('cookiejar'),
                'proxy': response.request.meta.get('proxy'),
            }
        )

    def parse_detail(self, response):
        extra_info = response.meta['item']

        line = '%s %s %s %s %s %s' % (
            extra_info['fs'],
            extra_info['f'],
            extra_info['ts'],
            extra_info['t'],
            extra_info['date'],
            extra_info['time_segment'])
        if is_error(response.body):
            self.logger.error(u'%s %s %s', 'ERROR', line, 'ferror')
            log = '[%s] ERROR\t %s %s' % (
                get_time(), line, 'ferror')
            fwerror.write(log + '\n')  # report error
            fwerror.flush()
            # fire terminal alarm
            print('\a')

            # 如果错误，则直接休息10~30 seconds
            stime = random.randint(10, 30)
            self.logger.info(u'not sleeping %s seconds' % stime)
            #  time.sleep(stime)

            self.logger.info(
                u'yield request %s again!',
                extra_info['referer'])
            yield scrapy.Request(
                extra_info['referer'],
                callback=self.parse_seed,
                headers={
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                    "Accept-Encoding": "gzip, deflate, sdch",
                    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,es;q=0.2,pt;q=0.2,ru;q=0.2,zh-TW;q=0.2",
                    "Connection": "keep-alive",
                    "Host": "www.europerail.cn",
                    "Referer": "http://www.europerail.cn/",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",
                },
                meta={
                    'item': {
                        'uid': 'seed',
                        'fs': extra_info['fs'],
                        'ts': extra_info['ts'],
                        'f': extra_info['f'],
                        't': extra_info['t'],
                        'date': extra_info['date'],
                        'time_segment': extra_info['time_segment'],
                    },
                    'dont_merge_cookies': True,
                    'cookiejar': response.meta['cookiejar'] + RETRY_COOKIEJAR,
                },
                dont_filter=True,
            )
        elif has_train(response.body):
            self.logger.info(u'%s %s', 'OK', line)
            log = '[%s] OK\t %s' % (get_time(), line)
            fwok.write(log + '\n')  # report ok
            fwok.flush()

            outputfile = os.path.join(
                dir_output, '%s_%s_%s_%s_%s.html' % (
                    extra_info['f'],
                    extra_info['t'],
                    extra_info['date'],
                    extra_info['time_segment'].split(',')[0].replace(':', ''),
                    extra_info['time_segment'].split(',')[1].replace(':', ''))
            )
            fw = open(outputfile, 'w')
            fw.write(response.body)
            fw.close()

            try:
                for item in self.generate_items(response):
                    yield item
            except Exception as e:
                self.logger.error('error when generating items: %s' % e)

            if allow_page_turning:
                ## 下面开始翻页逻辑 ##
                # 解析当前最大出发时间
                start_time_list = response.xpath(
                    "//table[@class='zy_guding_1']/tr/td[2]/span/text()").extract()
                if not start_time_list:
                    self.logger.error(
                        u'failed to get start time list using xpath.')
                else:
                    start_time_list.sort()
                    latest_start_time = start_time_list[-1]
                    # 如果当前最大时间在time_segment的开始时间之前，则break，无需翻页了，已经没有了，否则构造新的time_segment
                    if latest_start_time <= extra_info['time_segment'].split(',')[
                            0]:
                        self.logger.info(u'已经没有更晚的车次了！')
                    else:
                        latest_hour, latest_minute = latest_start_time.split(
                            ':')
                        # ceil time at 30 minutes or 0 minutes
                        next_start_time = '{}:{}'.format(latest_minute <= '30' and latest_hour or int(latest_hour) + 1,
                                                         latest_minute <= '30' and '30' or '00')
                        time_segment = '%s,%s' % (
                            next_start_time,
                            extra_info['time_segment'].split(',')[1])
                        self.logger.info(
                            u'还有更晚车次，重新构造time_segment查询： %s' %
                            time_segment)

                        ssnum = extra_info.get('ssnum') and extra_info[
                            'ssnum'] + 1 or 1
                        url = 'http://www.europerail.cn/timetable/inc/PTPSearch.aspx?ssnum=%s&stype=down&sid=%s&f=%s&t=%s&date=%s&time=%s&anum=1&ynum=0&cnum=0&snum=0&pass=false&_=%s' % \
                            (
                                ssnum,
                                extra_info['sid'],
                                extra_info['f'],
                                extra_info['t'],
                                extra_info['date'],
                                time_segment,
                                '%d' % (time.time() * 1000),
                            )
                        yield scrapy.Request(
                            url,
                            callback=self.parse_detail,
                            headers={
                                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                                "Accept-Encoding": "gzip, deflate, sdch",
                                "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,es;q=0.2,pt;q=0.2,ru;q=0.2,zh-TW;q=0.2",
                                "Connection": "keep-alive",
                                "Host": "www.europerail.cn",
                                #  "Referer": response.url, # the referer middleware will do the job?
                                "Upgrade-Insecure-Requests": "1",
                                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",
                                "X-Requested-With": "XMLHttpRequest",
                            },
                            meta={
                                'item': {
                                    'uid': 'detail',
                                    'fs': extra_info['fs'],
                                    'ts': extra_info['ts'],
                                    'f': extra_info['f'],
                                    't': extra_info['t'],
                                    'date': extra_info['date'],
                                    'time_segment': time_segment,
                                    'ssnum': ssnum,
                                    'sid': extra_info['sid'],
                                    'referer': response.url,
                                },
                                'dont_merge_cookies': True,
                                'cookiejar': response.meta['cookiejar'],
                                'proxy': response.request.meta.get('proxy'),
                            }
                        )
        else:
            self.logger.info(u'%s %s', 'NOLINE', line)
            log = '[%s] NOLINE\t %s' % (get_time(), line)
            fwfailed.write(log + '\n')  # report failed
            fwfailed.flush()

    def generate_items(self, response):
        extra_info = response.meta['item']
        # the returned html is malformed(without root like <html><body> and so on),
        # XPATH may fail
        train_tables = response.xpath('//table[@width="1157"]')
        #  [3].xpath('./tr/td[4]/a').extract()[0]
        train_list = response.xpath(
            '//td[@width="131"]/strong/text()').extract()
        train_list_indexes = range(len(train_list))
        seat_type_indexes = [5, 6]
        items = []
        for (i, k) in itertools.product(train_list_indexes, seat_type_indexes):

            seat_list = train_tables[i].xpath('./tr/td[{0}]/table/tr/td/a/text()'.format(
                k
            )).extract()

            price_list = train_tables[i].xpath('./tr/td[{0}]/table/tr/td/strong/text()'.format(
                k
            )).extract()

            for j, seat in enumerate(seat_list):
                item = {}
                item['adults'] = 1
                item['children'] = 0
                item['seniors'] = 0
                item['youth'] = 0
                item["departure_date"] = extra_info['date']
                item["start_city_name"] = extra_info['fs']
                item["dest_city_name"] = extra_info['ts']
                item["site"] = "www.europerail.cn"
                # 火车车次
                train_no = train_list[i]
                item["train_no"] = train_no
                # 发车站点
                from_station = train_tables[i].xpath(
                    './tr/td[2]/text()[2]'.format()).extract()[0].replace(
                    r"\u00A0", "").strip()
                item["from_station"] = from_station
                item["from_city_code"] = extra_info['f']
                # 发车时间
                from_date = train_tables[i].xpath(
                    './tr/td[2]/text()[1]'.format()).extract()[0]
                from_time = train_tables[i].xpath(
                    './tr/td[@width="200"][1]/span/text()'.format()).extract()[0]

                # 2016-
                year = extra_info.get("date")[0:5]
                from_time = '%s %s:00' % (extra_info.get("date"), from_time)
                item["from_time"] = from_time
                #  到站站点
                to_station = train_tables[i].xpath("./tr/td[@width='200'][2]/text()[2]".format(
                )).extract()[0].replace(r"\u00A0", "").strip()
                item["to_station"] = to_station
                item["to_city_code"] = extra_info['t']
                #  到站时间
                to_time = train_tables[i].xpath("./tr/td[@width='200'][2]/span/text()".format(
                )).extract()[0]
                to_year = year
                to_date = train_tables[i].xpath("./tr/td[3]/text()[1]".format(
                )).extract()[0]
                if to_date < from_date:
                    #  XXX:
                    #  HAPPY NEW YEAR!
                    to_year = "%s" % (int(year) + 1)
                    item[
                        "to_time"] = '%s-%s %s:00' % (to_year, to_date, to_time)
                # 用时
                spend_time = train_tables[i].xpath("./tr/td[@width='180'][1]/span/text()".format(
                )).extract()[0]
                item["time_length"] = spend_time
                # 价格
                price = price_list[j]
                item["price"] = price
                # 座位等级
                if (k == 5):
                    seat_grade = "一等舱".encode('utf-8')
                elif (k == 6):
                    seat_grade = "二等舱".encode('utf-8')
                item["seat_grade"] = seat_grade
                seat_type = seat_list[j]
                item["seat_type"] = seat_type.encode('utf-8')
                transfer_flag = train_tables[i].xpath(
                    './tr/td[4]/a/@href'.format()).extract()
                if transfer_flag:
                    try:
                        transfer_items = self.extract_transfer_trains(
                            response, transfer_flag)
                        if transfer_items:
                            train_no = '%s,%s' % (item['train_no'],
                                                  ','.join(map(lambda x: x['train_no'], transfer_items)))
                            item["train_no"] = '%s,%s' % (
                                l.get_value("train_no"), train_no_transfer)
                            item['segs'] = json.dumps(transfer_items)
                    except Exception as e:
                        self.logger.error('parse transfer train error: %s', e)
                yield ScrapyprjItem(item)

    def extract_transfer_trains(self, response, transfer_flag):
        # search for pattern!
        match = re.search(
            r"javascript:showDivInfo\('(travelchange\S+)'\);",
            transfer_flag[0])
        if match:
            transfer_id = match.group(1)
        else:
            return

        transfer_list = response.xpath("//div[@id='{0}']/table[@class='zy_search_hc2']/tr/td[@width='108'][@align='center']/strong/text()".format(
            transfer_id,
        )).extract()
        transfer_items = []
        if transfer_list:
            self.logger.info('%d transfer trains(中转车)', len(transfer_list))
        for transfer_index, transfer_train in enumerate(
                transfer_list):
            transfer_item = {}
            # 车次
            train_no_transfer = transfer_list[transfer_index]
            transfer_item["train_no"] = train_no_transfer
            #  出发时间
            from_time_transfer = response.xpath(
                "//div[@id='{0}']/table[{1}]/tr/td[@width='180'][1][@align='center']/span/text()".format(
                    transfer_id,
                    (2 * transfer_index + 2))
            ).extract()[0]
            transfer_item["from_time"] = from_time_transfer
            # 出发站点
            start_station_transfer = response.xpath(
                "//div[@id='{0}']/table[{1}]/tr/td[@width='180'][1][@align='center']/strong[1/text()]".format(
                    transfer_id,
                    (2 * transfer_index + 2),
                )).extract()[0]
            transfer_item["from_station"] = start_station_transfer.replace(
                u"\u00A0", "").strip()
            # 到达时间
            to_time_transfer = response.xpath("//div[@id='{0}']/table[{1}]/tr/td[@width='180'][2][@align='center']/span/text()".format(
                transfer_id,
                (2 * transfer_index + 2),
            )).extract()[0]
            transfer_item["to_time"] = to_time_transfer.replace(
                r"\u00A0", "").strip()
            # 到站站点
            to_station_transfer = response.xpath("//div[@id='{0}']/table[{1}]/tr/td[@width='180'][2][@align='center']/strong[1]/text()".format(
                transfer_id,
                (2 * transfer_index + 2),
            )).extract()[0]
            transfer_item["to_station"] = to_station_transfer
            transfer_item["adults"] = 1
            transfer_item["children"] = 0
            transfer_item["seniors"] = 0
            transfer_item["youth"] = 0
            transfer_item["departure_date"] = response.meta['item']['date']
            transfer_item["start_city_name"] = response.meta['item']['fs']
            transfer_item["dest_city_name"] = response.meta['item']['ts']
            transfer_items.append(transfer_item)

        return transfer_items
