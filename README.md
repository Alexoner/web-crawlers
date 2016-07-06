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
```shell
cd /home/admin/work/scrapyd && su admin -c "nohup scrapyd" &
```

### deploy the scrapy project
```shell
scrapyd-deploy
```

### sloth project for scheduler
```shell
curl http://127.0.0.1:6800/schedule.json -d project=scrapyrpj -d spider=dmoz
```
or use sloth to call the task

```python
from sloth_job.tasks.crawler import schedule_job
res = schedule_job.delay('scrapyprj', 'dmoz', url='http://127.0.0.1:6800')
print(res.get())
```

### docker container as the production host

if you have a container running scrapyd on its port 6800, you can run
```shell
wget http://container_ip:6800
```
To get the container´s ip address, run the 2 commands:
```shell
docker ps

docker inspect container_name | grep IPAddress
```
Internally, Docker shells out to call iptables when you run an image, so maybe some variation on this will work.

to expose the container's port 8000 on your localhosts port 8001
```shell
 iptables -t nat -A  DOCKER -p tcp --dport 6800 -j DNAT --to-destination 192.168.42.49:6800
```

### use netrc file to configure username and password

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


