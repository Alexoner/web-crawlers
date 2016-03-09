# Europerail crawler
http://www.europerail.cn/

## requests

### index search 
```code
GET /timetable/indexsearch_result.aspx?fs=PARIS-%E5%B7%B4%E9%BB%8E(%E6%B3%95%E5%9B%BD)&ts=MUNICH-%E6%85%95%E5%B0%BC%E9%BB%91(%E5%BE%B7%E5%9B%BD)&f=FRPAR|FR68600&t=DEMUC|8000261&date=2016-03-08&time=01:00,23:00&anum=1&ynum=1&cnum=0&snum=0&pass=false HTTP/1.1
Host: www.europerail.cn
Connection: keep-alive
Pragma: no-cache
Cache-Control: no-cache
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36
Referer: http://www.europerail.cn/timetable/indexsearch_result.aspx?fs=PARIS-%E5%B7%B4%E9%BB%8E(%E6%B3%95%E5%9B%BD)&ts=MUNICH-%E6%85%95%E5%B0%BC%E9%BB%91(%E5%BE%B7%E5%9B%BD)&f=FRPAR|FR68600&t=DEMUC|8000261&date=2016-03-08&time=01:00,23:00&anum=1&ynum=1&cnum=0&snum=0&pass=false
Accept-Encoding: gzip, deflate, sdch
Accept-Language: en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4
Cookie: ASP.NET_SessionId=h3thu1ndnorjrzxvxfq04c0r; Hm_lvt_0b87ce5b103d18c2a9cf0c583c7232c9=1457403852; Hm_lpvt_0b87ce5b103d18c2a9cf0c583c7232c9=1457417481
```

### login_top
```code
GET /inc/Login_Top.aspx?time=1457407275158 HTTP/1.1
Host: www.europerail.cn
Connection: keep-alive
Pragma: no-cache
Cache-Control: no-cache
Accept: text/html, */*
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36
Referer: http://www.europerail.cn/
Accept-Encoding: gzip, deflate, sdch
Accept-Language: en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4
Cookie: ASP.NET_SessionId=h3thu1ndnorjrzxvxfq04c0r; Hm_lvt_0b87ce5b103d18c2a9cf0c583c7232c9=1457403852; Hm_lpvt_0b87ce5b103d18c2a9cf0c583c7232c9=1457407275

```

### get city list
```code
GET /timetable/inc/GetCityList.ashx?ts=1457407660963&c=eng HTTP/1.1
Host: www.europerail.cn
Connection: keep-alive
Pragma: no-cache
Cache-Control: no-cache
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36
Accept: */*
Referer: http://www.europerail.cn/
Accept-Encoding: gzip, deflate, sdch
Accept-Language: en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4
Cookie: ASP.NET_SessionId=h3thu1ndnorjrzxvxfq04c0r; Hm_lvt_0b87ce5b103d18c2a9cf0c583c7232c9=1457403852; Hm_lpvt_0b87ce5b103d18c2a9cf0c583c7232c9=1457407275

```

### PTPSearch
```code
GET /timetable/inc/PTPSearch.aspx?sid=20160308113042kTd8&f=FRPAR%7cFR68600&t=FRNCE%7cFR75605&date=2016-03-08&time=01:00,23:00&anum=1&ynum=0&cnum=0&snum=0&pass=undefined&_=1457407843083 HTTP/1.1
Host: www.europerail.cn
Connection: keep-alive
Pragma: no-cache
Cache-Control: no-cache
Accept: */*
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36
Referer: http://www.europerail.cn/timetable/indexsearch_result.aspx?fs=PARIS-%E5%B7%B4%E9%BB%8E(%E6%B3%95%E5%9B%BD)&ts=NICE-%E5%B0%BC%E6%96%AF(%E6%B3%95%E5%9B%BD)&f=FRPAR|FR68600&t=FRNCE|FR75605&date=2016-03-08&time=01:00,23:00&anum=1&ynum=0&cnum=0&snum=0&pass=undefined
Accept-Encoding: gzip, deflate, sdch
Accept-Language: en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4
Cookie: ASP.NET_SessionId=h3thu1ndnorjrzxvxfq04c0r; Hm_lvt_0b87ce5b103d18c2a9cf0c583c7232c9=1457403852; Hm_lpvt_0b87ce5b103d18c2a9cf0c583c7232c9=1457407843
```

### ITPTPSearch
```code
GET /timetable/inc/ITPTPSearch.aspx?sid=20160308113042kTd8&f=FRPAR%7cFR68600&t=FRNCE%7cFR75605&date=2016-03-08&time=01:00,23:00&anum=1&ynum=0&cnum=0&snum=0&pass=undefined&_=1457407843083 HTTP/1.1
Host: www.europerail.cn
Connection: keep-alive
Pragma: no-cache
Cache-Control: no-cache
Accept: */*
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36
Referer: http://www.europerail.cn/timetable/indexsearch_result.aspx?fs=PARIS-%E5%B7%B4%E9%BB%8E(%E6%B3%95%E5%9B%BD)&ts=NICE-%E5%B0%BC%E6%96%AF(%E6%B3%95%E5%9B%BD)&f=FRPAR|FR68600&t=FRNCE|FR75605&date=2016-03-08&time=01:00,23:00&anum=1&ynum=0&cnum=0&snum=0&pass=undefined
Accept-Encoding: gzip, deflate, sdch
Accept-Language: en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4
Cookie: ASP.NET_SessionId=h3thu1ndnorjrzxvxfq04c0r; Hm_lvt_0b87ce5b103d18c2a9cf0c583c7232c9=1457403852; Hm_lpvt_0b87ce5b103d18c2a9cf0c583c7232c9=1457407843

```

# loco2.com
https://loco2.com/

## station suggestions
https://loco2.com/station_suggestions?q=berli&limit=10&ignore_session=1

## ticket query
https://loco2.com/journey/london-berlin-1bqgkgf?xhr&
