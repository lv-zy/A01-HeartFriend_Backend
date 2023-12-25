FROM python:3.8

WORKDIR /HeartFriend

COPY . /HeartFriend 

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

