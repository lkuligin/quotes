#!/usr/bin/env python
# coding: utf8

from quotes import Quotes, Asset
from config import SQLITE_DB_NAME
import sqlite3
from datetime import datetime, date, timedelta
import csv
import get_micex_data
import re

if __name__ == "__main__":
	#res = float(get_micex_data.get_curr_quot('gazprom'))
	#print res, type(res)
	q = Quotes()
	#a1 = q.get_asset_by_id(4)
	assets = q.get_list_of_assets(update = 'yes')
	tbl = q.get_index_view()
	print tbl
	#a1.upload_available_history()
	#a1.download_from_csv('table.csv')
	#a1.upload_available_history()
	#a1.update_current_quote()
	#a = q.get_current_view()
	#print a1
	
	#a1 = q.get_list_of_assets()
	#print a1[0].name
	con = sqlite3.connect(SQLITE_DB_NAME, detect_types=sqlite3.PARSE_DECLTYPES)
	cur = con.cursor()
	d = date.today()
	#cur.execute('DELETE FROM Hist_Stock_Quotes')
	#cur.execute('DROP TABLE Hist_Stock_Quotes')
	#cur.execute('CREATE TABLE Curr_Quotes (asset_id INTEGER NOT NULL, price double, primary key (asset_id))')
	#cur.execute('CREATE TABLE Hist_Stock_Quotes (asset_id INTEGER NOT NULL, dayref DATE NOT NULL, adj_close double NOT NULL, high double, low double, vol int NOT NULL, primary key (asset_id, dayref))')
	#cur.execute('INSERT INTO Hist_Stock_Quotes VALUES (3, ?, 22.03, 24.04, 21.04, 456999)', (d,))
	#con.commit()
	cur.execute('SELECT * FROM assets')
	for row in cur:
		print row
	cur.execute('SELECT asset_id, COUNT(*), MIN(dayref), MAX(dayref) FROM Hist_Stock_Quotes GROUP BY asset_id')
	for row in cur:
		print row
	#a1 = cur.fetchone()
	#print a1, type(a1)
	#a1 = datetime(year=a1.year, month=a1.month,day=a1.day)
	#print a1, type(a1)
	#print d1, type(d1)

