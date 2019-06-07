FROM cbaxter1988/flask_app

RUN pip install netmiko
RUN pip install pysnmp
RUN pip install Flask-Cors
RUN pip install protobuf