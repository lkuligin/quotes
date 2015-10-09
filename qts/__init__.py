#!/usr/bin/env python
# coding: utf8

from flask import Flask

web = Flask(__name__)
web.config.from_object('config')

from quotes import Quotes
quotes = Quotes()

from qts import views