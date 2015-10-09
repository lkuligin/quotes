#!/usr/bin/env python
# coding: utf8
"""
Count the number of lines for each file. Files are ~0.5Gb each.
"""
import traceback
import os
import csv
#path to directory with files, files are big: ~0.5Gb each
PATH = "C:/Users/kuligin/Documents/git/lkuligin/test/"

def count_lines(path):
	try:
		i = 0
		with open(path) as f:
			for line in f:
				i += 1
		return i
	except:
		print "count lines error", traceback.format_exc()

if __name__ == "__main__":
#names of file to be analyzed
	files = ["bookings.csv", "searches.csv"]
	for file in files:
		print file, count_lines(os.path.join(PATH, file))
