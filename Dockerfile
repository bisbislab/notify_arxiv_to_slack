FROM python:3.11.3

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Tokyo
ENV SHELL=/bin/bash

RUN apt-get update && \
    apt-get install -y \
    cron

COPY ./requirements.txt /tmp/
RUN python3 -m pip install -U pip && \
    python3 -m pip --disable-pip-version-check --no-cache-dir install -r /tmp/requirements.txt

ADD crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab

CMD ["cron", "-f"]
