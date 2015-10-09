# coding: utf8
"""
Download historical and present data using Yahoo.Finance
https://code.google.com/p/yahoo-finance-managed/wiki/YahooFinanceAPIs
"""
import urllib2
from lxml import html, etree
import json
import sys
from datetime import datetime
from datetime import timedelta
from config import FINAM_CURR_QUOTE_TITLE
import traceback
import re

def get_curr_quot(ticker):
	try:
		url = "".join((FINAM_CURR_QUOTE_TITLE, ticker))
		print url
		doc = urllib2.urlopen(url).read();
		page = html.fromstring(doc)
		path = "id('issuer-profile-informer-last')"
		nodes = page.xpath(path)
		s = nodes[0].text_content()
		#for node in nodes:
		#	print node.text_content()
		#	print etree.tostring(node, encoding='utf-8')
		return re.findall('\d+.?\d+', s)[0].replace(',','.')
	except:
		print "I didn't succeed to load and parse the quote:", traceback.format_exc()

def get_hist_quot(ticker,
	startdate = (str((datetime.now()+timedelta(weeks=-4)).year)+'-'+str((datetime.now()+timedelta(weeks=-4)).month)
		+'-'+str((datetime.now()+timedelta(weeks=-4)).day)),
	enddate = (str(datetime.now().year)+'-'+str(datetime.now().month)
		+'-'+str(datetime.now().day))):
	try:
		url = '"' + ticker + '"' + ' and startDate = "'
		url = url + startdate + '" and endDate = "' + enddate + '" '
		url = YAHOO_API_HIST_QUOTE_TITLE + convert_url(url) + YAHOO_API_CURR_QUOTE_END
		data = urllib2.urlopen(url)
		res = json.load(data)
		res = res['query']['results']['quote']
		if str(type(res)) == '<type \'dict\'>': 
			res = [res]
		res1 = {}
		for item in res:
			res1[item['Date']] =  {'AdjClose': item['Adj_Close'], 'High': item['High'], 'Low': item['Low'], 'Vol': item['Volume']}
		return res1
	except:
		print "Didn't succeed to load and parse historical data:", traceback.format_exc() #sys.exc_info()[1]
