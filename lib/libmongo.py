#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ritesh
# @Date:   2015-12-22 12:06:24
# @Last Modified by:   ritesh
# @Last Modified time: 2016-02-10 10:51:50

""" Mongodb
    Database    :       cf_gcmd
    Collections :
            cf    :   cf_to_gcmd_list
            gcmd   :   gcmd_to_cf_list
"""

from pymongo import MongoClient

def get_db():
    client = MongoClient('localhost', 27017)
    db = client.cf_gcmd      # mapper collection
    return db


def insert_into_cf(db):
    db.cf.insert_one(k2)


def insert_test_variables(db):
    db.gcmd.insert_one(airs)

def insert_test_maps(db):
    pass

def main():
    db = get_db()

    insert_test_keywords(db)
    # insert_test_variables(db)
    # insert_test_maps(db)

if __name__ == '__main__':
    main()

# db.keywords.insert_one(name_keywords_dict)