## europerail

Input and output are configured in "\$HOME/work/".
You need to provide pairs.txt file as input seeds.Each line of the file is in the format
'city1 city2'.

To run it,
```shell
./run.sh
```


## TODO

- [ ] keyword extraction from articles
    - [ ] TF-IDF
    - [ ] textrank
- [ ] visualization

##About ELK config

在web-crawlers/scrapyprj/scrapyprj目录下有两个.conf文件
	
	proxy.conf
	该配置文件是代理任务（爬取代理）的Logstash的配置文件，输出到redis

	house.conf
	该配置文件是房产数据的Logstash配置文件，输出到Elasticsearch
**注意：**后面会统一这个配置，所有任务用一个配置，分开配置方便测试
	

