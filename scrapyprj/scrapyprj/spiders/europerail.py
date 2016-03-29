# -*- coding: utf-8 -*-

import os
import random
import sys
import time
import scrapy

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
# ,'2016-03-29','2016-03-30','2016-03-31','2016-04-01','2016-04-02','2016-04-03']
go_date_list = ['2016-03-30']
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

    for date in go_date_list:
        for time_segment in time_segments:
            for pair in pairs:
                ds = pair + (date, time_segment,)
                if ds not in already_got:
                    datasource.append(ds)
    print 'done, datasource num = %d' % len(datasource)
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
            got_train = False
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
                        'go_date': date,
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
            raise e
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
                    'go_date': extra_info['go_date'],
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
            extra_info['go_date'],
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
                        'go_date': extra_info['go_date'],
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

            got_train = True

            outputfile = os.path.join(
                dir_output, '%s_%s_%s_%s_%s.html' % (
                    extra_info['f'],
                    extra_info['t'],
                    extra_info['go_date'],
                    extra_info['time_segment'].split(',')[0].replace(':', ''),
                    extra_info['time_segment'].split(',')[1].replace(':', ''))
            )
            fw = open(outputfile, 'w')
            fw.write(response.body)
            fw.close()

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
                        time_segment = '%s,%s' % (
                            latest_start_time,
                            extra_info['time_segment'].split(',')[1])
                        self.logger.info(
                            u'还有更晚车次，重新构造time_segment查询： %s' %
                            time_segment)

                        url = 'http://www.europerail.cn/timetable/inc/PTPSearch.aspx?sid=%s&f=%s&t=%s&date=%s&time=%s&anum=1&ynum=0&cnum=0&snum=0&pass=false&_=%s' % \
                            (
                                extra_info['sid'],
                                extra_info['f'],
                                extra_info['t'],
                                extra_info['go_date'],
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
                                    'go_date': extra_info['go_date'],
                                    'time_segment': time_segment,
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
