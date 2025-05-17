FROM bitnami/python:3.13.3-debian-12-r13

ARG NEW_LX_USER_GRP_GID='1010'
ARG NEW_LX_USER_GRP_NAME='tolteques'
ARG NEW_LX_USER_NAME='tolt'
ARG NEW_LX_USER_UID='1000'

RUN apt-get update -y

RUN mkdir -p /tolt
WORKDIR /tolt
COPY create.lx.user.sh .
RUN chmox a+x ./create.lx.user.sh && ./create.lx.user.sh
COPY install.miniconda.sh .
RUN chmox a+x ./install.miniconda.sh

RUN chown $NEW_LX_USER_NAME:$NEW_LX_USER_NAME -R /tolt

USER $NEW_LX_USER_NAME
RUN ./install.miniconda.sh

RUN . ~/.bashrc && conda --version
RUN . ~/.bashrc && conda create -n myenv llm && conda activate llm

RUN python --version 
RUN pip -V
