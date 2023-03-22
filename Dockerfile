FROM ubuntu:20.04

ENV TZ=Asia/Shanghai
ENV LANG=en_US.utf8
ENV APPNAME=lm-filter

ARG DEBIAN_FRONTEND=noninteractive
RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list && \
    sed -i s@/security.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list && \
    apt-get update -y && \
    apt-get install -y make vim cmake autoconf automake curl wget unzip bzip2 ssh build-essential && \
    apt-get install -y libssl-dev openssh-client python3-pip && \
    apt-get clean

ARG workdir=/home/admin/$APPNAME
RUN mkdir -p $workdir && \
    mkdir -p $workdir/logs
ADD . $workdir
WORKDIR $workdir

RUN pip install --upgrade pip && \
    pip install -r requirements.txt -i https://mirrors.cloud.tencent.com/pypi/simple/


#RUN python3 $workdir/itn_client/test.py || exit 1
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python


# Port for itn grpc service
#EXPOSE 30000

#CMD ["/bin/bash", "-c", "/home/admin/asr-itn/run.sh"]

