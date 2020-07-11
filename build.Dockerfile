# ---- Dependencies ----
FROM python:3.7-slim AS core

# Creates and Make sure we use the virtualenv:
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# ---- Compiles Python Distro ----
COPY connector /connector
COPY requirements.txt /
COPY setup.py /
COPY *.in /
COPY *.md /

RUN pip install -r requirements.txt
RUN python3 setup.py sdist

# ---- Copy Files/Build ----
FROM python:3.7-slim AS build

COPY --from=core /dist /dist
COPY --from=core /opt/venv /opt/venv

# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

RUN cd dist && ls | grep tar.gz | xargs pip3 install

ENTRYPOINT  ["python3", "-m","connector"]

CMD ["--run"]



