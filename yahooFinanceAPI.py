import requests
import threading
import pandas as pd
import time, datetime

class YahooFinance:
    def __init__(self):
        self.url = 'https://query1.finance.yahoo.com/v8/finance/chart/'
    def get(self, ticker = None):
        data = []
        params = {
            'formatted':'true',
            'includeAdjustedClose':'true',
            'interval':'1d',
            'period1':'46800',
            'period2': str(int(time.time()))
        }
        if ticker:
            response = requests.get(self.url+ticker, params)
            data = response.json()
            dates = list(map(datetime.datetime.utcfromtimestamp,data['chart']['result'][0]['timestamp']))
            ohlcv = data['chart']['result'][0]['indicators']
            df = pd.DataFrame()
            df.insert(0,'date', dates)
            df.insert(1,'open', ohlcv['quote'][0]['open'])
            df.insert(2,'high', ohlcv['quote'][0]['high'])
            df.insert(3,'low', ohlcv['quote'][0]['low'])
            df.insert(4,'close', ohlcv['quote'][0]['close'])
            df.insert(5,'volume', ohlcv['quote'][0]['volume'])
            df.insert(6,'adj_close', ohlcv['adjclose'][0]['adjclose'])
            adjust_ratio = df.close/df.adj_close[0]
            df.insert(6,'adj_low', df.low/adjust_ratio)
            df.insert(6,'adj_high', df.high/adjust_ratio)
            df.insert(6,'adj_open', df.open/adjust_ratio)
            df.insert(10,'adj_volume', df.volume/adjust_ratio)
            df = df[::-1]
            df.reset_index(drop=True, inplace=True)
            return df
        else:
            raise Exception('ticker missing')


