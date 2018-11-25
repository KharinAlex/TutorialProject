FROM ubuntu:18.04

ENV PYTHONUNBUFFERED 1
RUN apt-get update

RUN apt-get -y install \
  python3.6 \
  python3-pip

RUN mkdir -p /TutorialProject

WORKDIR /TutorialProject

COPY TutorialProject/requirements.txt /TutorialProject

RUN pip3 install --no-cache-dir -r /TutorialProject/requirements.txt --ignore-installed