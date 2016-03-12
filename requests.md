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


# www.b-europe.com/Travel

## station search
```code
POST /Update/Search/StationSearch?ds=f29afce8-7586-4803-8dec-8eb9377bfef6&lang=en&channelId=64b729c2-7b18-4dcd-a42e-980cd747c15f HTTP/1.1
Host: www.b-europe.com
Connection: keep-alive
Content-Length: 120
Pragma: no-cache
Cache-Control: no-cache
Accept: application/json, text/javascript, */*; q=0.01
Origin: https://www.b-europe.com
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36
Content-Type: application/json
Referer: https://www.b-europe.com/Travel
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4
Cookie: websitecrosssite_production#lang=en; SitePreferences_www.b-europe.com={"c":"OT","l":"en","r":"EUR","u":false,"h":"64b729c2-7b18-4dcd-a42e-980cd747c15f"}; referrerInfo_64b729c2-7b18-4dcd-a42e-980cd747c15f=; _ga=GA1.2.30767610.1457526788; _dc_gtm_UA-4476891-6=1; _wt.mode-984274=WT3y5sb-9KDcn8~; _wt.user-984274=WT35cpysxR96HIwBMSM7JqL9RjcVrXAYX2Wn-o2ZlzMm3Nx4yoVR6VpxoH2hH43arkqT4CWcYKwKZaobsip7U4ulUsnwwLyNcm9djjL0shB4lY~

Request Payload:
{
    "Criteria": "München Hbf (De) ( Munich, Munchen, Muenchen )",
    "OriginOrDestination": "Destination",
    "RCodeRestrictions": null,
    "GetGuidance": true,
    "AjaxCallOrigin": "railtour"
}

Response:
[{
    "Title": "München Hbf (De) ( Munich, Munchen, Muenchen )",
    "DisplayTitle": "München Hbf (De)",
    "RCode": "DEBEG",
    "Synonyms": "Munich, Munchen, Muenchen",
    "InfoIcon": "icon-icoTrain"
}]
```

## query landing page
https://www.b-europe.com/Travel/Booking/Tickets?autoactivatestep2=true&origin=FRPAR&dest=DEBEG&traveltype=OneWay&outbound=10%2F03%2F2016&outboundt=&outboundtp=DepartureTime&inbound=&inboundt=&inboundtp=DepartureTime&comfortclass=2&ticketlanguage=en&travelparty=%257B%2522P%2522%253A%255B%257B%2522T%2522%253A%25220%2522%257D%252C%257B%2522T%2522%253A%25224%2522%257D%252C%257B%2522T%2522%253A%25226%2522%257D%252C%257B%2522T%2522%253A%252212%2522%257D%252C%257B%2522T%2522%253A%2522Y%2522%257D%252C%257B%2522T%2522%253A%2522A%2522%257D%252C%257B%2522T%2522%253A%2522S%2522%257D%255D%252C%2522M%2522%253Afalse%257D#stepTravelWish

https://www.b-europe.com/Travel/Booking/Tickets?autoactivatestep2=true&origin=FRPAR&dest=DEBEG&traveltype=OneWay&outbound=10/03/2016&outboundt=&outboundtp=DepartureTime&inbound=&inboundt=&inboundtp=DepartureTime&comfortclass=2&ticketlanguage=en&travelparty={"P":[{"T":"0"},{"T":"4"},{"T":"6"},{"T":"12"},{"T":"Y"},{"T":"A"},{"T":"S"}],"M":false}#stepTrainSelection
travelparty={"P":[{"T":"0"},{"T":"4","F":[],"R":[]},{"T":"6","F":[],"R":[]},{"T":"12","F":[],"R":[]},{"T":"Y","F":[],"R":[]},{"T":"A","F":[],"R":[]},{"T":"S","F":[],"R":[]}],"M":false}

## ajax query tickets
```code
POST /Update/Booking3/TravelWish/GotoNextStep?ds=c3953f57-22ad-47ce-b020-b57f4e3061b7&lang=en&channelId=64b729c2-7b18-4dcd-a42e-980cd747c15f HTTP/1.1
Host: www.b-europe.com
Connection: keep-alive
Content-Length: 1054
Pragma: no-cache
Cache-Control: no-cache
Accept: application/json, text/javascript, */*; q=0.01
Origin: https://www.b-europe.com
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36
Content-Type: application/json
Referer: https://www.b-europe.com/Travel/Booking/Tickets?autoactivatestep2=true&origin=FRPAR&dest=DEBEG&traveltype=TwoWay&outbound=10%2F03%2F2016&outboundt=&outboundtp=DepartureTime&inbound=&inboundt=&inboundtp=DepartureTime&comfortclass=2&ticketlanguage=en&travelparty=%257B%2522P%2522%253A%255B%257B%2522T%2522%253A%25220%2522%257D%252C%257B%2522T%2522%253A%25224%2522%257D%252C%257B%2522T%2522%253A%25226%2522%257D%252C%257B%2522T%2522%253A%252212%2522%257D%252C%257B%2522T%2522%253A%2522Y%2522%257D%252C%257B%2522T%2522%253A%2522A%2522%257D%252C%257B%2522T%2522%253A%2522S%2522%257D%255D%252C%2522M%2522%253Afalse%257D
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4
Cookie: websitecrosssite_production#lang=en; SitePreferences_www.b-europe.com={"c":"OT","l":"en","r":"EUR","u":false,"h":"64b729c2-7b18-4dcd-a42e-980cd747c15f"}; referrerInfo_64b729c2-7b18-4dcd-a42e-980cd747c15f=; _ga=GA1.2.30767610.1457526788; _wt.control-984274-ta_24SearchResultsNewDesign=WT3Vtc0l_LZoGy6qzm00yg23GM_-lLv1oLP7QqDDoWDNBfK-hXxREhGWxHK5k88gTFJV6Pf_vzi77zhhSEyoalwDVrmwpVL6uxVavtNxSAtlmjnK7p2eoYrvoXh2_tSnYNEwkqiDq9Ikcn8TDk1shwWnVOPMnSv41zuy-otwm74_2V_WvB6K0bhSR0tiASKMri1Zt6vneqJPVBiU6tkS9X81ZH_0LTdk0lT4zo42DuJnj5Dyd9hXFNoBSxWYaA~; _wt.control-984274-ta_9SearchResultsPageAB=WT3St9qfPab8M4lrLm158zCiW7xkZ6TYCG9DY94IHP2huUEfvmxuJAnc9vMDlK7G0nGObP-dMhxtmdsasGkfKXvGOddFBAQcMdn_mQyJHOy4Vab0ttaJQkZgBlfTStoomyeIqktmet5dMbRuv2QKfqKTDXK-d2DXiqh7wi6eRfQWTSRjdir7W-0-JHVFHfF2AfGlCVIkWWXelMPXDvl52XeyNCwFls_PKQJywEl35xS2TEcMWjXLp_870kYNlw~; _wt.user-984274=WT3xCKtf-2_BwcqjBGky4aFAjxjhzKrlfPop_V4iWDriPprqxMZd0z_6xBF2g4UxNCB8DUqyzjLfgNOsMV6RX-eZs5v0mMEkPtIGcmfZjrEhHLekKDOctBgQLny8BDa-U8axWd0yf0vLsYzJ-eNJBTgGvAdTZqVX0SnMgIYnewH45MY6Yf2XWMKqpar4BN7Ktngc-QOW64XXiEeC5L-O6SGYUN9nRXt0HP5; _wt.control-984274-ta_10SocialProofABn=WT3hfR9DCec7GxnJjRmIZUvUGzmfl5adcnod6_y_xQ3obFekbGjXOtNN0JlzM5itp7bWIrCy1HrIxWGJfu54zW-XLNfgriA8ZBmzJVjag-lzT8i_CvvYFymTGy8pCiGLFQW4pWvtzvirOIfeiK0YImDDLDnoKKttj4hVlJv4PXftlSVJC3R8la0peqX3OVtpbup7YPYmEMDxOuAL0_Uwpzc4abA6cWgQepm_7YpYwo1hwp_riakTZ5mBGFqcOyRpYb-1dQDtZ22e8BiV093; _wt.mode-984274=WT3y5sb-9KDcn8~; _dc_gtm_UA-4476891-6=1

Request Payload:
{
    "SharedCacheDossierId": "3bd57798-d4e1-45f5-ae61-251e0a05da00",
    "TravelWishData": {
        "TravelType": "OneWay",
        "OriginStationName": "Paris (Fr)",
        "DestinationStationName": "München Hbf (De) ( Munich, Munchen, Muenchen )",
        "OriginRCodeRestrictions": null,
        "DestinationRCodeRestrictions": null,
        "DepartureSearchParameters": {
            "Date": "10/03/2016",
            "HourOfDayIn24HourFormat": "7",
            "TimePreference": "DepartureTime",
            "Trainnumber": null,
            "ComfortClass": "2"
        },
        "MaximumNumberOfTransfers": null,
        "ViaStationName": "",
        "TicketLanguage": "en",
        "TravelParty": [{
            "PassengerType": "0",
            "DisplayName": "Child (0-3) 1"
        }, {
            "PassengerType": "4",
            "DisplayName": "Child (4-5) 2"
        }, {
            "PassengerType": "6",
            "DisplayName": "Child (6-11) 3"
        }, {
            "PassengerType": "12",
            "DisplayName": "Youth (12-14) 4"
        }, {
            "PassengerType": "Y",
            "DisplayName": "Youth (15-25) 5"
        }, {
            "PassengerType": "A",
            "DisplayName": "Adult (26-59) 6"
        }, {
            "PassengerType": "S",
            "DisplayName": "Senior (60+) 7"
        }],
        "MoreThanNinePassengersSelected": false,
        "GreenPointsNumber": null,
        "CorporateContracts": {
            "ECP": "",
            "TCP": "",
            "ICP": ""
        }
    },
    "AjaxCallOrigin": "railtour",
    "TimeDelta": 342345
}
```
