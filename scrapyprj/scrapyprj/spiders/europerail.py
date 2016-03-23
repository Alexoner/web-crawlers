# -*- coding: utf-8 -*-

from lxml import html as html_parser
import os
import random
import re
import sys
import time
import scrapy
import urllib2

reload(sys)
sys.setdefaultencoding('utf-8')

DIRNAME = '{}/..'.format(os.path.dirname(__file__))

file_ok = '{}/ok.txt'.format(DIRNAME)
file_error = '{}/error.txt'.format(DIRNAME)
file_failed = '{}/noline.txt'.format(DIRNAME)
file_pairs = '{}/pairs.txt'.format(DIRNAME)
dir_output = '{}/output'.format(DIRNAME)
# ,'2016-03-29','2016-03-30','2016-03-31','2016-04-01','2016-04-02','2016-04-03']
go_date_list = ['2016-03-28']
# ['00:00,07:00','07:00,10:00','10:00,14:00','14:00,18:00','18:00,24:00']
time_segments = ['01:00,23:00']
allow_page_turning = False

fwfailed = open(file_failed, 'a')
fwerror = open(file_error, 'a')
fwok = open(file_ok, 'a')

if not os.path.exists(dir_output):
    os.makedirs(dir_output)

#----------------------------------------------------------------------
def read_log_file(filename):
    """"""
    datasource = []
    if os.path.exists(filename):
        lines = open(filename).readlines()
        for line in lines:
            line = line.strip()
            if line and line.startswith('['):
                pp = line.split()
                fs, f, ts, t = pp[3:7]
                datasource.append((fs, f, ts, t))
    return datasource

#----------------------------------------------------------------------
def read_already_got():
    """"""
    dsok = read_log_file(file_ok)
    dserror = read_log_file(file_error)
    dsnoline = read_log_file(file_failed)

    already_got = set()
    already_got = already_got | set(dsok)
    already_got = already_got | set(dsnoline)
    for e in dserror:
        if e in already_got:
            already_got.remove(e)

    return already_got

#----------------------------------------------------------------------
def get_sleeptime():
    """"""
    return random.randint(40, 100)

#----------------------------------------------------------------------
def get_time():
    """"""
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

#----------------------------------------------------------------------
def read_datasource(filename):
    """"""
    print 'loading pairs alreay got ...'
    already_got = read_already_got()
    print 'loaded pairs already got, num = %d' % len(already_got)

    print 'loading datasource ...'
    # element is: (fs,f,ts,t), example: fs=巴黎&ts=伦敦&f=FRPAR&t=GBLON
    datasource = []
    lines = open(filename).readlines()
    for line in lines:
        line = line.strip()  # line format:  巴黎:FRPAR \t 伦敦:GBLON
        if line:
            pp = line.split('\t')
            fs, f = pp[0].split(':')
            ts, t = pp[1].split(':')
            ds = (fs, f, ts, t)
            if ds not in already_got:
                datasource.append(ds)
                pass
            pass
        pass
    print 'done, datasource num = %d' % len(datasource)
    return datasource

#----------------------------------------------------------------------
def has_train(html):
    """"""
    if html.find('没有找到符合您搜索条件的车次') >= 0:
        return False
    else:
        return True

#----------------------------------------------------------------------
def is_error(html):
    """"""
    if not html or html.find('ferror') >= 0:
        return True
    else:
        return False

class EuroperailSpider(scrapy.Spider):
    handle_httpstatus_list = [400, 404, 502]
    name = "europerail"
    allowed_domains = ["www.europerail.cn"]
    #  start_urls = (
    #  'http://www.www.europerail.cn/',
    #  )

    def __init__(self):
        super(EuroperailSpider, self).__init__()
        #  self.fwfailed = open(file_failed, 'w')
        #  self.fwerror = open(file_error, 'w')
        #  self.fwok = open(file_ok, 'w')
        self.datasource = read_datasource(file_pairs)

    def start_requests(self):

        for fs, f, ts, t in self.datasource:
            for go_date in go_date_list:
                got_train = False
                for time_segment in time_segments:
                    #  line = '%s %s %s %s %s %s' % (fs,f,ts,t,go_date,time_segment)
                    #  print '[%s] getting\t %s' % (get_time(), line)
                    url = 'http://www.europerail.cn/timetable/indexsearch_result.aspx?fs=%s&ts=%s&f=%s&t=%s&date=%s&time=%s&anum=1&ynum=0&cnum=0&snum=0&pass=false' % \
                        (fs, ts, f, t, go_date, time_segment)
                    self.logger.debug('seed url: %s', url)

                    yield scrapy.Request(url,
                                         callback=self.parse_seed,
                                         headers={
                                             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                                             "Accept-Encoding": "gzip, deflate, sdch",
                                             "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,es;q=0.2,pt;q=0.2,ru;q=0.2,zh-TW;q=0.2",
                                             "Connection": "keep-alive",
                                             "Host": "www.europerail.cn",
                                             "Referer": "http://www.europerail.cn/timetable/",
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
                                                 'go_date': go_date,
                                                 'time_segment': time_segment,
                                             },
                                         }
                                         )

    def parse(self, response):
        pass

    def parse_seed(self, response):
        sid = response.xpath('//html').re("var sid='(.*?)'")
        opentime = '%d' % (time.time() * 1000)
        extra_info = response.meta['item']
        url = 'http://www.europerail.cn/timetable/inc/PTPSearch.aspx?sid=%s&f=%s&t=%s&date=%s&time=%s&anum=1&ynum=0&cnum=0&snum=0&pass=false&_=%s' % \
            (
                sid,
                extra_info['f'],
                extra_info['t'],
                extra_info['go_date'],
                extra_info['time_segment'],
                opentime,
            )
        yield scrapy.Request(url,
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
                                     'go_date': extra_info['go_date'],
                                     'time_segment': extra_info['time_segment'],
                                     'referer': url,
                                 },
                             }
                             )

    def parse_detail(self, response):
        extra_info = response.meta['item']

        line = '%s %s %s %s %s %s' % (
            extra_info['fs'],
            extra_info['f'],
            extra_info['ts'],
            extra_info['t'],
            extra_info['go_date'],
            extra_info['time_segment'])
        if is_error(response.body):
            log = '[%s] error\t %s %s' % (
                get_time(), line, 'ferror')
            print log
            fwerror.write(log + '\n')  # report error
            fwerror.flush()

            # 如果错误，则直接休息10~30分钟
            stime = random.randint(10, 30) * 60
            print 'sleep %s seconds' % stime

            yield scrapy.Request(
                extra_info['item']['referer'],
                callback=self.parse_seed,
                headers={
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                    "Accept-Encoding": "gzip, deflate, sdch",
                    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,es;q=0.2,pt;q=0.2,ru;q=0.2,zh-TW;q=0.2",
                    "Connection": "keep-alive",
                    "Host": "www.europerail.cn",
                    "Referer": "http://www.europerail.cn/timetable/",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",
                },
                meta={
                    'item': {
                        'uid': 'seed',
                        'fs': extra_info['item']['fs'],
                        'ts': extra_info['item']['ts'],
                        'f': extra_info['item']['f'],
                        't': extra_info['item']['t'],
                        'go_date': extra_info['item']['go_date'],
                        'time_segment': extra_info['item']['time_segment'],
                    },
                }
            )
            #  time.sleep(stime)
        elif has_train(response.body):
            log = '[%s] ok\t %s' % (get_time(), line)
            print log
            fwok.write(log + '\n')  # report ok
            fwok.flush()

            got_train = True

            outputfile = os.path.join(
                dir_output, '%s_%s_%s_%s.html' % (
                    extra_info['f'],
                    extra_info['t'],
                    extra_info['time_segment'].split(',')[0].replace(':', ''),
                    extra_info['time_segment'].split(',')[1].replace(':', ''))
            )
            fw = open(outputfile, 'w')
            fw.write(response.body)
            fw.close()

            if allow_page_turning:
                ## 下面开始翻页逻辑 ##
                # 解析当前最大出发时间
                tree = html_parser.fromstring(response.body)
                start_time_list = tree.xpath(
                    "//table[@class='zy_guding_1']/tr/td[2]/span/text()")
                if not start_time_list:
                    print 'failed to get start time list using xpath.'
                else:
                    start_time_list.sort()
                    latest_start_time = start_time_list[-1]
                    # 如果当前最大时间在time_segment的开始时间之前，则break，无需翻页了，已经没有了，否则构造新的time_segment
                    if latest_start_time <= extra_info['time_segment'].split(',')[
                            0]:
                        print '已经没有更晚的车次了！'
                    else:
                        time_segment = '%s,%s' % (
                            latest_start_time,
                            extra_info['time_segment'].split(',')[1])
                        print '还有更晚车次，重新构造time_segment查询： %s' % time_segment

                        # sleep for a while
                        stime = get_sleeptime()
                        print 'sleep %s seconds' % stime
                        #  time.sleep(stime)
                        url = 'http://www.europerail.cn/timetable/inc/PTPSearch.aspx?sid=%s&f=%s&t=%s&date=%s&time=%s&anum=1&ynum=0&cnum=0&snum=0&pass=false&_=%s' % \
                            (
                                extra_info['sid'],
                                extra_info['item']['f'],
                                extra_info['item']['t'],
                                extra_info['item']['go_date'],
                                extra_info['item']['time_segment'],
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
                                "Referer": response.url,
                                "Upgrade-Insecure-Requests": "1",
                                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",
                                "X-Requested-With": "XMLHttpRequest",
                            },
                            meta={
                                'item': {
                                    'uid': 'seed',
                                    'fs': extra_info['item']['fs'],
                                    'ts': extra_info['item']['ts'],
                                    'f': extra_info['item']['f'],
                                    't': extra_info['item']['t'],
                                    'go_date': extra_info['item']['go_date'],
                                    'time_segment': time_segment,
                                },
                            }
                        )
        else:
            log = '[%s] noline\t %s' % (get_time(), line)
            print log
            fwfailed.write(log + '\n')  # report failed
            fwfailed.flush()
