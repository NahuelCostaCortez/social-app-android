#!/bin/sh
#Lanzamos a todos los servidores
docker run -d --network pruebas -v $(pwd):/app python:3.7 python /app/udp_servidor6_broadcast.py
docker run -d --network pruebas -v $(pwd):/app python:3.7 python /app/udp_servidor6_broadcast.py
docker run -d --network pruebas -v $(pwd):/app python:3.7 python /app/udp_servidor6_broadcast.py