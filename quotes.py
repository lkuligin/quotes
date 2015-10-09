# coding: utf8
from datetime import datetime, date, timedelta
import get_yahoo_data
import get_micex_data
from config import SQLITE_DB_NAME, MIN_DATE
import sqlite3
import csv
import sys
import traceback
"""
Asset - stores asset name, symbol, date format and source, initialize from a file??? or add new asset
Curr_Quotes - 

getassetbyid

"""
class Asset:
	"""a general class for assets"""
	def __init__(self, id, name, symb, source):
		self.id = id
		self.name = name
		self.symb = symb
		#self.quotes={} #example: {'dd-mm-yyyy': {'AdjClose': xx, 'High': xx, 'Low': xx, 'Vol': xx}}
		self.last_price = None
		self.dt_format = '%Y-%m-%d'
		self.source = source #yahoo, 
	def add_quote(self, dayRef, quote):
		if dayRef not in self.quotes.keys():
			self.quotes[dayRef] = quote
	def get_timeseries(self, indx):
		days = [datetime.strptime(day, self.dt_format) for day in self.quotes]
		days = sorted(days)
		values = [self.quotes[(datetime.strftime(day, self.dt_format))][str(indx)] for day in days]
		return days, values
		
	def update_current_quote(self):
		con = sqlite3.connect(SQLITE_DB_NAME, detect_types=sqlite3.PARSE_DECLTYPES)
		cur = con.cursor()
		if self.source == 'yahoo':
			last_price = get_yahoo_data.get_curr_quot(self.symb)
			cur.execute('UPDATE Curr_Quotes SET price = ? WHERE asset_id = ?', (last_price, self.id))
			con.commit()
		if self.source == 'micex':
			last_price = get_micex_data.get_curr_quot(self.symb)
			cur.execute('UPDATE Curr_Quotes SET price = ? WHERE asset_id = ?', (last_price, self.id))
			con.commit()
		con.close()
	#upload and store in db quoting history from min date to today-1
	def upload_available_history(self):
		try:
			con = sqlite3.connect(SQLITE_DB_NAME, detect_types=sqlite3.PARSE_DECLTYPES)
			cur = con.cursor()
			cur.execute('SELECT MAX(dayref) date FROM Hist_Stock_Quotes WHERE asset_id = ?', (self.id,))
			mindate = cur.fetchone()[0]
			if mindate == None: mindate = datetime.strptime(MIN_DATE, self.dt_format)
			else: 
				mindate = datetime.strptime(mindate, self.dt_format)
				mindate = datetime(year=mindate.year, month=mindate.month,day=mindate.day)+timedelta(days=1)
			mindate = datetime.strftime(mindate, self.dt_format)
			maxdate = datetime.strftime(date.today(), self.dt_format)
			if self.source == 'yahoo' and mindate <> maxdate:
				quotes = get_yahoo_data.get_hist_quot(self.symb, mindate, maxdate)
				for day in quotes:
					dq = self.quotes[day] #daily quote
					cur.execute('INSERT INTO Hist_Stock_Quotes VALUES (?, ?, ?, ?, ?, ?)', (self.id, day, dq['AdjClose'], dq['High'], dq['Low'], dq['Vol']))
					con.commit()
			#self.quotes = {}
		except:
			print "Didn't succeed to load and parse historical data:", traceback.format_exc()
	def download_from_csv(self, path):
		con = sqlite3.connect(SQLITE_DB_NAME, detect_types=sqlite3.PARSE_DECLTYPES)
		cur = con.cursor()
		with open(path, 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter = ',')
			try:
				row0 = reader.next()
				ind_date = row0.index('Date')
				ind_adj_close = row0.index('Adj Close')
				ind_high = row0.index('High')
				ind_low = row0.index('Low')
				ind_vol = row0.index('Volume')
				for row in reader:
					cur.execute('INSERT INTO Hist_Stock_Quotes VALUES (?, ?, ?, ?, ?, ?)', (self.id, row[ind_date], row[ind_adj_close], row[ind_high], row[ind_low], row[ind_vol]))
					con.commit()
			except:
				print "The file should have Date, High, Low, Volume, Adj Close columns:", traceback.format_exc()

class Quotes:
	def __init__(self):
		self.dbname = SQLITE_DB_NAME
	def get_asset_by_id(self, id):
		con = sqlite3.connect(self.dbname)
		cur = con.cursor()
		cur.execute('SELECT * FROM assets WHERE asset_id=?', (id,))
		asset = cur.fetchone()
		return Asset(asset[0], asset[1], asset[2], asset[3])
	def get_list_of_assets(self, **kwargs):
		con = sqlite3.connect(self.dbname)
		cur = con.cursor()
		cur.execute('SELECT ast.asset_id, ast.name, ast.symbol, ast.source, MAX(hq.dayref) maxdate FROM assets ast LEFT OUTER JOIN Hist_Stock_Quotes hq ON ast.asset_id =hq.asset_id GROUP BY ast.asset_id, ast.name, ast.symbol, ast.source')
		return [Asset(asset[0], asset[1], asset[2], asset[3]) for asset in cur]
	def add_new_asset(self, name, symb, source):
		con = sqlite3.connect(self.dbname)
		cur = con.cursor()
		cur.execute('SELECT MAX(asset_id) FROM assets')
		id = cur.fetchone()[0] + 1
		cur.execute('INSERT INTO assets VALUES (?,?,?,?)', (id, name, symb, source))
		cur.execute('INSERT INTO Curr_Quotes VALUES (?, NULL)', (id,))
		con.commit()
		print 'added'
		con.close()
	def get_index_view(self):
		con = sqlite3.connect(self.dbname)
		cur = con.cursor()
		cur.execute('SELECT hq.asset_id, ast.name, ast.symbol, cq.price, IFNULL(MAX(hq.adj_close),-1) maxprice, IFNULL(MIN(hq.adj_close),-1) minprice FROM Hist_Stock_Quotes as hq, assets as ast, Curr_Quotes cq WHERE ast.asset_id = hq.asset_id AND ast.asset_id = cq.asset_id and hq.dayref >= date(\'now\', \'-1 year\') GROUP BY hq.asset_id, ast.name, ast.symbol')
		res = cur.fetchall()
		con.close()
		return res