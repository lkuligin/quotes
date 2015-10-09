#!/usr/bin/env python
# coding: utf8
"""For every search in the searches file, find out whether the search ended up in a booking or not (using the info in the bookings file). For instance, search and booking origin and destination should match. For the bookings file, origin and destination are the columns dep_port and arr_port, respectively. Generate a CSV file with the search data, and an additional field, containing 1 if the search ended up in a booking, and 0 otherwise.
"""
import traceback
import os
import csv
import pandas as pd
PATH_booking = "C:/Users/kuligin/Documents/git/lkuligin/test/bookings.csv"
PATH_searches = "C:/Users/kuligin/Documents/git/lkuligin/test/searches.csv"
PATH_searches_output = "C:/Users/kuligin/Documents/git/lkuligin/test/searches_new.csv"

def test():
	with open("C:/Users/kuligin/Documents/git/lkuligin/test/searches.csv") as f:
		i = 0
		datareader = csv.reader(f, delimiter = '^')
		headers = datareader.next()
		i1 = headers.index("Seg1BookingCode")
		i2 = headers.index("Seg2BookingCode")
		i3 = headers.index("Seg3BookingCode")
		i4 = headers.index("Seg4BookingCode")
		i5 = headers.index("Seg5BookingCode")
		i6 = headers.index("Seg6BookingCode")
		print headers
		for row in datareader:
			if len(row) == len(headers):
				if row[i1] == "" and row[i2] <> "":
					print row

def load_to_set(path, lines_to_do = None):
#index on the bookings.file. Set seems to be fasted than list: https://juliank.wordpress.com/2008/04/29/python-speed-x-in-list-vs-x-in-set/
	try:
		res = []
		lines_done = 0
		i = 0
		with open(path) as f:
			datareader = csv.reader(f, delimiter = '^')
			headers = datareader.next()
		#i1 = headers.index("rloc          ")
		#i2 = headers.index("pos_oid  ")
			dest_ind = headers.index("arr_port")
			arr_ind = headers.index("dep_port")
			date_ind = headers.index("act_date           ")
			for row in datareader:
				lines_done += 1
				if len(row) == len(headers):
					i += 1
					b_destination = row[dest_ind]
					b_origin = row[arr_ind]
					b_date = pd.to_datetime(row[date_ind], format = '%Y-%m-%d %H:%M:%S')
				#if (b_destination == destination and b_origin  == origin 
				#    and (b_date - date).total_seconds < 10000):
				#    print row
					res.append((b_date.date(), b_destination.rstrip(), b_origin.rstrip()))
				if i % 250000 == 0: print i
				if lines_to_do is not None and lines_done > lines_to_do: return set(res)
		return set(res)
	except:
		print "error: ", traceback.format_exc()

def update_searches(path, path_output, search_set, lines_to_do = None):
	try:
		lines_done = 0
		with open(path) as csv_input:
			with open(path_output, 'wt') as csv_output:
				datareader = csv.reader(csv_input, delimiter = '^')
				datawriter = csv.writer(csv_output, delimiter = '^', lineterminator='\n')
				headers = datareader.next()
				newheaders = headers + ['res']
				datawriter.writerow(newheaders)
				date_ind = headers.index("Date")
				time_ind = headers.index("Time")
				office_ind = headers.index("OfficeID")
				destination_ind = headers.index("Destination")
				origin_ind = headers.index("Origin")
				cntr_ind = headers.index("Country")
				for row in datareader:
					lines_done += 1
					res = 0
					if len(row) == len(headers):
						#date = pd.to_datetime(row[date_ind] + " " + row[time_ind], format = '%Y-%m-%d %H:%M:%S')
						date = pd.to_datetime(row[date_ind], format = '%Y-%m-%d')
						destination = row[destination_ind]
						origin = row[origin_ind]
						search = (date.date(), destination, origin)
						if search in search_set: 
							res = 1
					row.append(res)
					datawriter.writerow(row)
					if lines_to_do is not None and lines_done > lines_to_do: return 
		return
	except:
		print "error: ", traceback.format_exc()
		
def success_searches(path, search_set, lines_to_do = None):
	try:
		lines_done = 0
		lines_success = 0
		with open(path) as csv_input:
			datareader = csv.reader(csv_input, delimiter = '^')
			headers = datareader.next()
			date_ind = headers.index("Date")
			destination_ind = headers.index("Destination")
			origin_ind = headers.index("Origin")
			for row in datareader:
				lines_done += 1
				if len(row) == len(headers):
					date = pd.to_datetime(row[date_ind], format = '%Y-%m-%d')
					destination = row[destination_ind]
					origin = row[origin_ind]
					search = (date.date(), destination, origin)
					if search in search_set: 
						lines_success += 1
				if lines_to_do is not None and lines_done > lines_to_do: return lines_done, lines_success
		return lines_done, lines_success
	except:
		print "error: ", traceback.format_exc()

if __name__ == "__main__":
	bookings = load_to_set(PATH_booking,)
	update_searches(PATH_searches, PATH_searches_output, bookings, 50000)
	print 'example done'
	lines_done, lines_success = success_searches(PATH_searches, bookings)
	print "lines in search: ", lines_done
	print "lines success: ", lines_success
	print "success ratio ", 1.0*lines_success/lines_done
