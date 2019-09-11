FROM ubuntu:18.10

RUN apt-get update && \
    apt-get install -y python3 python3-dev python3-pip nginx

COPY ./ ./app
WORKDIR ./app

RUN mkdir -p /app/var/log

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3" ]

CMD [ "index.py" ]
