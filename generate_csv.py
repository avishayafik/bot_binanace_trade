import logging ,sys
import numpy as np
from binance.client import Client
from binance_client import binance_client
from data_manager import DataManager
import os
import time
import datetime
from datetime import date


# logger = logging.getLogger('bot_trade' + ' ')
# logger.setLevel(logging.INFO)
# ch = logging.StreamHandler(sys.__stdout__)
# ch.setLevel(logging.INFO)
# formatter = logging.Formatter('%(asctime)s - %(lineno)s - %(levelname)s - %(message)s')
# ch.setFormatter(formatter)
# logger.addHandler(ch)
#
# print()
# access_key = os.environ['access_key']
# secret_key = os.environ['secret_key']
#
# print()
#
# data = []
# signals = []
#
#
#
# client = Client(api_key=access_key,api_secret=secret_key,tld='us')
# market = "ETHUSD"
# trade = "ETH"
# firstRun = True
# sell_price = None
# buy_price = ""
# close = []
#
# today = date.today()
#
# f = open("results/"+str(today)+".csv", "a")
#
# def generate_csv(market):
#     global f
#     f.write("date,open,high,low,close,volume\n")
#     data_list = []
#     data = client.get_klines(symbol=market, interval=Client.KLINE_INTERVAL_1MINUTE)
#     for i in range(1, len(data)):
#         timestamp = str(data[i][0])
#         open = data[i][1]
#         high = data[i][2]
#         low = data[i][3]
#         close = data[i][4]
#         volume = data[i][5]
#         trim_timestamp = timestamp[:-3]
#         Date = (datetime.datetime.utcfromtimestamp(int(trim_timestamp)).strftime('%Y-%m-%d %H:%M:%S'))
#         list_to_append = [int(i),Date,open,high,low,close,volume]
#         data_list.append(list_to_append)
#         print(str(Date)+","+str(open)+","+str(high)+","+str(low)+","+str(close)+","+str(volume)+"\n")
#         f.write(str(Date)+","+str(open)+","+str(high)+","+str(low)+","+str(close)+","+str(volume)+"\n")
#     f.close()
#
# generate_csv(market)


def buy_sell_function(data):
    position = False
    buy_list = []
    sell_list = []
    print(data)
    for i in range(0, len(data)):

        if data['middle'][i] < data['long'][i] and not position:
            buy_list.append(data['close'][i])
            sell_list.append(np.nan)
            position = True
        elif data['middle'][i] > data['long'][i] and position:
            sell_list.append(data['close'][i])
            buy_list.append(np.nan)
            position = False
        else:
            buy_list.append(np.nan)
            sell_list.append(np.nan)
    return buy_list, sell_list


def make_csv(symbol="ETHUSD"):

    klines_history = binance_client.get_historical_klines(symbol=symbol)
    data_manager = DataManager(load_data=False)
    data_manager.generate_csv(klines_data=klines_history)
    sell, buy = buy_sell_function(data=data_manager.data)
    data_manager.set_column(attr='buy', data=buy)
    data_manager.set_column(attr='sell', data=sell)
    data_manager.to_graph()


make_csv()