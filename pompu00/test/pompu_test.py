import sys
sys.path.append("..")
import pompuAPI
from pompuAPI import *
reload (pompuAPI)
import numpy as np
import matplotlib.pyplot as plt
import unittest
import os
import glob
import pickle
import config

class PompuTest(unittest.TestCase):
    def setUp(self):
        self.api = PompuAPI(config.api_key, config.api_secret)
        self.symbol = 'XVGBTC'
        pass

    def test_orders(self):
        try:
            orders = self.api.get_open_orders(self.symbol,10)
            print "(orders): '%s" % orders
        except "BinanceAPIException" as e:
            print e.status_code
            print e.message
        pass

    def test_balances(self):
        try:
            balances = self.api.get_account()
            for balance in balances['balances'] :
                if float(balance["locked"]) > 0 or float(balance["free"]) > 0 :
                    print '%s: %s' % (balance['asset'], balance['free'])
            print "(balance): '%s" % balances['balances'][0]
            balances['balances'] = []
            print "(balance): '%s" % balances
        except "BinanceAPIException" as e:
            print e.status_code
            print e.message
        pass


    def test_tickers(self):
        try:
            tickers = self.api.get_ticker(self.symbol)
            print "(tickers):'%s" % tickers
        except "BinanceAPIException" as e:
            print e.status_code
            print e.message
        pass


    def test_server_time(self):
        try:
            server_time = self.api.get_server_time()
            print "(server_time):'%s" % server_time
        except "BinanceAPIException" as e:
            print e.status_code
            print e.message
        pass

    def test_open_orders(self):
        try:
            open_orders = self.api.get_open_orders(self.symbol)
            print "(open_orders):'%s" % open_orders
        except "BinanceAPIException" as e:
            print e.status_code
            print e.message
        pass

if __name__ == "__main__" :
  unittest.main()
  pass

#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-
