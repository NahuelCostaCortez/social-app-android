#!/bin/sh
#Lanzamos al cliente
docker run -it --network pruebas -v $(pwd):/app python:3.7 python /app/udp_cliente6_broadcast.py 172.18.0.0