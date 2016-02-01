FROM andrewosh/binder-base
MAINTAINER Massimo Santini <massimo.santini@gmail.com>
RUN apt-get -y update && apt-get install -y graphviz
