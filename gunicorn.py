#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/5/7 20:03
# @Author : Felix Zhou
# @File : gunicorn.py.py
# @Software: PyCharm

import os
import gevent.monkey
gevent.monkey.patch_all()

import multiprocessing

debug = True
loglevel = 'debug'
bind = '0.0.0.0:8800'
pidfile = 'log/gunicorn.pid'
logfile = 'log/debug.log'
accesslog = 'log/gun_access.log'
access_log_format = '%(h)s %(t)s %(U)s %(q)s'
errorlog = 'log/gun_error.log'
timeout = 60*60*6

daemon = True
#启动的进程数
workers = multiprocessing.cpu_count() * 2 + 1
# worker_class = 'gunicorn.workers.ggevent.GeventWorker'
worker_class = "gevent"

x_forwarded_for_header = 'X-FORWARDED-FOR'