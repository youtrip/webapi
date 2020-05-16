#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/5/7 16:07
# @Author : Felix Zhou
# @File : api.py.py
# @Software: PyCharm

from flask import Flask, jsonify, request, make_response, current_app
import datetime
from functools import wraps
import jwt
import requests
import json
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


app = Flask(__name__)
app.config['API_SECRET_KEY'] = 'dnottellanybody!'

hostname = 'api.reality.co'

headers = {
            'Host': hostname,
            'User-Agent': 'Landlord 2/2.20.2 (com.landlordTycoonEdition.www; build:207; iOS 12.4.5) Alamofire/4.9.1',
            'x-fs-token': 'AYUPT0GZOXDCTPPAGGTRYWALLU4XFVV1DBJZSNVDEIAIVLQI',
            'api-version': '2',
            'Accept': '*/*',
            'Accept-Language': 'zh-CN',
            'Accept-Encoding': 'gzip;q=1.0, compress;q=0.5',
            'Connection': 'close'
        }

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # http://127.0.0.1/route?token=asdasfdsffgdsfgdffgdfsdf
        token = request.args.get('token')
        print(token)

        if not token:
            return jsonify({'messages': 'token is missing!'}), 403

        try:
            data = jwt.decode(token, current_app.config['API_SECRET_KEY'])
        except Exception as err:
            return jsonify({'messages': 'token is missing or invalid. error:%s' % err}), 403
        return f(*args, **kwargs)

    return decorated


def getApi(urlString, postData=None):
    requests.adapters.DEFAULT_RETRIES = 6  # 增加重连次数
    result = requests.session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    # adapter = HTTPAdapter(max_retries=3)
    result.mount('https://', adapter)
    result.keep_alive = False

    # 设置网络请求超时时间,连接时间最长10秒，返回数据最长200秒
    setTimeout = (10, 200)

    if postData is not None:
        headers['Content-Type'] = 'application/json'
        headers['Content-Length'] = str(len(postData))

        result = result.post(urlString, postData, headers=headers, timeout=setTimeout).content
    else:
        result = result.get(urlString, headers=headers, timeout=setTimeout).content
    return result


@app.route('/post', methods=['GET'])
def post():
    latlon = request.args.get('ll').split(',')

    url = 'https://%s/landlord/assets/nearby' % hostname
    # -5.889513013116261,54.51492117546928
    postData = {
        "location": {
            "lon": latlon[1],
            "lat": latlon[0]
        }
    }
    postDatastr = json.dumps(postData)
    headers['Content-Type'] = 'application/json'
    headers['Content-Length'] = str(len(postDatastr))
    return getApi(url, postDatastr)

@app.route('/get', methods=['GET'])
def get():
    url = 'https://%s/landlord/marketplace' % hostname
    return getApi(url)


@app.route('/login', methods=['GET'])
def login():
    auth = request.authorization
    if auth and auth.password == 'password':
        token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                           current_app.config['API_SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})
    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="login Required"'})

if __name__== '__main__':
    app.run(debug=True,port=8800,host='0.0.0.0')