#!/bin/sh

DIRNAME=$(dirname "$0")

cp /dev/null "${DIRNAME}/cityCode.log"

while IFS= read -r cityName; do
    printf "%s\n" "$cityName"
    curl 'https://www.b-europe.com/Update/Search/StationSearch?ds=f29afce8-7586-4803-8dec-8eb9377bfef6&lang=en&channelId=64b729c2-7b18-4dcd-a42e-980cd747c15f' -H 'Pragma: no-cache' -H 'Origin: https://www.b-europe.com' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en-US,en;q=0.8,zh-CN;q=0.6,zh-TW;q=0.4' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36' -H 'Content-Type: application/json' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Cache-Control: no-cache' -H 'X-Requested-With: XMLHttpRequest' -H 'Cookie: websitecrosssite_production#lang=en; SitePreferences_www.b-europe.com={"c":"OT","l":"en","r":"EUR","u":false,"h":"64b729c2-7b18-4dcd-a42e-980cd747c15f"}; referrerInfo_64b729c2-7b18-4dcd-a42e-980cd747c15f=; _ga=GA1.2.30767610.1457526788; _dc_gtm_UA-4476891-6=1; _wt.mode-984274=WT3y5sb-9KDcn8~; _wt.user-984274=WT35cpysxR96HIwBMSM7JqL9RjcVrXAYX2Wn-o2ZlzMm3Nx4yoVR6VpxoH2hH43arkqT4CWcYKwKZaobsip7U4ulUsnwwLyNcm9djjL0shB4lY~' -H 'Connection: keep-alive' -H 'Referer: https://www.b-europe.com/Travel' --data-binary "{\"Criteria\":\"${cityName}\",\"OriginOrDestination\":\"Origin\",\"RCodeRestrictions\":null,\"GetGuidance\":true,\"AjaxCallOrigin\":\"railtour\"}" --compressed >> cityCode.log
    printf "\n" >> cityCode.log
done < "${DIRNAME}/cities.list"

python3 processLog.py > a.java
