FROM python:3.8-buster

WORKDIR /opt/musical-bassoon

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . . 

CMD /bin/sh -c ./start.sh

