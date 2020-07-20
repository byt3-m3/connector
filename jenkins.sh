#!/usr/bin/env bash
cd .temp/connector

docker build -f build.Dockerfile -t cbaxter1988/connector .

docker-compose up -d

cd

rm -rf .temp/

