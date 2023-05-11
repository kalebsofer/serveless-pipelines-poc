# IMAGE
FROM ubuntu:jammy

ENV DEBIAN_FRONTEND=noninteractive

# GENERAL TOOLS
RUN apt-get update -y && \
    apt-get install apt-utils -y && \
    apt-get install git curl build-essential -y && \
    apt install software-properties-common -y && \
    apt-get install time -y && \
    apt-get install vim -y && \
    apt-get install -y tzdata

# # SQLITE - Not used but will keep for now
# RUN apt-get update -y && \
#     apt-get install sqlite3
    
# PYTHON 3.10
RUN add-apt-repository ppa:deadsnakes/ppa -y && \
    apt-get update -y && \
    apt-get install python3.10 python3-pip python3.10-distutils -y && \
    python3.10 -m pip install pipenv 

# Root dir for running things inside the container
RUN mkdir /local_explorer

# PIPENV & Prefect
WORKDIR /local_explorer
RUN python3.10 -m pipenv install && \
    export PATH="~/.local/bin:$PATH"

# install prefect
RUN python3.10 -m pipenv install prefect
RUN python3.10 -m pipenv install prefect-dask

# add local_explorer root to python path
ENV PYTHONPATH="/local_explorer"
