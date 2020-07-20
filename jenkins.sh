#!/usr/bin/env bash
cd  ~/.temp/connector

echo "Building Image"
docker build -f build.Dockerfile -t cbaxter1988/connector .

echo "Running Image"
docker-compose up -d

cd
echo "Cleaning"
rm -rf .temp/

