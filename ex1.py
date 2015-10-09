#!/usr/bin/env python
# coding: utf8
import urllib2
from urllib import urlencode, quote
import json
import traceback

import pandas as pd
import matplotlib as mpl
mpl.use('Agg') #the script is used from command line without GUI
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D 

API_Key = 'f809f8c11e0601b2fe24ca3e92196e51'
API_url = 'https://airport.api.aero/airport/'
#https://www.developer.aero/Airport-API/Try-it-Now - can be used to detect airport

def test_plot():
	countries = ['France','Spain','Sweden','Germany','Finland','Poland','Italy', 'United Kingdom','Romania','Greece','Bulgaria','Hungary', 'Portugal','Austria','Czech Republic','Ireland','Lithuania','Latvia', 'Croatia','Slovakia','Estonia','Denmark','Netherlands','Belgium']
	
	extensions = [547030,504782,450295,357022,338145,312685,301340,243610,238391,
	131940,110879,93028,92090,83871,78867,70273,65300,64589,56594,
	49035,45228,43094,41543,30528]
	
	populations = [63.8,47,9.55,81.8,5.42,38.3,61.1,63.2,21.3,11.4,7.35,
	9.93,10.7,8.44,10.6,4.63,3.28,2.23,4.38,5.49,1.34,5.61,
	16.8,10.8]

	life_expectancies = [81.8,82.1,81.8,80.7,80.5,76.4,82.4,80.5,73.8,80.8,73.5,
	74.6,79.9,81.1,77.7,80.7,72.1,72.2,77,75.4,74.4,79.4,81,80.5]

	data = {'extension' : pd.Series(extensions, index=countries), 
	'population' : pd.Series(populations, index=countries),
	'life expectancy' : pd.Series(life_expectancies, index=countries)}
 
	df = pd.DataFrame(data)
	df = df.sort('life expectancy')
	
	print df
	
	fig, axes = plt.subplots(nrows=3, ncols=1)
	for i, c in enumerate(df.columns):
		df[c].plot(kind='bar', ax=axes[i], figsize=(12, 10), title=c)
		plt.savefig('EU1.png', bbox_inches='tight')
	
	# Create a figure of given size
	fig = plt.figure(figsize=(16,12))
	# Add a subplot
	ax = fig.add_subplot(111)
	# Set title
	ttl = 'Population, size and age expectancy in the European Union'
	# Set color transparency (0: transparent; 1: solid)
	a = 0.7
	# Create a colormap
	customcmap = [(x/24.0,  x/48.0, 0.05) for x in range(len(df))]
	# Plot the 'population' column as horizontal bar plot
	df['population'].plot(kind='barh', ax=ax, alpha=a, legend=False, color=customcmap,
	edgecolor='w', xlim=(0,max(df['population'])), title=ttl)
	

def get_airport (symb):
	try:
		params = {'user_key': API_Key}
		#url = ''.join((API_url, quote(''.join((symb, '?'))), urlencode(params)))
		url = ''.join((API_url, symb, '?', urlencode(params)))
		data = urllib2.urlopen(url).read()
		data =  data[9:][:-1]
		res = json.loads(data)
		return res['airports'][0]['name']
	except:
		print "Didn't suceed to download airport's name", traceback.format_exc()
		return None

if __name__ == '__main__':
	s = 'SVO'
	#print get_airport(s)
	test_plot()