import requests
import threading
import pandas as pd

class Marketstack:
    def __init__(self, apikey = None):
        if apikey:
            self.apikey = apikey
        else:
            try:
                f = open("apikey", "r")
                self.apikey = f.read().rstrip() #rstrip removes \n
                f.close()
            except:
                raise Exception("apikey missing")
        self.url = 'http://api.marketstack.com/v1'
        self.limit = 1000
        self.maxconnections = 5
        self.pool_sema = threading.BoundedSemaphore(value=self.maxconnections)

    def get(self, ticker = None):
        data = []
        params = {
            'access_key': self.apikey,
            'symbols': ticker,
            'limit': 1000,
            'offset':0,
            'date_from ': '2012-01-01'
        }
        if ticker:
            response = requests.get(self.url+'/eod', params)
            data.append(response.json()['data'])
            pagination_data = response.json()['pagination']
            for offset in range(pagination_data['limit'], pagination_data['total'], pagination_data['limit']):
                params['offset'] = offset
                response = requests.get(self.url+'/eod', params)
                data.append(response.json()['data'])
                pagination_data = response.json()['pagination']
            return pd.DataFrame([y for x in data for y in x])
        else:
            raise Exception('ticker missing')
