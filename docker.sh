#!/bin/bash
# exec docker for the backend

sudo docker build -t edgar/xkcd-server .

sudo docker run -p 5000:5000 edgar/xkcd-server:latest
