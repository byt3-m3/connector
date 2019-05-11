FROM cbaxter1988/connector

COPY . /app
RUN pip install netmiko
RUN pip install pysnmp

CMD python /app/run.py