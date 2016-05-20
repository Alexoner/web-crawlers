# captured `rails.ctrip.com` requests

## landing page
```code
GET /ptp/FRPAR-DEMUC?departureDate=2016-03-15&starttime=06:00-24:00&searchType=0&pageStatus=0&passHolders=0&adult=2&child=0&youth=0&seniors=0 HTTP/1.1
Host: rails.ctrip.com
Connection: keep-alive
Pragma: no-cache
Cache-Control: no-cache
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36
Referer: http://rails.ctrip.com/ptp/FRPAR-DEMUC?departureDate=2016-03-15&starttime=06:00-24:00&searchType=0&pageStatus=0&passHolders=0&adult=2&child=0&youth=0&seniors=0
Accept-Encoding: gzip, deflate, sdch
Accept-Language: en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4
Cookie: ASP.NET_SessionSvc=MTAuOC45Mi42fDkwOTB8amlucWlhb3xkZWZhdWx0fDE0NDkxMzUxMTAyNTQ; ASP.NET_SessionId=b0dnhgd0h2hstxlp45wq5p1m; _abtest_userid=c699920a-a673-439b-ae18-ef758f54755a; Customer=HAL=ctrip_cn; _ctm_t=ctrip; _gat=1; _bfa=1.1457425340091.1r2af1.1.1457591811760.1457779195509.5.27; _bfs=1.5; _bfi=p1%3D103112%26p2%3D103112%26v1%3D27%26v2%3D26; _ga=GA1.2.630276705.1457425344; __zpspc=9.5.1457779198.1457779667.5%234%7C%7C%7C%7C%7C%23; _jzqco=%7C%7C%7C%7C%7C1.1281512317.1457425343652.1457779606738.1457779667652.1457779606738.1457779667652.0.0.0.22.22; appFloatCnt=13

```

## query tickets
```code
POST /international/Ajax/PTPProductListHandler.ashx?Action=GetPTPProductList HTTP/1.1
Host: rails.ctrip.com
Connection: keep-alive
Content-Length: 366
Pragma: no-cache
Cache-Control: no-cache
Origin: http://rails.ctrip.com
If-Modified-Since: Thu, 01 Jan 1970 00:00:00 GMT
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Accept: */*
Referer: http://rails.ctrip.com/ptp/FRPAR-DEMUC?departureDate=2016-03-15&starttime=06:00-24:00&searchType=0&pageStatus=0&passHolders=0&adult=2&child=0&youth=0&seniors=0
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4
Cookie: ASP.NET_SessionSvc=MTAuOC45Mi42fDkwOTB8amlucWlhb3xkZWZhdWx0fDE0NDkxMzUxMTAyNTQ; ASP.NET_SessionId=b0dnhgd0h2hstxlp45wq5p1m; _abtest_userid=c699920a-a673-439b-ae18-ef758f54755a; Customer=HAL=ctrip_cn; _ctm_t=ctrip; _gat=1; _bfi=p1%3D103112%26p2%3D103112%26v1%3D27%26v2%3D26; _ga=GA1.2.630276705.1457425344; __zpspc=9.5.1457779198.1457779667.5%234%7C%7C%7C%7C%7C%23; _jzqco=%7C%7C%7C%7C%7C1.1281512317.1457425343652.1457779606738.1457779667652.1457779606738.1457779667652.0.0.0.22.22; appFloatCnt=13; _bfa=1.1457425340091.1r2af1.1.1457591811760.1457779195509.5.28; _bfs=1.6

```

```python
{
'Accept':*/*
'Accept-Encoding':'gzip, deflate'
'Accept-Language':'en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4'
'Cache-Control':'no-cache'
'Connection':'keep-alive'
'Content-Length':366
'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'
'Cookie':'ASP.NET_SessionSvc=MTAuOC45Mi4xNzJ8OTA5MHxqaW5xaWFvfGRlZmF1bHR8MTQ0OTEzNzUxNzEwMg; ASP.NET_SessionId=ofldmiolbnioxpjvjzon0v22; _bfa=1.1457853128485.3ik6k8.1.1457853128485.1457853128485.1.1; _bfs=1.1'
'Host':'rails.ctrip.com'
'If-Modified-Since':'Thu, 01 Jan 1970 00:00:00 GMT'
'Origin':'http://rails.ctrip.com'
'Pragma':'no-cache'
'Referer':'http://rails.ctrip.com/ptp/FRPAR-DEMUC?departureDate=2016-03-15&starttime=06:00-24:00&searchType=0&pageStatus=0&passHolders=0&adult=2&child=0&youth=0&seniors=0'
'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
}
```

## cookie
1. landing page set-cookie
2. landing page XPath: "/html/head/script[26]"

## bfa.min.js analysis
```javascript
readBfa: function() {
                    var a = this.getItem("_bfa", "", !0);
                    a && y._bfa.test(a) && (a = a.split("."),
                    6 < a.length && (this.bfa = a));
                    this.bfa || (a = this.enterTime,
                    this.bfa = [1, a, this.uniqueId_().toString(36), 1, a, a, 0, 0],
                    this._isNewVisitor = 1)
                },

sessRead: function() {
                    var a = this.getItem("_bfs", "", !0);
                    (!this._isNewVisitor && a && y._bfs.test(a) ? (this.bfs = a.split("."),
                    this.bfs[1] = this.plus_(this.bfs[1])) : (this._isNewSession = 1,
                    this.bfs = [1, 1],
                    this.bfa[4] = this.bfa[5],
                    this.bfa[5] = this.enterTime,
                    this.bfa[6] = this.plus_(this.bfa[6])));
                    this.bfa[7] = this.plus_(this.bfa[7]);
                    this.sessWrite()
                },

sessWrite: function() {
                    this.setItem("_bfa", this.bfa.join("."), 63072E6);
                    this.setItem("_bfs", this.bfs.join("."), 18E5)
                },
this.uniqueId_ = function() {
    return c.getRand()^c.CLI.getHash()&2147483647
}

c.getRand = function () {
    return(""+Math.random()).slice(-8)
}

c.getHash: function() {
    for (var q = f.history.length, n = [browser.appName, browser.appVersion, locale, browser.platform, browser.userAgent, l, screen.width + screen.height, d, (page.cookie ? page.cookie : ""), (page.referrer ? page.referrer : "")].join(""), g = n.length; 0 < q; )
        n += q-- ^ g++;
    return c.hash(n)
}

c.hash = function(a) {
                var b = 1, d = 0, e;
                if (!c.isEmpty(a))
                    for (b = 
                    0,
                    e = a.length - 1; 0 <= e; e--)
                        d = a.charCodeAt(e),
                        b = (b << 6 & 268435455) + d + (d << 14),
                        d = b & 266338304,
                        b = (0 != d ? b ^ d >> 21 : b);
                return b
            }

```
JS execution
```javascript
getHash() {
    for (var q = 2, n = [ "Netscape", "5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36", "en-us","MacIntel", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36", 0, 1920+1080, "24-bit", "", ""].join(""), g = 266;0 < q;>)
        n += q-- ^ g++;
    return c.hash(n);
}
```
