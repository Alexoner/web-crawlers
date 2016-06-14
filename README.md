# web crawling project based on scrapy

## scripts
- 963110
- weather.com.cn
- scrapyprj is a scrapy project containing a collection of scripts:
    - europerail

## europerail

Input and output are configured in "\$HOME/work/".
You need to provide pairs.txt file as input seeds.Each line of the file is in the format
'city1 city2'.

To run it,
```shell
./run.sh
```

## deploy
### frontera for distributed crawling

### scrapyd as crawling daemon

### sloth project for scheduler

### docker container as the production host

### use netrc file to configure username and password

## distributed deploying with frontera

```shell
# start the message broker
python -m frontera.contrib.messagebus.zeromq.broker > zeromq.log 2>&1 &
# start the db worker
python -m frontera.worker.db --config frontier.workersettings > db.log 2>&1 &
# start the strategy worker
# ...
# run spider workers parallely
# run spider worker that loads seeds
scrapy crawl general -L INFO -s FRONTERA_SETTINGS=scrapyprj.frontera.spider0 -s SEEDS_SOURCE=seeds.txt
# run spider worker that only crawls
scrapy crawl general -L INFO -s FRONTERA_SETTINGS=scrapyprj.frontera.spider1
scrapy crawl general -L INFO -s FRONTERA_SETTINGS=scrapyprj.frontera.spider2
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


##About Dockerfile
在尝试Docker安装后，决定将Python开发环境和Java相关环境隔离(ELK使用的是JDK)，Docker中安装python相关环境，主要是爬虫，其余的环境安装在宿主机上，爬取数据在docker中和宿主机共享目录
这个Dockerfile没有安装caffe和torch
