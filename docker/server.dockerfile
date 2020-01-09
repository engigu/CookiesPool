FROM python:3.7-alpine

ADD ./  /code
ADD ./docker/localtime /etc/localtime

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories \
	&& pip install -r /code/requirements.txt  -i https://mirrors.aliyun.com/pypi/simple/ 

WORKDIR /code
EXPOSE  9632
CMD ["python", "app.py"]
