#!/usr/bin/env python
# coding: utf8
"""top 10 arrival airports in the world in 2013
Arrival airport is the column arr_port. It is the IATA code for the airport
 total number of passengers for an airport =  sum the column pax, grouping by arr_port ( there is negative pax that corresponds to cancelations)
"""
import traceback
import os
import csv
import pandas as pd
import json
from urllib import urlencode
import urllib2
PATH = "C:/Users/kuligin/Documents/git/lkuligin/test/bookings.csv"
API_Key = 'f809f8c11e0601b2fe24ca3e92196e51'
API_url = 'https://airport.api.aero/airport/'

def get_airport (symb):
#https://www.developer.aero/Airport-API/Try-it-Now - can be used to detect airport
	try:
		params = {'user_key': API_Key}
		url = ''.join((API_url, symb.rstrip(), '?', urlencode(params)))
		data = urllib2.urlopen(url).read()
		#the answer is "callback(<json>)" and needs to be deserialized
		data =  data[9:][:-1]
		res = json.loads(data)
		return res['airports'][0]['name']
	except:
		print "Didn't suceed to download airport's name", traceback.format_exc()
		return None

def count_airports(path, lines_to_do = None):
#lines_to_do is for testing purpose only = no need to read all huge file for testing
	try:
		res = pd.Series()
		mindate = pd.to_datetime('2013-01-01 00:00:00', format = '%Y-%m-%d %H:%M:%S')
		maxdate = pd.to_datetime('2013-01-01 00:00:00', format = '%Y-%m-%d %H:%M:%S')
		with open(path) as f:
			datareader = csv.reader(f, delimiter = '^')
			#determine  columns indexes
			headers = datareader.next()
			airport_hind = headers.index("arr_port")
			pax_hind = headers.index("pax")
			date_hind = headers.index("act_date           ")
			lines_done = 1
			#sometimes the line might be corrupted - e.g. 2013-03-25 00:00:00^1V    JP      ^^a37584d1485cb35991e4ff1a2ba92262^2013-03-2500:00:00^8371^60^NRT     ^TYO     ^JP      ^SIN     ^SIN     ^SG      ^HND     TYO     ^JP      ^NRT     ^TYO     ^JP      ^SIN     ^SIN     ^SG      ^NRTSIN  ^SINTYO  ^JPSG    ^1^NRTSIN         ^XR,Q        ^Y        ^2013-04-14 11:05:00^2013-04-14 17:10:56^2^2013^3^NULL 
			lines_corrupted = 0
			#print headers
			for row in datareader:
				lines_done += 1
				if len(row) == len(headers):
					airport = row[airport_hind]
					pax = int(row[pax_hind])
					date = pd.to_datetime(row[date_hind], format = '%Y-%m-%d %H:%M:%S')
					if airport in res.index:
						#print "index: ", airport, res.loc[airport], res.loc[airport]+pax
						res.set_value(airport, res.loc[airport] + pax)
					else: res.set_value(airport, pax)
					if date < mindate: mindate = date
					if date > maxdate: maxdate = date
				else:
					#print 'corrupted: ', lines_done
					lines_corrupted += 1
				#for testing purpose only
				if lines_done > lines_to_do and lines_to_do is not None:
					return res, lines_corrupted
				if lines_done % 500000 == 0: print "rows done:", lines_done
			#I was asked only for 2013, so it's for control. Better to transfer mindate, maxdate to the function's optional  parameters
			print 'mindate:', mindate, 'maxdate:', maxdate
		return res, lines_corrupted
	except:
		print row
		print "error: ", traceback.format_exc()

if __name__ == "__main__":
	airports_arrivals, corrupted = count_airports(PATH)
	#some lines might be corrupted - look at the comment above
	print "lines corrupted: ", corrupted
	airports_arrivals_top = pd.DataFrame({'count': airports_arrivals.order(ascending = False)[:10]})
	#add the name of the airport instead of the code
	airports_arrivals_top['airport']= airports_arrivals_top.index.map(lambda x: get_airport(x))
	print airports_arrivals_top
