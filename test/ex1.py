#!/usr/bin/env python
# coding: utf8
import traceback
import os
import csv
import pandas as pd
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
	files = ["bookings.csv", "searches.csv"]
	print "ex1"
	for file in files:
		print file, count_lines(os.path.join(PATH, file))
