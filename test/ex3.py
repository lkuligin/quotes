#!/usr/bin/env python
# coding: utf8
"""plot the monthly number of searches for flights arriving at Málaga, Madrid or Barcelona
the arriving airport = the Destination column in the searches file
"""
import traceback
import os
import csv
import pandas as pd
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

PATH = "C:/Users/kuligin/Documents/git/lkuligin/test/searches.csv"

def count_airports(path, airports, lines_to_do = None):
#lines_to_do is for testing purpose only
	try:
		#res = pd.DataFrame(columns = ['year', 'month', 'airport', 'count']) - too slow
		res = {}
		lines_corrupted = 0
		with open(path) as f:
			datareader = csv.reader(f, delimiter = '^')
			headers = datareader.next()
			destination_hind = headers.index("Destination")
			date_hind = headers.index("Date")
			lines_done = 1
			lines_read = 0
			for row in datareader:
				lines_done += 1
				#some lines might be corrupted - missing delimiters, etc.
				if len(row) == len(headers):
					destination = row[destination_hind]
					date = pd.to_datetime(row[date_hind], format = '%Y-%m-%d')
					if destination in airports:
						if date in res.keys():
							if destination in res[date].keys(): 
								res[date][destination] += 1
							else: res[date][destination] = 1
						else:
							res[date] = {destination: 1}
						lines_read += 1
					#for testing purpose only
					if lines_read > lines_to_do and lines_to_do is not None: return pd.DataFrame(res).transpose(), lines_corrupted
				else:
					#print 'corrupted: ', lines_done
					lines_corrupted += 1
				if lines_done % 250000 == 0: print "rows done:", lines_done
		return pd.DataFrame(res).transpose(), lines_corrupted
	except:
		print row
		print "error: ", traceback.format_exc()

if __name__ == "__main__":
	pd.options.mode.chained_assignment = None  # default='warn'
	#aiport names + IATA codes
	airports = pd.DataFrame({'IATA': pd.Series(['AGP', 'MAD', 'BCN'], index = ['Malaga', 'Madrid', 'Barcelona'])})
	#receive dataframe with date | IATA code
	airports_searches, corrupted = count_airports(PATH, airports['IATA'].tolist())
	print airports_searches
	print "lines corrupted: ", corrupted
	#fig, ax = plt.subplots()
	airports_searches = airports_searches.resample('MS',how=sum)
	airports_searches = airports_searches.set_index(airports_searches.index.values + np.timedelta64(14, 'D'))
	print airports_searches
	ax = airports_searches.plot(style=['o','--'])
	#for airport in airports['IATA'].tolist():
	#	searches = airports_searches[airports_searches['airport']==airport]
	#	searches['count'] = 1
	#	searches = searches[['date', 'count']]
	#	searches = searches.set_index('date')
	#	searches = searches.resample('MS',how=sum)
	#	#for better autoscaling
	#	searches = searches.set_index(searches.index.values + np.timedelta64(14, 'D'))
	#	ax.plot(searches.index, searches['count'], linestyle='--', marker='o', label = airport)
	plt.title('Searches per month')
	ax.xaxis.set_major_formatter(mdates.DateFormatter("%b'%y"))
	ax.xaxis.set_major_locator(mdates.AutoDateLocator())
	ax.autoscale_view()
	ax.legend()
	fig = ax.get_figure()
	fig.autofmt_xdate()
	fig.savefig('test.png')
	plt.close(fig)
