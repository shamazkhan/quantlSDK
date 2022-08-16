import logging
import requests
from IGServices.rest import IGService
import sys
from IGServices.config.trade_ig_config import config
from IGServices.IG_trade import IGtrade
from IGServices.rest import IGService
from IGServices.stream import IGStreamService
from IGServices.lightstreamer import LSClient, Subscription
import pandas as pd
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# if you need to cache to DB your requests
from datetime import timedelta
import requests_cache

sys.path.append('/...IGServices/config')


def computeRSI(data, time_window):
    diff = data.diff(1).dropna()  # diff in one field(one day)

    # this preservers dimensions off diff values
    up_chg = 0 * diff
    down_chg = 0 * diff

    # up change is equal to the positive difference, otherwise equal to zero
    up_chg[diff > 0] = diff[diff > 0]

    # down change is equal to negative deifference, otherwise equal to zero
    down_chg[diff < 0] = diff[diff < 0]

    # check pandas documentation for ewm
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.ewm.html
    # values are related to exponential decay
    # we set com=time_window-1 so we get decay alpha=1/time_window
    up_chg_avg = up_chg.ewm(com=time_window - 1, min_periods=time_window).mean()
    down_chg_avg = down_chg.ewm(com=time_window - 1, min_periods=time_window).mean()

    rs = abs(up_chg_avg / down_chg_avg)
    rsi = 100 - 100 / (1 + rs)
    return rsi

def wait_for_input():
    input("{0:-^80}\n".format("HIT CR TO UNSUBSCRIBE AND DISCONNECT FROM \
                                  LIGHTSTREAMER"))


class config(object):
    username = "shamazkhan86"
    password = "A330airbus?"
    api_key = "3dffcba4bd2570d8b36c204ecc92554cc1d11eb4"
    acc_type = "DEMO"  # LIVE / DEMO
    acc_number = "Z3TMKL"


logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)


class Trade_rsi():
    def __init__(self,username,password,api_key,acc_type,acc_id):
        self.username = username
        self.password = password
        self.api_key = api_key
        self.acc_type = acc_type
        self.acc_id = acc_id
        self.df = pd.DataFrame(columns=["UPDATE_TIME", "BID", "OFFER"])
        self.condition = False
        self.dealid = 0
        self.df_summary = pd.DataFrame(columns=['UPDATE_TIME','OPEN','CLOSE'])
        self.df_pl = pd.DataFrame(columns=['pl', 'returns'])

    def initialize(self,lower = 30,upper = 70,period = 14):
        self.upper = upper
        self.lower = lower
        self.period = period

        ig_service = IGService(self.username, self.password, self.api_key, self.acc_type,
                               acc_id=self.acc_id)
        self.ig_service = ig_service
        ig_stream_service = IGStreamService(ig_service)
        ig_stream_service.create_session()

        igtrade = IGtrade(self.username, self.password, self.api_key, self.acc_type,
                               acc_number=self.acc_id)
        igtrade.create_session()

        self.igtrade = igtrade

        self.ig_seream_service = ig_stream_service


    def Subscription(self,symbol,size,currency):

        igtrade = self.igtrade
        self.size = size
        self.currency = currency
        epic = igtrade.get_epic(symbol)

        subscription = Subscription(
            mode="MERGE",
            items=["MARKET:" + epic],
            fields=["UPDATE_TIME", "BID", "OFFER"]
        )

        self.subscription = subscription
        self.epic = epic


    def on_item_update(self,item_update):
        df = self.df
        condition = self.condition
        dealid = self.dealid
        igtrade = self.igtrade
        epic = self.epic
        size = self.size
        currency = self.currency
        upper = self.upper
        lower = self.lower
        period = self.period
        df_summary = self.df_summary
        # print("price: %s " % item_update)
        print(item_update["values"])
        row = {'BID': float(item_update['values']["BID"]),
               'OFFER': float(item_update['values']["OFFER"]),
               'UPDATE_TIME': item_update['values']["UPDATE_TIME"]}
        df = df.append(row, ignore_index=True)
        if len(df) > period:
            df['rsi'] = computeRSI(df['BID'], period)
        print(df)
        if (len(df) > period) and (df.loc[(len(df) - 1), 'rsi'] < lower) and condition == False:
            op = igtrade.open_position_market(currency, 'BUY', epic, size)
            dealid = op['dealId']
            df_summary.loc[(len(df_summary)),'OPEN'] = df.loc[(len(df) - 1), 'BID']
            condition = True
            self.buy_price = df.loc[(len(df) - 1), 'OFFER']

        if condition == True:
            buy_price = self.buy_price
            df_pl = self.df_pl
            pl = (row['BID'] - buy_price) * 10 * int(size)
            returns = ((row['BID'] - buy_price) / buy_price) * 100
            pl_row = {'UPDATE_TIME' : row['UPDATE_TIME'],
                      'pl' : pl,
                      'returns' : returns}
            df_pl = df_pl.append(pl_row, ignore_index = True)
            self.df_pl = df_pl
            print(df_pl)

        if (len(df) > period) and (df.loc[(len(df) - 1), 'rsi'] > upper) and condition == True:
            igtrade.close_position(dealid, 'SELL', size, 'MARKET')
            print('closed')
            df_summary.loc[(len(df_summary) - 1), 'CLOSE'] = df.loc[(len(df) - 1), 'BID']
            condition = False
        self.df = df
        self.condition = condition
        self.dealid = dealid
        self.df_summary = df_summary


    def execute(self):
        subscription = self.subscription
        ig_stream_service = self.ig_seream_service

        subscription.addlistener(self.on_item_update)

        # Registering the Subscription
        sub_key = ig_stream_service.ls_client.subscribe(subscription)

        '''wait_for_input()

        # Unsubscribing from Lightstreamer by using the subscription key
        ig_stream_service.ls_client.unsubscribe(sub_key)'''

    def stop(self):
        ig_stream_service = self.ig_seream_service
        sub_key = 'cr'
        ig_stream_service.ls_client.unsubscribe(sub_key)
        # Disconnecting
        ig_stream_service.disconnect()

    def get_summary(self):
        df_summary = self.df_summary
        size = self.size
        df_summary['RETURN'] = ((df_summary['CLOSE'] - df_summary['OPEN']) / df_summary['OPEN']) * 100
        df_summary['PL'] = (df_summary['CLOSE'] - df_summary['OPEN']) * 10 * int(size)

        return df_summary




tr = Trade_rsi(
        config.username, config.password, config.api_key, config.acc_type, acc_id=config.acc_number
    )

tr.initialize(lower=30,upper=70,period=14)
tr.Subscription(symbol='FTSE', size = '2', currency= 'GBP')
tr.execute()
time.sleep(15)
tr.stop()

result = tr.get_summary()
print(result)


