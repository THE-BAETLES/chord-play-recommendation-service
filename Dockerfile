FROM python:latest
LABEL maintainer "chobe1<chobe0719@gmail.com>"
LABEL serverType="Recommendation Worker Server"

COPY . /recommendationServer
WORKDIR /recommendationServer

ENV SERVER_PORT 3000

RUN pip install -r requirements.txt
EXPOSE 3000

ENTRYPOINT ["python", "server.py"]