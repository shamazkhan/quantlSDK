import logging
import requests
from IGServices.rest import IGService
import sys
from IGServices.config.trade_ig_config import config
from IGServices.IG_trade import IGtrade
from IGServices.rest import IGService
from IGServices.stream import IGStreamService
from IGServices.lightstreamer import LSClient, Subscription
from IG_trade import IGtrade
import pandas as pd


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


ig_service = IGService(
        config.username, config.password, config.api_key, config.acc_type, acc_id=config.acc_number
    )

ig_stream_service = IGStreamService(ig_service)
ig_stream_service.create_session()



subscription = Subscription(
        mode="MERGE",
        items=["MARKET:IX.D.FTSE.CFD.IP"],
        fields=["UPDATE_TIME", "BID", "OFFER"],
    )




df = pd.DataFrame(columns=["UPDATE_TIME", "BID", "OFFER"])

igt = IGtrade(config.username,config.password,config.api_key,config.acc_type,config.acc_number)
igt.create_session()

condition = False
dealid = 0
#OFFER = BUY
#BID = SELL

def on_item_update(item_update):
    global df
    global condition
    global dealid
    # print("price: %s " % item_update)
    print(item_update["values"])
    row = {'BID' : float(item_update['values']["BID"]),
           'OFFER' : float(item_update['values']["OFFER"]),
           'UPDATE_TIME' : item_update['values']["UPDATE_TIME"]}
    df = df.append(row,ignore_index=True)
    if len(df) > 5:
        df['rsi'] = computeRSI(df['OFFER'], 5)
    print(df)
    if (len(df) > 5) and (df.loc[(len(df)-1),'rsi'] < 35) and condition == False:
        op = igt.open_position_market('GBP','BUY','IX.D.FTSE.CFD.IP','2')
        dealid = op['dealId']
        condition = True
    if (len(df) > 5) and (df.loc[(len(df) - 1), 'rsi'] > 65) and condition == True:
        igt.close_position(dealid, 'SELL', '2', 'MARKET')
        print('closed')
        condition = False




# Adding the "on_item_update" function to Subscription
subscription.addlistener(on_item_update)

# Registering the Subscription
sub_key = ig_stream_service.ls_client.subscribe(subscription)

wait_for_input()

# Unsubscribing from Lightstreamer by using the subscription key
ig_stream_service.ls_client.unsubscribe(sub_key)

# Disconnecting
ig_stream_service.disconnect()