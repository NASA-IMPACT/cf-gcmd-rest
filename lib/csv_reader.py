#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ritesh
# @Date:   2016-02-08 15:59:15
# @Last Modified by:   ritesh
# @Last Modified time: 2016-02-09 14:55:47

import csv
import json

input_filename = "../keywordsCfToGcmd.csv"
output_cf_filename = "../cf_gcmd_map.json"
output_gcmd_filename = "../gcmd_cf_map.json"

def get_gcmd_cf_map(cf_gcmd_map):
	gcmd_cf_map = dict()
	for cf, gcmd_list in cf_gcmd_map.iteritems():
		for gcmd in gcmd_list:
			if gcmd not in gcmd_cf_map.keys():
				gcmd_cf_map[gcmd] = [cf]
			else:
				gcmd_cf_map[gcmd].append(cf)

	print "gcmd_cf_map Creation completed."
	return gcmd_cf_map


def get_cf_gcmd_map():
	cf_gcmd = dict()
	""" Read here """
	with open(input_filename, 'rb') as csvfile:
		cf_gcmd_reader = csv.reader(csvfile)
		header = cf_gcmd_reader.next()
		print header

		gcmd_cf = dict()
		gcmd_list = list()
		new_start = True
		cf_name = None
		for row in cf_gcmd_reader:
			if len(row) == 0:
				print "Space"
				if cf_name:
					cf_gcmd[cf_name] = gcmd_list
					# print "cfgcmd: ", cf_gcmd
				gcmd_list = list()
				new_start = True
			else:
				print row[0]
				if new_start:
					cf_name = row[0]
					print  "c_name: ", cf_name
					new_start = False
				else:
					gcmd_list.append(row[0])
	return cf_gcmd

def main():
	cf_gcmd_map = get_cf_gcmd_map()
	print "Reading Completed."

	""" Write to cf file here """
	with open(output_cf_filename, "wb") as cffile:
		json.dump(cf_gcmd_map, cffile, indent=4)
	print "Writing cf Completed"


	gcmd_cf_map = get_gcmd_cf_map(cf_gcmd_map)
	""" Write to gcmd file here """
	with open(output_gcmd_filename, "wb") as gcmdfile:
		json.dump(gcmd_cf_map, gcmdfile, indent=4)
	print "Writing gcmd Completed"


if __name__ == '__main__':
	main()