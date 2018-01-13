import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/..")
import  pompuAPI
from pompuAPI import *
reload (pompuAPI)
import numpy as np
import matplotlib.pyplot as plt
import unittest
import glob
import pickle
import config
import sqlite3
import sys
import pprint as pp
class PompuTest(unittest.TestCase):
    def setUp(self):
        self.api = PompuAPI(config.api_key, config.api_secret)
        self.symbol = 'XVGBTC'
        self.sql = sqlite3.connect('orders.db')
        pass

    def tearDown(self):
        self.sql.close
        pass

    # Database
    def write_sql(self,sql,data):
        """    
        Save order
        data = orderid,symbol,amount,price,side,quantity,profit
        Create a database connection
        """
        cur = sql.cursor()

        # should be 2d array!!!
        cur.executemany('''INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?)''', map(tuple, data))
        sql.commit()
        pass
        
    def read_sql(self,sql,orderid):
        """
        Query order info by id
        :param orderid: the buy/sell order id
        :return:
        """
        cur = sql.cursor()
        cur.execute("SELECT * FROM orders WHERE orderid = ?", (orderid,))
        return cur.fetchone()

    def test_sql(self):
        self.write_sql(self.sql,[ ["id-1",2,3,4,5,6,7],
                                  ["id-2",2,3,4,5,6,7] ])
        value = self.read_sql(self.sql, "id-1")
        print "(read sql):%s" % map(str,value)
        pass


    def _test_history(self):
        """
            only 1200 / 100   per 500 requesst
            this means every 5 seconds, I can fetch 4 data.
            This meas I cannot get forever
        """
        try:
            history = self.api.get_history(self.symbol,10)
            print "(history):"
            pp.pprint(history)
        except "BinanceAPIException" as e:
            print e.status_code
            print e.message
        pass

    def test_agg_trades(self):
        """
            about 500 data for 20sec
        """
        try:
            trades = self.api.get_aggTrades(self.symbol)
            print "(test_agg_trades):"
            print time.ctime(trades[0]['T']/1000)
            print time.ctime(trades[-1]['T']/1000)
          #  pp.pprint(trades)
        except "BinanceAPIException" as e:
            print e.status_code
            print e.message
        pass



    def test_trades(self):
        """
            about 4 sec 500 trades : 
        """
        try:
            trades = self.api.get_history(self.symbol,500)
            print "(trades):"
            print time.ctime(trades[0]['time'])
            print time.ctime(trades[-1]['time'])
          #  pp.pprint(trades)
        except "BinanceAPIException" as e:
            print e.status_code
            print e.message
        pass

    def test_klines(self):
        """
            about 4 sec 500 trades : 
        """
        try:
            trades = self.api.get_klines(self.symbol, "1m")
            print "(test_klines):"
            print trades[0][0]
            print trades[1][0]
            print time.ctime(trades[0][0]/1000)
            print time.ctime(trades[1][0]/1000)

          #  pp.pprint(trades)
        except "BinanceAPIException" as e:
            print e.status_code
            print e.message
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


    def test_ip_ban(self):
        """
The /api/v1/exchangeInfo rateLimits array contains objects 
    related to the exchange's REQUESTS and ORDER rate limits.
A 429 will be returned when either rather limit is violated.
Each route has a weight which determines for the number of requests each endpoint counts for. 
Heavier endpoints and endpoints that do operations on multiple symbols 
will have a heavier weight.
When a 429 is recieved, it's your obligation as an API to back off and not spam the API.
Repeatedly violating rate limits and/or failing to back off after receiving 429s will result in an automated IP ban (http status 418).
IP bans are tracked and scale in duration for repeat offenders, from 2 minutes to 3 days.
        """
        try:
            info = self.api.get_exchangeInfo()
            sys.stdout.write("(test_ip_ban):")
            pp.pprint( info["rateLimits"] )
        except "BinanceAPIException" as e:
            print e.status_code
            print e.message
        pass

if __name__ == "__main__" :
  unittest.main()
  pass

#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-
