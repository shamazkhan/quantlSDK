import requests
import pandas as pd
from io import StringIO
import time
import datetime
import get_data

'''EOD API TOKEN --- DO NOT REMOVE'''
api_token = '629e878bade044.51655762'


class TechnicalIndicators():
    def __init__(self,symbol,group):
        self.symbol = symbol
        self.group = group


    def average_volume(self, period=50):
        symbol = self.symbol
        group = self.group
        order = 'a'
        period = str(period)
        function = 'avgvol'

        url = 'https://eodhistoricaldata.com/api/technical/' + symbol + '.' + group + '?order=' + order + '&fmt=csv' + '&function=' + function + '&period=' + period + '&api_token=' + api_token
        r = requests.get(url)
        df_average_volume = pd.read_csv(StringIO(r.text), skipfooter=1, parse_dates=[0], index_col=0, engine='python')
        return df_average_volume

    def average_volume_by_price(self, period=50):
        symbol = self.symbol
        group = self.group
        order = 'a'
        period = str(period)
        function = 'avgvolccy'

        url = 'https://eodhistoricaldata.com/api/technical/' + symbol + '.' + group + '?order=' + order + '&fmt=csv' + '&function=' + function + '&period=' + period + '&api_token=' + api_token
        r = requests.get(url)
        df_average_volume_by_price = pd.read_csv(StringIO(r.text), skipfooter=1, parse_dates=[0], index_col=0, engine='python')
        return df_average_volume_by_price

    def simple_moving_average(self, period=50):
        symbol = self.symbol
        group = self.group
        order = 'a'
        period = str(period)
        function = 'sma'

        url = 'https://eodhistoricaldata.com/api/technical/' + symbol + '.' + group + '?order=' + order + '&fmt=csv' + '&function=' + function + '&period=' + period + '&api_token=' + api_token
        r = requests.get(url)
        df_simple_moving_average = pd.read_csv(StringIO(r.text), skipfooter=1, parse_dates=[0], index_col=0, engine='python')
        return df_simple_moving_average

    def exponential_moving_average(self, period=50):
        symbol = self.symbol
        group = self.group
        order = 'a'
        period = str(period)
        function = 'ema'

        url = 'https://eodhistoricaldata.com/api/technical/' + symbol + '.' + group + '?order=' + order + '&fmt=csv' + '&function=' + function + '&period=' + period + '&api_token=' + api_token
        r = requests.get(url)
        df_exponential_moving_average = pd.read_csv(StringIO(r.text), skipfooter=1, parse_dates=[0], index_col=0, engine='python')
        return df_exponential_moving_average

    def weighted_moving_average(self, period=50):
        symbol = self.symbol
        group = self.group
        order = 'a'
        period = str(period)
        function = 'wma'

        url = 'https://eodhistoricaldata.com/api/technical/' + symbol + '.' + group + '?order=' + order + '&fmt=csv' + '&function=' + function + '&period=' + period + '&api_token=' + api_token
        r = requests.get(url)
        df_weighted_moving_average = pd.read_csv(StringIO(r.text), skipfooter=1, parse_dates=[0], index_col=0, engine='python')
        return df_weighted_moving_average

    def volatility(self, period=50):
        symbol = self.symbol
        group = self.group
        order = 'a'
        period = str(period)
        function = 'volatility'

        url = 'https://eodhistoricaldata.com/api/technical/' + symbol + '.' + group + '?order=' + order + '&fmt=csv' + '&function=' + function + '&period=' + period + '&api_token=' + api_token
        r = requests.get(url)
        df_volatility = pd.read_csv(StringIO(r.text), skipfooter=1, parse_dates=[0], index_col=0, engine='python')
        return df_volatility

    def stochastic_technical_indicator(self, fast_kperiod=14, slow_kperiod=3, slow_dperiod=3):
        symbol = self.symbol
        group = self.group
        order = 'a'
        fast_kperiod = str(fast_kperiod)
        slow_kperiod = str(slow_kperiod)
        slow_dperiod = str(slow_dperiod)
        function = 'stochastic'

        url = 'https://eodhistoricaldata.com/api/technical/' + symbol + '.' + group + '?order=' + order + '&fmt=csv' + '&function=' + function + '&fast_kperiod=' + fast_kperiod + '&slow_kperiod=' + slow_kperiod + '&slow_dperiod=' + slow_dperiod + '&api_token=' + api_token
        r = requests.get(url)
        df_stochastic_technical_indicator = pd.read_csv(StringIO(r.text), skipfooter=1, parse_dates=[0], index_col=0, engine='python')
        return df_stochastic_technical_indicator

    def relative_strength_index(self, period=50):
        symbol = self.symbol
        group = self.group
        order = 'a'
        period = str(period)
        function = 'rsi'

        url = 'https://eodhistoricaldata.com/api/technical/' + symbol + '.' + group + '?order=' + order + '&fmt=csv' + '&function=' + function + '&period=' + period + '&api_token=' + api_token
        r = requests.get(url)
        df_relative_strength_index = pd.read_csv(StringIO(r.text), skipfooter=1, parse_dates=[0], index_col=0, engine='python')
        return df_relative_strength_index

    def standard_deviation(self, period=50):
        symbol = self.symbol
        group = self.group
        order = 'a'
        period = str(period)
        function = 'stddev'

        url = 'https://eodhistoricaldata.com/api/technical/' + symbol + '.' + group + '?order=' + order + '&fmt=csv' + '&function=' + function + '&period=' + period + '&api_token=' + api_token
        r = requests.get(url)
        df_standard_deviation = pd.read_csv(StringIO(r.text), skipfooter=1, parse_dates=[0], index_col=0, engine='python')
        return df_standard_deviation

    def stochastic_relative_strength_index(self, fast_kperiod=14, fast_dperiod=14):
        symbol = self.symbol
        group = self.group
        order = 'a'
        fast_kperiod = str(fast_kperiod)
        fast_dperiod = str(fast_dperiod)
        function = 'stochrsi'

        url = 'https://eodhistoricaldata.com/api/technical/' + symbol + '.' + group + '?order=' + order + '&fmt=csv' + '&function=' + function + '&fast_kperiod=' + fast_kperiod + '&fast_dperiod=' + fast_dperiod + '&api_token=' + api_token
        r = requests.get(url)
        df_stochastic_relative_strength_index = pd.read_csv(StringIO(r.text), skipfooter=1, parse_dates=[0], index_col=0, engine='python')
        return df_stochastic_relative_strength_index

    def slope_linear_regression(self, period=50):
        symbol = self.symbol
        group = self.group
        order = 'a'
        period = str(period)
        function = 'slope'

        url = 'https://eodhistoricaldata.com/api/technical/' + symbol + '.' + group + '?order=' + order + '&fmt=csv' + '&function=' + function + '&period=' + period + '&api_token=' + api_token
        r = requests.get(url)
        df_slope_linear_regression = pd.read_csv(StringIO(r.text), skipfooter=1, parse_dates=[0], index_col=0, engine='python')
        return df_slope_linear_regression

    def directional_movement_index(self, period=50):
        symbol = self.symbol
        group = self.group
        order = 'a'
        period = str(period)
        function = 'dmi'

        url = 'https://eodhistoricaldata.com/api/technical/' + symbol + '.' + group + '?order=' + order + '&fmt=csv' + '&function=' + function + '&period=' + period + '&api_token=' + api_token
        r = requests.get(url)
        df_directional_movement_index = pd.read_csv(StringIO(r.text), skipfooter=1, parse_dates=[0], index_col=0, engine='python')
        return df_directional_movement_index

    def average_directional_movement_index(self, period=50):
        symbol = self.symbol
        group = self.group
        order = 'a'
        period = str(period)
        function = 'adx'

        url = 'https://eodhistoricaldata.com/api/technical/' + symbol + '.' + group + '?order=' + order + '&fmt=csv' + '&function=' + function + '&period=' + period + '&api_token=' + api_token
        r = requests.get(url)
        df_average_directional_movement_index = pd.read_csv(StringIO(r.text), skipfooter=1, parse_dates=[0], index_col=0, engine='python')
        return df_average_directional_movement_index

    def moving_average_convergence_divergence(self, fast_period=12, slow_period=26, signal_period=9):
        symbol = self.symbol
        group = self.group
        order = 'a'
        fast_period = str(fast_period)
        slow_period = str(slow_period)
        signal_period = str(signal_period)
        function = 'macd'

        url = 'https://eodhistoricaldata.com/api/technical/' + symbol + '.' + group + '?order=' + order + '&fmt=csv' + '&function=' + function + '&fast_period=' + fast_period + '&slow_period=' + slow_period + '&signal_period=' + signal_period + '&api_token=' + api_token
        r = requests.get(url)
        df_moving_average_convergance_divergance = pd.read_csv(StringIO(r.text), skipfooter=1, parse_dates=[0], index_col=0, engine='python')
        return df_moving_average_convergance_divergance

    def average_true_range(self, period=50):
        symbol = self.symbol
        group = self.group
        order = 'a'
        period = str(period)
        function = 'atr'

        url = 'https://eodhistoricaldata.com/api/technical/' + symbol + '.' + group + '?order=' + order + '&fmt=csv' + '&function=' + function + '&period=' + period + '&api_token=' + api_token
        r = requests.get(url)
        df_average_true_range = pd.read_csv(StringIO(r.text), skipfooter=1, parse_dates=[0], index_col=0, engine='python')
        return df_average_true_range

    def commodity_channel_index(self, period=50):
        symbol = self.symbol
        group = self.group
        order = 'a'
        period = str(period)
        function = 'cci'

        url = 'https://eodhistoricaldata.com/api/technical/' + symbol + '.' + group + '?order=' + order + '&fmt=csv' + '&function=' + function + '&period=' + period + '&api_token=' + api_token
        r = requests.get(url)
        df_commodity_channel_index = pd.read_csv(StringIO(r.text), skipfooter=1, parse_dates=[0], index_col=0, engine='python')
        return df_commodity_channel_index

    def parabolic_sar(self, acceleration=0.02, maximum=0.20):
        symbol = self.symbol
        group = self.group
        order = 'a'
        acceleration = str(acceleration)
        maximum = str(maximum)
        function = 'sar'

        url = 'https://eodhistoricaldata.com/api/technical/' + symbol + '.' + group + '?order=' + order + '&fmt=csv' + '&function=' + function + '&acceleration=' + acceleration + '&maximum=' + maximum + '&api_token=' + api_token
        r = requests.get(url)
        df_parabolic_sar = pd.read_csv(StringIO(r.text), skipfooter=1, parse_dates=[0], index_col=0, engine='python')
        return df_parabolic_sar

    def bollinger_bands(self, period=50):
        symbol = self.symbol
        group = self.group
        order = 'a'
        period = str(period)
        function = 'bbands'

        url = 'https://eodhistoricaldata.com/api/technical/' + symbol + '.' + group + '?order=' + order + '&fmt=csv' + '&function=' + function + '&period=' + period + '&api_token=' + api_token
        r = requests.get(url)
        df_bollinger_bands = pd.read_csv(StringIO(r.text), skipfooter=1, parse_dates=[0], index_col=0, engine='python')
        return df_bollinger_bands

    def volume_weighted_average_price(self, period='d'):
        symbol = self.symbol
        group = self.group
        df = get_data(symbol, group, period)
        df['PV'] = ((df['Close'] + df['High'] + df['Low']) / 3) * df['Volume']
        df['PV_cumsum'] = df['PV'].cumsum()
        df['cumvol'] = df['Volume'].cumsum()
        df['VWAP'] = df['PV_cumsum'] / df['cumvol']
        df_volume_weighted_average_price = df[['VWAP']]
        return df_volume_weighted_average_price

    def on_balance_volume(self, period='d'):
        symbol = self.symbol
        group = self.group
        df = get_data(symbol, group, period)
        df = df.reset_index()
        for i in range(len(df)):
            if i == 0:
                df.loc[i, 'OBV'] = 0
                continue
            if df.loc[i, 'Close'] > df.loc[i - 1, 'Close']:
                df.loc[i, 'OBV'] = df.loc[i, 'Volume'] + df.loc[i - 1, 'OBV']
            elif df.loc[i, 'Close'] < df.loc[i - 1, 'Close']:
                df.loc[i, 'OBV'] = df.loc[i - 1, 'OBV'] - df.loc[i, 'Volume']
            else:
                df.loc[i, 'OBV'] = df.loc[i - 1, 'OBV']
        df = df.set_index(df['Date'])
        df_on_balance_volume = df[['OBV']]
        return df_on_balance_volume