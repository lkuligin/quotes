#!/usr/bin/env python
# coding: utf8
"""
Create a sqlite db, supports easy migration between different db versions
"""
import sqlite3
import os
from config import SQLITE_DB_NAME, API_CURR_VERS
db_versions_lists = ['1.0', '1.1']

def db_versions(version):
	if version == '1.1':
		con = sqlite3.connect(SQLITE_DB_NAME)
		cur = con.cursor()
		cur.execute('INSERT INTO Assets VALUES (3 ,\'Microsoft\',\'MSFT\',\'yahoo\')')
		cur.execute('CREATE TABLE Hist_Stock_Quotes (asset_id INTEGER NOT NULL, dayref date NOT NULL, adj_close double NOT NULL, high double, low double, vol int NOT NULL, primary key (asset_id, dayref))')
		cur.execute('CREATE TABLE Curr_Quotes (asset_id INTEGER NOT NULL, price double, primary key (asset_id))')
		cur.execute('UPDATE Version SET Db_Version = \'1.1\'')
		con.commit()
		con.close()

if __name__ == "__main__":
	#create a 1.0 db if we don't have a db at all
	if not os.path.exists(SQLITE_DB_NAME):
		con = sqlite3.connect(SQLITE_DB_NAME)
		cur = con.cursor()
		cur.execute('CREATE TABLE Version (Db_Version NVARCHAR(100))')
		cur.execute('INSERT INTO Version VALUES (''1.0'')')
		con.commit()
		cur.execute('CREATE TABLE Assets (asset_id INTEGER PRIMARY KEY, name NVARCHAR(100), symbol NVARCHAR(20), source NVARCHAR(100))')
		cur.execute('INSERT INTO Assets VALUES (1,\'Google\',\'GOOG\',\'yahoo\'), (2,\'Yandex\',\'YNDX\',\'yahoo\')')
		con.commit()
		con.close()
	con = sqlite3.connect(SQLITE_DB_NAME)
	cur = con.cursor()
	cur.execute('SELECT * FROM Version')
	curr_version = cur.fetchone()[0]
	con.close()
	#if we need to test newer version of db - need to switch below to the newer version instead of API_CURR_VERS
	if curr_version == API_CURR_VERS:
		print 'everything OK'
	else:
		for version in db_versions_lists:
			print 'migrating to version: ' + version
			db_versions(version)
			print 'success!'

