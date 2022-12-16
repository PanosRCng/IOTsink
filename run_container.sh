#!/bin/bash

docker run --rm \
 -p 1095:8080 \
 -e GUNICORN_CONF="gunicorn_conf.py" \
 -v `pwd`/envs:/usr/src/app/envs/:ro \
 -v `pwd`/logs:/usr/src/app/logs/:rw \
 --user $(id -u ${USER}):$(id -g ${USER}) \
--name iotsink iotsink:latest