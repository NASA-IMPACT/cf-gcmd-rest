#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ritesh
# @Date:   2016-01-21 14:24:16
# @Last Modified by:   ritesh
# @Last Modified time: 2016-02-09 15:00:38


""" Mongodb
    Database    :       cf_gcmd
    Collections :
            cf    :   cf_to_gcmd_list
            gcmd   :   gcmd_to_cf_list
"""
import json
import libmongo

db = libmongo.get_db()
input_cf_filename = "../cf_gcmd_map.json"
input_gcmd_filename = "../gcmd_cf_map.json"

def sanitize(name):
    return name.replace("/", "_").replace(".", "_")

def insert_cf(doc):
    db.cf.insert(doc)

def insert_gcmd(doc):
    db.gcmd.insert(doc)

def insert(map, cf_flag):
    if cf_flag:
        # insert each doc to cf collection
        for k in map.keys():
            doc = {k: map[k]}
            insert_cf(doc)
    else:
        # insert each doc to cf collection
        for k in map.keys():
            doc = {k: map[k]}
            insert_gcmd(doc)

    print "Insert completed"

def main():
    with open(input_cf_filename) as cf_gcmd_map_file:
        cf_gcmd_map = json.load(cf_gcmd_map_file)
        insert(cf_gcmd_map, cf_flag=True)
    print "cf doc insert completed."

    with open(input_gcmd_filename) as gcmd_cf_map_file:
        gcmd_cf_map = json.load(gcmd_cf_map_file)
        insert(gcmd_cf_map, cf_flag=False)
    print "gcmd doc insert completed."

if __name__ == '__main__':
    main()