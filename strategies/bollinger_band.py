import matplotlib.pyplot as plt
import pandas as pd
import requests
from io import StringIO
import datetime
import numpy as np
import matplotlib.pyplot as plt
import statistics
import scipy.stats as stats
from data_api.get_data import GetData


def ts_to_date(ts) -> str:
    return datetime.datetime.fromtimestamp(ts / 1000.0).date()


def ts_to_datetime(ts) -> str:
    return datetime.datetime.fromtimestamp(ts / 1000.0)

class bband(object):
    def __init__(self, stock, group, period, start_date, end_date, amount):
        self.stock = stock
        self.group = group
        self.period = period
        self.start_date = start_date
        self.end_date = end_date
        self.amount = amount

    def first_page(self, setResultValues):
        stock = self.stock
        group = self.group
        period = self.period
        start_date = self.start_date
        end_date = self.end_date
        gd = GetData(stock, group)
        df = gd.get_data_strategy(period, start_date, end_date)
        df['sma'] = df['close'].rolling(21).mean()

        df['std'] = df['close'].rolling(21).std()

        df['up'] = df['sma'] + (df['std'] * 2)
        df['down'] = df['sma'] - (df['std'] * 2)

        for i in range(len(df)):
            if i == 0:
                continue
            if (df.loc[i, 'close'] - df.loc[i - 1, 'close']) >= 0:
                df.loc[i, 'max'] = df.loc[i, 'close'] - df.loc[i - 1, 'close']
            if (df.loc[i, 'close'] - df.loc[i - 1, 'close']) < 0:
                df.loc[i, 'min'] = abs(df.loc[i, 'close'] - df.loc[i - 1, 'close'])

        df = df.fillna(0)
        # df['cmo'] = (sum(df['max'] - df['min']) / sum(df['max'] + df['min'])) * 100
        df['r_max'] = df['max'].rolling(21).sum()
        df['r_min'] = df['min'].rolling(21).sum()
        df['cmo'] = ((df['r_max'] - df['r_min']) / (df['r_max'] + df['r_min'])) * 100
        # df.replace(0, np.nan, inplace=True)
        # print(df)

        # plt.plot(df['date'],df['cmo'])
        # plt.gcf().autofmt_xdate()
        # plt.title('Chande Momentum Oscillator')
        # plt.show()

        plt.title(stock.upper() + ' Bollinger Bands')
        plt.xlabel('Days')
        plt.ylabel('Closing Prices')
        plt.plot(df['date'],df['close'], label='Closing Prices')
        plt.plot(df['date'],df['up'], label='Bollinger Up', c='g')
        plt.plot(df['date'],df['sma'])
        plt.plot(df['date'],df['down'], label='Bollinger Down', c='r')
        plt.gcf().autofmt_xdate()
        plt.legend()
        plt.show()
        if (setResultValues):
            df1 = pd.DataFrame(columns=['open', 'close', 'direction'])
            close_index = [0]
            for i in range(len(df)):
                if i in close_index:
                    continue
                if (df.loc[i - 1, 'close'] < df.loc[i - 1, 'down'] and df.loc[i, 'close'] > df.loc[i, 'down']):
                    for j in range(i, len(df)):
                        close_index.append(j + 1)
                        if (df.loc[j, 'close'] > df.loc[j, 'up']):
                            df1 = df1.append({'open': i, 'close': j + 1, 'direction': 'long'}, ignore_index=True)
                            break
            # print(df1)
            self.df1 = df1
            self.df_stock = df
            gd = GetData('SPY', 'US')
            self.df_spy = gd.get_data_strategy(period, start_date, end_date)

        values_returned = True

        return df, values_returned

    def get_results(self):
        df1 = self.df1
        df_stock = self.df_stock
        df_spy = self.df_spy
        initial_amount = self.amount
        amount = self.amount

        df_final_stock = pd.DataFrame()
        if len(df1) == 0:
            print('Condition not satisfied')
        else:
            for i in range(len(df1)):
                df_temp = df_stock[df1.loc[i, 'open']:df1.loc[i, 'close']]
                df_temp['return'] = np.log(df_temp['close'] / df_temp['close'].shift(1))
                df_temp['creturn'] = df_temp['return'].cumsum().apply(np.exp) * amount
                df_final_stock = df_final_stock.append(df_temp)
                # print(df_temp)
                df_final_stock = df_final_stock.reset_index()
                df_final_stock.pop('index')
                amount = df_final_stock.loc[(len(df_final_stock) - 1), 'creturn']
                df1.loc[i, 'stock_amount'] = amount

        amount = self.amount
        df_final_spy = pd.DataFrame()
        if len(df1) == 0:
            print('Condition not satisfied')
        else:
            for i in range(len(df1)):
                df_temp = df_spy[df1.loc[i, 'open']:df1.loc[i, 'close']]
                df_temp['return'] = np.log(df_temp['close'] / df_temp['close'].shift(1))
                df_temp['creturn'] = df_temp['return'].cumsum().apply(np.exp) * amount
                df_final_spy = df_final_spy.append(df_temp)
                # print(df_temp)
                df_final_spy = df_final_spy.reset_index()
                df_final_spy.pop('index')
                amount = df_final_spy.loc[(len(df_final_spy) - 1), 'creturn']
                # amount_list.append(amount)
                df1.loc[i, 'spy_amount'] = amount

        # print('Net Profit = ')
        final_amount = (df1.loc[(len(df1) - 1), 'stock_amount'])
        net_profit = (((final_amount - initial_amount) / initial_amount) * 100)
        # print(net_profit)

        # print('No of trades executed = ')
        # print(len(df1))

        amt = initial_amount
        if len(df1) == 0:
            print('No trades executed')
        else:
            for i in range(len(df1)):
                df1.loc[i, '% return'] = (((df1.loc[i, 'stock_amount'] - amt) / amt) * 100)
                amt = df1.loc[i, 'stock_amount']

        # print('Most profitable trade = ')
        # print(max(df1['% return']))

        # print('No of winning trades = ' )
        # print((len(df1[df1['% return'] > 0])))

        # print('No of losing trades = ')
        # print((len(df1[df1['% return'] < 0])))

        # print('Strategy return % = ')
        # print(net_profit)

        # print('Strategy return $ = ')
        # print((final_amount - initial_amount))

        df1['diff'] = df1['close'] - df1['open']

        # print('Average bars in a trade = ')
        # print(df1['diff'].mean())

        for i in range(len(df1)):
            if df1.loc[i, '% return'] > 0:
                df1.loc[i, 'result'] = 'PROFIT'
            else:
                df1.loc[i, 'result'] = 'LOSS'

        #PLOTS
        #Bollinger bands
        plt.xlabel('Days')
        plt.ylabel('Closing Prices')
        plt.plot(df_stock['date'], df_stock['close'], label='Closing Prices')
        plt.plot(df_stock['date'], df_stock['up'], label='Bollinger Up', c='g')
        plt.plot(df_stock['date'], df_stock['sma'])
        plt.plot(df_stock['date'], df_stock['down'], label='Bollinger Down', c='r')
        plt.gcf().autofmt_xdate()
        plt.legend()
        plt.show()

        #Stock vs SPY return
        plt.plot(df_final_stock['date'],df_final_stock['creturn'])
        plt.plot(df_final_spy['date'],df_final_spy['creturn'])
        plt.gcf().autofmt_xdate()
        plt.show()

        #Momentum Oscillator

        plt.plot(df_stock['date'], df_stock['cmo'])
        plt.gcf().autofmt_xdate()
        plt.title('Chande Momentum Oscillator')
        plt.show()

        return_difference = df_final_stock['return'] - df_final_spy['return']
        volatility = return_difference.std() * np.sqrt(len(df_stock))
        information_ratio = return_difference.mean() / volatility
        # print('Information ratio', information_ratio)

        ss = df_final_stock['return'] / df_final_spy['return']
        svs = ss.mean()
        # print('strategy vs spy returns', svs)

        df_stock['return'] = np.log(df_stock['close'] / df_stock['close'].shift(1))
        data = df_stock['return'].tail(len(df_stock) - 1)
        ci = stats.t.interval(alpha=0.95, df=len(data) - 1, loc=np.mean(data), scale=stats.sem(data))
        # print('confidence interval', ci)

        cagr = pow((final_amount / amount), (len(df_stock) / 252)) - 1
        # print('CAGR', cagr)

        # Profit/Loss per trade as bar graph
        # df1['% return']

        textual_data = {
            "netProfit": net_profit,
            "noOfTrades": len(df1),
            "mostProfitableTrades": max(df1['% return']),
            "noOfWinningTrades": (len(df1[df1['% return'] > 0])),
            "noOfLosingTrades": (len(df1[df1['% return'] < 0])),
            "strategyReturn%": net_profit,
            "strategyReturn$": (final_amount - initial_amount),
            "avgBars": df1['diff'].mean(),
            "finalAmount": final_amount,
            "informationRatio": information_ratio,
            "svs": svs,
            "confidenceInterval": ci,
            "cagr": cagr
        }

        values_returned = True

        return df_stock, df_final_stock, df_final_spy, values_returned, textual_data, df1

a = bband('AAPL', 'US', 'd', '2021-01-01','2022-04-14',10000)
a.first_page(True)
a.get_results()
print(a.get_results())