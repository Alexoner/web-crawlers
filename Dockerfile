FROM ubuntu:latest
MAINTAINER onerhao@gmail.com

# TODO: change the apt-get mirror in /etc/apt/sources.list and pip mirror in ~/.pip/pip.conf
# otherwise it would be way too slow in China mainland

# change apt-get software respository's mirror url
# heredoc cat << EOF is not supported
RUN cp /etc/apt/sources.list /etc/apt/sources.list.bak && echo "deb http://mirrors.aliyun.com/ubuntu/ xenial main restricted universe multiverse\ndeb http://mirrors.aliyun.com/ubuntu/ xenial-security main restricted universe multiverse\ndeb http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted universe multiverse\ndeb http://mirrors.aliyun.com/ubuntu/ xenial-proposed main restricted universe multiverse\ndeb http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse\ndeb-src http://mirrors.aliyun.com/ubuntu/ xenial main restricted universe multiverse\ndeb-src http://mirrors.aliyun.com/ubuntu/ xenial-security main restricted universe multiverse\ndeb-src http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted universe multiverse\ndeb-src http://mirrors.aliyun.com/ubuntu/ xenial-proposed main restricted universe multiverse\ndeb-src http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse" > /etc/apt/sources.list

# change pip' mirror url
RUN mkdir ~/.pip && echo "[global]\n#index-urls:  https://pypi.douban.com, https://mirrors.aliyun.com/pypi,\ncheckout https://www.pypi-mirrors.org/ for more available mirror servers\nindex-url = https://pypi.douban.com/simple\ntrusted-host = pypi.douban.com" > ~/.pip/pip.conf

#modify by xueliang . update then install,otherwise will report can not find source error
RUN apt-get update
# install basic requirements
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        git \
        wget \
        curl \
        python-pip \
        python3-pip \
        python3 \
        python-dev \
        python3-dev \
        libssl-dev \
        libffi-dev \
        libxml2-dev \
        libxslt-dev
RUN rm -rf /var/lib/apt/lists/*

# install scrapyprj
RUN mkdir ~/src/
RUN git clone https://github.com/Alexoner/web-crawlers.git ~/src/scrapyprj && \
    cd ~/src/scrapyprj && pip install -r requirements.txt

WORKDIR ~/src/scrapyprj


#I think we should install the ELK outside Docker,
#that is more easy, and the docker env is more clean(no java related software),  just share the #output folder of scrapy to host machine, so the logstash can access the shared folder and ship
#data to elasticsearch and reids
#the dockerfile for elasticsearch is here https://github.com/docker-library/elasticsearch/blob/30af4a027561ede1295621039ebc4ae6c656ea2a/2.3/Dockerfile
# and the doc is https://hub.docker.com/_/elasticsearch/
