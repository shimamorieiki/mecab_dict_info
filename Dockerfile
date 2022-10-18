FROM python:3-buster

WORKDIR /root

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update --fix-missing &&\
    apt-get install -y --fix-missing apt-utils dialog
RUN apt-get upgrade -y --fix-missing &&\
    apt-get install -y --fix-missing libboost-dev &&\
    apt-get install -y --fix-missing google-perftools &&\
    apt-get install -y --fix-missing libgoogle-perftools-dev &&\
    # python container had already
    apt-get install -y --fix-missing gcc &&\
    apt-get install -y --fix-missing g++ &&\
    apt-get install -y --fix-missing make &&\
    apt-get install -y --fix-missing wget &&\
    # to decompress *.tar.bz2
    apt-get install -y --fix-missing bzip2

# to use Japanese
RUN apt-get install -y -f locales
RUN locale-gen ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LC_CTYPE ja_JP.UTF-8
RUN localedef -f UTF-8 -i ja_JP ja_JP.utf8

# clean up all temporary files 
RUN apt-get clean &&\
    apt-get autoclean -y &&\
    apt-get autoremove -y &&\
    apt-get clean &&\
    rm -rf /tmp/* /var/tmp/* &&\
    rm -rf /var/lib/apt/lists/* &&\    
    rm -f /etc/ssh/ssh_host_*

# ユーザーを作成
ARG UID=1000
RUN useradd -m -u ${UID} docker

# フォルダを作る
RUN mkdir -p /code
RUN chown docker /code

# 作成したユーザーに切り替える
USER ${UID}

WORKDIR /code
ADD requirements.txt /code/

USER root

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Mecab
RUN apt-get update && apt-get upgrade -y &&\
    apt-get install -y apt-utils &&\
    apt-get install -y mecab &&\
    apt-get install -y libmecab-dev && \
    apt-get install -y mecab-ipadic-utf8 && \
    apt-get install -y git && \
    apt-get install -y curl && \
    apt-get install -y xz-utils && \
    apt-get install -y file && \
    apt-get install -y sudo

# # neologd辞書
# RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git && \
#     cd mecab-ipadic-neologd && \
#     ./bin/install-mecab-ipadic-neologd -n -y && \
#     echo dicdir = `mecab-config --dicdir`"/mecab-ipadic-neologd">/etc/mecabrc && \
#     sudo cp /etc/mecabrc /usr/local/etc && \
#     cd ..

# 作成したユーザーに切り替える
USER ${UID}
ADD . /code/

USER root
RUN chown -hR docker:docker /code

USER ${UID}
CMD /bin/bash