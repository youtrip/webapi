#!/usr/bin/env bash
mkdir github
cd github
get clone https://github.com/youtrip/webapi.git
sudo apt update
sudo apt upgrade
sudo apt install python3-dev python3-pip python-gevent python3-venv nethogs
cd webapi
python3 -m venv venv