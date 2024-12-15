# https://www.builtydata.com/
# author: Harut Grigoryan

# The definition of the docker image
# to run the Builty crawling and parsing framework

FROM --platform=linux/amd64 amazonlinux:2023.3.20240108.0

ENV PATH=$PATH:/root/.local/bin/
ENV PYTHONPATH=$PYTHONPATH:/usr/src

RUN yum -y update && yum -y install \
  gcc glibc-devel make which \
  python3 python3-devel

RUN curl -O https://bootstrap.pypa.io/get-pip.py && python3 get-pip.py --user

COPY requirements.txt /
RUN pip3 install --no-cache-dir -r /requirements.txt

COPY main.py /usr/src

WORKDIR "/usr/src/"
CMD [ "python3", "main.py"]
