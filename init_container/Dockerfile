FROM ubuntu

ENV URL=http://192.168.100.10:31447
ENV USER=admin
ENV PASSWORD=changeme
ENV BUCKET_NAME=jmx
ENV TASK_NAME=example


WORKDIR /boxter
COPY boxter.sh /boxter/

RUN apt-get update
RUN apt-get install -y wget jq
RUN wget https://dl.min.io/client/mc/release/linux-amd64/mc
RUN chmod +x mc
RUN ./mc --help


CMD ["./boxter.sh" ]


