#!/usr/bin/env bash

cd /home/cbaxter/build/connector

docker build -f build.Dockerfile -t cbaxter1988/connector .

docker-compose up -d

rm -rf /home/cbaxter/build/connector