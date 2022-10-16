FROM ubuntu:20.04

ENV PYTHON_VERSION="3.7.5"
ENV APP_VERSION="0.1.0"

RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
	&& localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8

RUN apt-get update -y \
 && apt-get install -y \
 curl \
 wget \
 tar \
 xz-utils
RUN apt-get install build-essential -y
RUN apt-get install zlib1g-dev -y

RUN wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tar.xz
RUN tar -xvf Python-${PYTHON_VERSION}.tar.xz
RUN cd Python-${PYTHON_VERSION} && ./configure --enable-optimizations && make altinstall

RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip setuptools wheel

RUN pip3 install poetry

RUN mkdir -p /opt/app
WORKDIR /opt/app
COPY . .

RUN pip3 install dist/command_lib-${APP_VERSION}.tar.gz

RUN adduser --system --uid 10000 --group --shell /sbin/nologin --home /opt/app app
RUN adduser --system --uid 10001 --group --shell /sbin/nologin --home /opt/app app
RUN chown -R 10000:10001 /opt/app
USER 10000:10001

