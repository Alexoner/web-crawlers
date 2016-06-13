FROM ubuntu:latest
MAINTAINER onerhao@gmail.com

# TODO: change the apt-get mirror in /etc/apt/sources.list and pip mirror in ~/.pip/pip.conf
# otherwise it would be way too slow in China mainland

# change apt-get software respository's mirror url
# heredoc cat << EOF is not supported
RUN cp /etc/apt/sources.list /etc/apt/sources.list.bak && echo "deb http://mirrors.aliyun.com/ubuntu/ xenial main restricted universe multiverse\ndeb http://mirrors.aliyun.com/ubuntu/ xenial-security main restricted universe multiverse\ndeb http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted universe multiverse\ndeb http://mirrors.aliyun.com/ubuntu/ xenial-proposed main restricted universe multiverse\ndeb http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse\ndeb-src http://mirrors.aliyun.com/ubuntu/ xenial main restricted universe multiverse\ndeb-src http://mirrors.aliyun.com/ubuntu/ xenial-security main restricted universe multiverse\ndeb-src http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted universe multiverse\ndeb-src http://mirrors.aliyun.com/ubuntu/ xenial-proposed main restricted universe multiverse\ndeb-src http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse" > /etc/apt/sources.list

# change pip' mirror url
RUN mkdir ~/.pip && echo "[global]\n#index-urls:  https://pypi.douban.com, https://mirrors.aliyun.com/pypi,\ncheckout https://www.pypi-mirrors.org/ for more available mirror servers\nindex-url = https://pypi.douban.com/simple\ntrusted-host = pypi.douban.com" > ~/.pip/pip.conf

# install basic requirements
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        git \
        curl \
        python-dev \
        python-numpy \
        python-pip \
        python-scipy \
        python3-dev \
        python3-pip \
        software-properties-common

# install caffe
RUN apt-get install -y --no-install-recommends \
        libatlas-base-dev \
        libboost-all-dev \
        libboost-mpi-dev \
        libgflags-dev \
        libgoogle-glog-dev \
        libhdf5-serial-dev \
        libleveldb-dev \
        liblmdb-dev \
        libopencv-dev \
        libprotobuf-dev \
        libsnappy-dev \
        protobuf-compiler


# install tensorflow
ENV TF_BINARY_URL=https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow-0.9.0rc0-cp27-none-linux_x86_64.whl
RUN pip install --upgrade $TF_BINARY_URL


# install neovim
RUN add-apt-repository ppa:neovim-ppa/unstable -y && apt-get update && apt-get install neovim && \
    update-alternatives --install /usr/bin/vi vi /usr/bin/nvim 60 && \
    update-alternatives --install /usr/bin/vi vi /usr/bin/nvim 60 && \
    update-alternatives --install /usr/bin/vim vim /usr/bin/nvim 60 && \
    update-alternatives --config vim && \
    update-alternatives --install /usr/bin/editor editor /usr/bin/nvim 60 && \
    update-alternatives --config editor

RUN rm -rf /var/lib/apt/lists/*
WORKDIR /workspace

#modify by xueliang . update then install,otherwise will report can not find source error
RUN apt-get update

#install dependency lib for scrapy
RUN apt-get install -y \
    python3 \
    python-dev \
    python3-dev \
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt-dev

# install scrapy
RUN pip install scrapy scrapyd


#add wget and curl ,after try add ELK ,I think we should install the ELK outside Docker,
#that is more easy, and the docker env is more clean(no java related software),  just share the #output folder of scrapy to host machine, so the logstash can access the shared folder and ship
#data to elasticsearch and reids
#the dockerfile for elasticsearch is here https://github.com/docker-library/elasticsearch/blob/30af4a027561ede1295621039ebc4ae6c656ea2a/2.3/Dockerfile
# and the doc is https://hub.docker.com/_/elasticsearch/

RUN apt-get install wget
RUN apt-get install curl




