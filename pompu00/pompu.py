import config
import time
import hashlib
import requests
import PompuApi

try: 
  from urllib import urlencode
except ImportEror:
  from urllib.parse import urlencode


# Set parser
parser = argparse.ArgumentParser()
parser.add_argument("--quantity", type=int, help="Buy/Sell Quantity", default=200)
parser.add_argument("--symbol", type=str, help="Market Symbol (Ex: XVGBTC)", required=True)
parser.add_argument("--profit", type=float, help="Target Profit", default=1.3)
parser.add_argument("--stoploss", type=float, help="Target Stop-Loss % (If the price drops by 6%, sell market_price.)", default=0) # Not complated (Todo)

parser.add_argument("--increasing", type=float, help="Buy Price +Increasing (0.00000001)", default=0.00000001)
parser.add_argument("--decreasing", type=float, help="Sell Price -Decreasing (0.00000001)", default=0.00000001)

# Manually defined --orderid try to sell 
parser.add_argument("--orderid", type=int, help="Target Order Id (use balance.py)", default=0)

parser.add_argument("--wait_time", type=int, help="Wait Time (seconds)", default=1)
parser.add_argument("--test_mode", type=bool, help="Test Mode True/False", default=False)
parser.add_argument("--prints", type=bool, help="Scanning Profit Screen Print True/False", default=True)
parser.add_argument("--debug", type=bool, help="Debug True/False", default=True)
parser.add_argument("--loop", type=int, help="Loop (0 unlimited)", default=0)

option = parser.parse_args()


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

def main():
  pompu = PompuClient(config.api_key, config.api_secret) 
  pompu.hello()

if __name__ == "__main__":
  main()



