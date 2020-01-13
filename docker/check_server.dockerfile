FROM python:3.7-alpine

ADD ./requirements.txt  /code/requirements.txt

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories \
	&& pip install -r /code/requirements.txt  -i https://mirrors.aliyun.com/pypi/simple/  

ADD ./  /code
ADD ./docker/localtime /etc/localtime

WORKDIR /code
CMD ["python", "cookies_pool.py"]
