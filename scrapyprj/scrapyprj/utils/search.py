# -*- coding: utf-8 -*-
import json
import os
def writeToSearch(file_name,indexName,typeName):
    lines = open(file_name).readlines()
    for line in lines:
        comStr = "curl -XPUT 'http://localhost:9200/"+indexName+"/"+typeName+"/"
        id = line.split("###")[0]
        comStr += id +"' -d'"
        comStr += line.split("###")[1]+"'"
        print comStr
        result = os.system(comStr)
        print result
if __name__ == "__main__":
    writeToSearch('/Users/xueliang.xl/work/getter/house.json','areastaticentity','areainfo')
