import time
import hashlib
import requests

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode
 
#https://github.com/purboox/BinanceAPI

class PompuAPI:
    
    BASE_URL_V1 = "https://www.binance.com/api/v1"
    BASE_URL_V3 = "https://api.binance.com/api/v3"

    def __init__(self, key, secret):
        self.key = key
        self.secret = secret


    def get_history(self, market, limit=50):
        path = "%s/historicalTrades" % self.BASE_URL_V1
        params = {"symbol": market, "limit": limit}
        return self._get_no_sign(path, params)
        
    def get_trades(self, market, limit=50):
        path = "%s/trades" % self.BASE_URL_V1
        params = {"symbol": market, "limit": limit}
        return self._get_no_sign(path, params)
        
    def get_klines(self, market, interval):
        path = "%s/klines" % self.BASE_URL_V1
        params = {"symbol": market, "interval": interval}
        return self._get_no_sign(path, params)

    def get_aggTrades(self, market):
        path = "%s/aggTrades" % self.BASE_URL_V1
        params = {"symbol": market}
        return self._get_no_sign(path, params)
        
    def get_ticker(self, market):
        path = "%s/ticker/24hr" % self.BASE_URL_V1
        params = {"symbol": market}
        return self._get_no_sign(path, params)

    def get_orderbooks(self, market, limit=50):
        path = "%s/depth" % self.BASE_URL_V1
        params = {"symbol": market, "limit": limit}
        return self._get_no_sign(path, params)

    def get_account(self):
        path = "%s/account" % self.BASE_URL_V1
        return self._get(path, {})

    def get_open_orders(self, symbol, limit = 100):
        path = "%s/openOrders" % self.BASE_URL_V1
        params = {"symbol": symbol}
        return self._get(path, params)

    def get_exchangeInfo(self):
        path = "%s/exchangeInfo" % self.BASE_URL_V1
        return self._get_no_sign(path)

    def get_server_time(self):
        path = "%s/time" % self.BASE_URL_V1
        return self._get_no_sign(path, {})

    def buy_limit(self, market, quantity, rate):
        path = "%s/order" % self.BASE_URL_V1
        params = {"symbol": market, "side": "BUY", \
            "type": "LIMIT", "timeInForce": "GTC", \
            "quantity": '%.8f' % quantity, "price": '%.8f' % rate}
        return self._post(path, params)

    def sell_limit(self, market, quantity, rate):
        path = "%s/order" % self.BASE_URL_V1
        params = {"symbol": market, "side": "SELL", \
            "type": "LIMIT", "timeInForce": "GTC", \
            "quantity": '%.8f' % quantity, "price": '%.8f' % rate}
        return self._post(path, params)

    def buy_market(self, market, quantity):
        path = "%s/order" % self.BASE_URL_V1
        params = {"symbol": market, "side": "BUY", \
            "type": "MARKET", "quantity": '%.8f' % quantity}
        return self._post(path, params)

    def sell_market(self, market, quantity):
        path = "%s/order" % self.BASE_URL_V1
        params = {"symbol": market, "side": "SELL", \
            "type": "MARKET", "quantity": '%.8f' % quantity}
        return self._post(path, params)

    def query_order(self, market, orderId):
        path = "%s/order" % self.BASE_URL_V1
        params = {"symbol": market, "orderId": orderId}
        return self._get(path, params)

    def cancel(self, market, order_id):
        path = "%s/order" % self.BASE_URL_V1
        params = {"symbol": market, "orderId": order_id}
        return self._delete(path, params)

    def _get_no_sign(self, path, params={}):
        query = urlencode(params)
        url = "%s?%s" % (path, query)
        header = {"X-MBX-APIKEY": self.key}
        return requests.get(url, headers=header, timeout=30, verify=True).json()
    
    def _sign(self, params={}):
        data = params.copy()

        ts = str(int(1000 * time.time()))
        data.update({"timestamp": ts})

        h = self.secret + "|" + urlencode(data)
        signature = hashlib.sha256(h).hexdigest()
        data.update({"signature": signature})
        return data

    def _get(self, path, params={}):
        params.update({"recvWindow": 120000})
        query = urlencode(self._sign(params))
        url = "%s?%s" % (path, query)
        header = {"X-MBX-APIKEY": self.key}
        return requests.get(url, headers=header, \
            timeout=30, verify=True).json()


    def _post(self, path, params={}):
        params.update({"recvWindow": 120000})
        query = urlencode(self._sign(params))
        url = "%s?%s" % (path, query)
        header = {"X-MBX-APIKEY": self.key}
        return requests.post(url, headers=header, \
            timeout=30, verify=True).json()


    def _delete(self, path, params={}):
        params.update({"recvWindow": 120000})
        query = urlencode(self._sign(params))
        url = "%s?%s" % (path, query)
        header = {"X-MBX-APIKEY": self.key}
        return requests.delete(url, headers=header, \
            timeout=30, verify=True).json()
