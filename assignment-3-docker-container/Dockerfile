FROM alpine:3.12
ENV VAR=10
ENV MSG="Hello Docker!"
WORKDIR /usr/app
COPY fibonacci.sh ./
COPY helloDocker.sh ./
RUN ["/bin/sh","fibonacci.sh"]
RUN ["/bin/sh","helloDocker.sh"]