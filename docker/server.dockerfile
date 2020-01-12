FROM python:3.7-alpine

ADD ./  /code

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories \
	&& pip install -r /code/requirements.txt  -i https://mirrors.aliyun.com/pypi/simple/  \
	&& cp /code/docker/localtime /etc/localtime

WORKDIR /code
EXPOSE  9632
CMD ["python", "app.py"]
