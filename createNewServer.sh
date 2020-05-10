#!/usr/bin/env bash
mkdir github
cd github
git clone https://github.com/youtrip/webapi.git
sudo apt update
sudo apt upgrade
sudo apt install -y python3-dev python3-pip python-gevent python3-venv nethogs nginx
cd webapi
python3 -m venv venv
pip install -r requirements.txt
gunicorn -D -c gunicorn.py api:app
# 获取Gunicorn进程树
# pstree -ap|grep gunicorn

# 重启Gunicorn任务,例如进程号是30080
# kill -HUP 30080

# http://XXX:8800/post?ll=54.51492117546928,-5.889513013116261