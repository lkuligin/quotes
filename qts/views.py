# coding: utf8
#!/usr/bin/env python

from qts import web, quotes
from flask import render_template, flash, redirect
from forms import NewAssetForm
#from  quotes.py import Curr_quotes

@web.route('/')
@web.route('/index')
def index():
	assets = quotes.get_list_of_assets(update = 'yes')
	for asset in assets:
		asset.update_current_quote()
		asset.upload_available_history()
	tbl = quotes.get_index_view()
	curr_quotes = [{'name': row[1], 'ticker': row[2], 'price': round(row[3],2), 'maxprice': round(row[4],2), 'minprice': round(row[5],2)} for row in tbl]
	return render_template("index.html", curr_quotes = curr_quotes)
	
@web.route('/new_asset', methods = ['GET', 'POST'])
def add_new_asset():
	form = NewAssetForm()
	if form.validate_on_submit():
		quotes.add_new_asset(form.name.data, form.symb.data, form.source.data)
		flash('New asset ' + form.name.data)
		return redirect('/index')
	return render_template('new_asset.html', title = 'Add new asset', form = form)