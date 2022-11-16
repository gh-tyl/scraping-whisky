FROM selenium/standalone-chrome:latest
RUN sudo apt-get update && \
    sudo apt-get install -y python3-pip
WORKDIR /src
COPY ./requirements.txt /src
RUN pip3 install -r requirements.txt
COPY ./src /src
