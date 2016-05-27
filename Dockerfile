FROM daocloud.io/library/python:3.5-alpine

MAINTAINER starsharp06sharp <zhenglei@std.uestc.edu.cn>
USER root
EXPOSE 80

RUN sh ./gen_serect_key.sh

ENTRYPOINT ["sh", "./run_in_docker.sh"]
