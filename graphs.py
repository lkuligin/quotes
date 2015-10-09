# coding: utf8
from get_yahoo_data import get_hist_quot
from quotes import Asset
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
#from matplotlib.dates import DateFormatter
import sys
#!/usr/bin/env python
#coding: utf8

"""
Plots different types of graphs about stocks/bonds quotes
"""
from datetime import datetime

def date_autoformat(days):
#если собираем
	date0 = min(days)
	date1 = max(days)
	n = len(days)
	print date0, date1, n

if __name__ == "__main__":
	google = Asset('Google', 'GOOG')
	startdate='2015-06-01'
	enddate='2015-06-28'
	google.quotes = get_hist_quot(google.symb, startdate, enddate)
	#print google.quotes['2015-06-03']
	days, values = google.get_timeseries('AdjClose')
	print days
	days = mdates.date2num(days)
	fig, ax = plt.subplots()
	ax.plot_date(days, values, '-')
	ax.xaxis.set_major_formatter(mdates.DateFormatter("%d-%b'%y"))
	ax.xaxis.set_major_locator(mdates.AutoDateLocator())
	ax.autoscale_view()
	fig.autofmt_xdate()
	#ays=datetime.strptime(
	# = mdates.date2num(days)
	#ax.plot_date(x=x, y=y)
	fig.savefig('test.png')
	plt.close(fig)
	