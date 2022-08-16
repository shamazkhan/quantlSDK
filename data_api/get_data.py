import requests
import pandas as pd
from io import StringIO
import time
import datetime

api_token = '629e878bade044.51655762'

class GetData():
    def __init__(self, symbol, group):
        self.symbol = symbol
        self.group = group

    def get_daily_data(self, period):
        symbol = self.symbol
        group = self.group
        url = 'https://eodhistoricaldata.com/api/eod/' + symbol + '.' + group + '?api_token=' + api_token + '&period=' + period
        r = requests.get(url)
        df_daily = pd.read_csv(StringIO(r.text), skipfooter=1, parse_dates=[0], index_col=0, engine='python')
        return df_daily

    def get_intraday_data(self, interval):
        symbol = self.symbol
        group = self.group
        # 1m for minute, 5m for 5 minute, 1h for hourly intervals
        url = 'https://eodhistoricaldata.com/api/intraday/' + symbol + '.' + group + '?api_token=' + api_token + '&interval=' + interval
        r = requests.get(url)
        df_intraday = pd.read_csv(StringIO(r.text), skipfooter=1, parse_dates=[0], index_col=0, engine='python')
        return df_intraday

    def get_data_strategy(self, period, start_date='2012-02-28', end_date='2022-02-28'):
        symbol = self.symbol
        group = self.group
        url = 'https://eodhistoricaldata.com/api/eod/' + symbol + '.' + group + '?api_token=' + api_token + '&period=' + period + '&from=' + start_date + '&to=' + end_date
        r = requests.get(url)
        df = pd.read_csv(StringIO(r.text), skipfooter=1, parse_dates=[0], index_col=0, engine='python')
        df = df.reset_index()
        df.columns = ['date', 'open', 'high', 'low', 'close', 'adj_close', 'volume']
        df['datetime'] = df['date']
        return df