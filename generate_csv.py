import logging ,sys
from binance.client import Client
import os
import time
import datetime
from datetime import date


logger = logging.getLogger('bot_trade' + ' ')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.__stdout__)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(lineno)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)



access_key = os.environ['access_key']
secret_key = os.environ['secret_key']

data = []
signals = []



client = Client(access_key,secret_key,tld='us')
market = "ETHUSD"
trade = "ETH"
firstRun = True
sell_price = None
buy_price = ""
close = []

today = date.today()

f = open("results/"+str(today), "a")

def generate_csv(market):
    global f
    f.write("date,open,high,low,close,volume\n")
    data_list = []
    data = client.get_klines(symbol=market, interval=Client.KLINE_INTERVAL_1MINUTE)
    for i in range(1, len(data)):
        timestamp = str(data[i][0])
        open = data[i][1]
        high = data[i][2]
        low = data[i][3]
        close = data[i][4]
        volume = data[i][5]
        trim_timestamp = timestamp[:-3]
        Date = (datetime.datetime.utcfromtimestamp(int(trim_timestamp)).strftime('%Y-%m-%d %H:%M:%S'))
        list_to_append = [int(i),Date,open,high,low,close,volume]
        data_list.append(list_to_append)
        print(str(Date)+","+str(open)+","+str(high)+","+str(low)+","+str(close)+","+str(volume)+"\n")
        f.write(str(Date)+","+str(open)+","+str(high)+","+str(low)+","+str(close)+","+str(volume)+"\n")
    f.close()

generate_csv(market)

