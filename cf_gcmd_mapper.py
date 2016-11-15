#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ritesh
# @Date:   2016-02-10 16:25:03
# @Last Modified by:   ritesh
# @Last Modified time: 2016-02-10 16:55:47

from flask import Flask, render_template, request, jsonify, redirect, url_for, Response
import os
import json
from bson import json_util
import time
import operator
from bson.objectid import ObjectId


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

####################################
"""Read cf and gcmd maps """
cf_map = None
gcmd_map = None

input_cf_filename = "./cf_gcmd_map.json"
input_gcmd_filename = "./gcmd_cf_map.json"

with open(input_cf_filename) as cf_gcmd_map_file:
    cf_map = json.load(cf_gcmd_map_file)

with open(input_gcmd_filename) as gcmd_cf_map_file:
    gcmd_map = json.load(gcmd_cf_map_file)



###########################
"""REST API"""
def to_json(data):
    """Convert Mongo object(s) to JSON"""
    # return json.dumps(data, default=json_util.default)
    return json.dumps( data, indent = 4, ensure_ascii = False )

@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

@app.route('/service/<keyword>', methods=['GET'])
def rest_service(keyword):
    """Return a list of all UFO sighting; you know what i mean
    ex) GET /service/<keyword>
    """
    try:
        if request.method == 'GET':
            if keyword == "cf":
                js = to_json(cf_map)
                resp = Response(js, status=200, mimetype='application/json')
                return resp
            elif keyword =="gcmd":
                js = to_json(gcmd_map)
                resp = Response(js, status=200, mimetype='application/json')
                return resp
    except Exception, e:
        print (e)
        return not_found()


@app.route("/service")
def rest_service_key():
    """Return specific UFO sighting which is not possible in this case
    ex) GET /service?cf=123456
    """
    try:
        if request.method == 'GET':
            arg_key = "cf" if "cf" in request.args else "gcmd"
            arg_value = request.args.get(arg_key)
            result = cf_map.get(arg_value) if arg_key == "cf" else gcmd_map.get(arg_value)
            js = to_json(result)
            resp = Response(js, status=200, mimetype='application/json')
            return resp
    except Exception, e:
        print (e)
        return not_found()

# Index page
@app.route('/')
def index():
    result = {
    "..url/service/cf": "for all cf to gcmd map",
    "..url/service/gcmd": "for all gcmd to cf map",
    "..url/service?cf=value": "for each cf to gcmd map",
    "..url/service?gcmd=value": "for each gcmd to cf map",
    }
    js = to_json(result)
    resp = Response(js, status=200, mimetype='application/json')
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug = True)