#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/5/10 17:57
# @Author : Felix Zhou
# @File : siteok.py
# @Software: PyCharm

import requests

siteid = ['34.92.126.153',
          '34.72.40.73',
          '35.194.228.183',
          '13.229.135.242',
          ]
for i in siteid:
    site = 'http://%s:8800/post?ll=54.51492117546928,-5.889513013116261' % i
    obj = requests.get(site).content.decode('utf-8')
    if obj.find('500 Internal Server Error') >=0:
        print(i,':error')
    else:
        print(i,':ok!')