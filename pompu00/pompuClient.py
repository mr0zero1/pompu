import config
import time
import hashlib
import requests
import PompuApi

try: 
  from urllib import urlencode
except ImportEror:
  from urllib.parse import urlencode

#-----------------------------------------------------------
# client
#-----------------------------------------------------------
class PompuCilent:
  def __init__(self, key, secret):
    self.client = BinanceAPI(config.api_key, config.api_secret)
#    conn = sqlite3.connect('orders.db')
    pass

  def hello(self):
    print("hello")
    pass



