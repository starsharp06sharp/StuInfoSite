FROM daocloud.io/library/python:3.5

MAINTAINER starsharp06sharp <zhenglei@std.uestc.edu.cn>

COPY . /StuInfoSite

WORKDIR /StuInfoSite

RUN pip install -r requirements.txt

RUN /StuInfoSite/production_config.sh

VOLUME ["/StuInfoSite"]

ENTRYPOINT ["uwsgi", "uwsgi.ini"]
