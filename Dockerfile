FROM daocloud.io/library/python:3.5

MAINTAINER starsharp06sharp <zhenglei@std.uestc.edu.cn>
USER root
EXPOSE 80

COPY . /StuInfoSite

WORKDIR /StuInfoSite

RUN apk add uwsgi

RUN pip install -r requirements.txt

RUN /StuInfoSite/gen_serect_key.sh

ENTRYPOINT /StuInfoSite/run_in_docker.sh