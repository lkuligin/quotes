#!/usr/bin/env python
# coding: utf8

import os
basedir = os.path.abspath(os.path.dirname(__file__))
#yahoo API for current quotes (beginning part)
YAHOO_API_CURR_QUOTE_TITLE='https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in'#yahoo API for current quotes (ending part)
YAHOO_API_CURR_QUOTE_END='&format=json&diagnostics=true&env=store://datatables.org/alltableswithkeys&callback='
#yahoo API for historical quotes
YAHOO_API_HIST_QUOTE_TITLE='https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.historicaldata%20where%20symbol%20=%20' 
FINAM_CURR_QUOTE_TITLE='http://www.finam.ru/profile/moex-akcii/'
SQLITE_DB_NAME = os.path.join(basedir, 'quotes.db') #where sqlitedb is located
API_CURR_VERS = '1.1' #version of db API for db migration
MIN_DATE = '1980-01-01' 
CSRF_ENABLED = True
SECRET_KEY = 'really_secret_key'