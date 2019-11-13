#!/bin/bash

docker image rm backend:1.0
docker container stop backendServer
docker container rm  backendServer

docker image build -t backend:1.0 .
docker container run --network=host --name backendServer backend:1.0
