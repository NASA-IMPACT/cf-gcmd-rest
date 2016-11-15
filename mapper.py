#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ritesh
# @Date:   2015-11-25 10:53:58
# @Last Modified by:   ritesh
# @Last Modified time: 2016-03-02 15:33:46

from flask import Flask, render_template, request, jsonify, redirect, url_for, Response
from werkzeug import secure_filename
import os
import json
from bson import json_util
import time
import operator
from bson.objectid import ObjectId

# from lib import libmongo
# db = libmongo.get_db()

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

def get_result(result):
    result["id"] = str(result["_id"])
    del result["_id"]
    return result

@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

@app.route('/service/<db_table_name>', methods=['GET'])
def rest_service(db_table_name):
    """Return a list of all UFO sighting; you know what i mean
    ex) GET /service/<db_table_name>
    """
    print request.args.get('aa')

    print request.url
    print request.query_string
    print db_table_name
    # print url_for(db_table_name)
    try:
        if request.method == 'GET':
            results = db[db_table_name].find()
            json_results = []
            for result in results:
                json_results.append(get_result(result))

            js = to_json(json_results)
            resp = Response(js, status=200, mimetype='application/json')
            return resp
    except Exception, e:
        print (e)
        return not_found()


@app.route('/service/<db_table_name>/<id>', methods=['GET'])
def rest_service_id(db_table_name, id):
    """Return specific UFO sighting which is not possible in this case
    ex) GET /service/cf/123456
    """
    print request.url
    print request.query_string
    try:
        if request.method == 'GET':
            print "ID: ", id
            result = db[db_table_name].find_one({'_id': ObjectId(id)})
            js = to_json(get_result(result))
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
    print request.url
    print request.query_string

    print request.args.get('gcmd')
    print 'gcmd' in request.args
    try:
        if request.method == 'GET':
            db_table_name = 'gcmd' if "gcmd" in request.args else "cf"
            key = request.args.get(db_table_name)
            result = db[db_table_name].find_one({'_id': ObjectId(id)})
            js = to_json(get_result(result))
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
    "..url/service/cf/id": "for each cf to gcmd map",
    "..url/service/gcmd/id": "for each gcmd to cf map",
    }
    js = to_json(result)
    resp = Response(js, status=200, mimetype='application/json')
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug = True)