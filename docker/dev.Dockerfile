FROM cbaxter1988/connector:base

COPY . /app

CMD python /app/run.py