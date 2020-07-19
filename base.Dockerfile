FROM cbaxter1988/ubuntu:easysnmp

COPY requirements.txt /

RUN pip3 install -r /requirements.txt