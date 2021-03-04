import websocket,json ,numpy
import pprint
#config,pprit
import talib
import logging ,sys
from binance.enums import *
from binance.client import Client
import os
from datetime import datetime
import time
import pandas as pd
import numpy as np

#ts = time.time()
sttime = datetime.now().strftime('%Y%m%d_%H:%M:%S - ')


logger = logging.getLogger('bot_trade' + ' ')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.__stdout__)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(lineno)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


## percentage fee
fees = 0.01
coin = "eth"
in_position = False
RSI_PERIOD = 14
RSI_OVERSOLD_THRESHOLD = 30
RSI_OVERBOUGHT_THRESHOLD = 70
TRADE_SYMBOL = 'ADAUSD'
SOCKET = "wss://stream.binance.com:9443/ws/"+coin+"usdt@kline_1m"
TRADE_QUANTITY = 0.05
#closes = [1.26351, 1.26092, 1.26412, 1.26201, 1.25921, 1.24827, 1.25593, 1.24785, 1.25214, 1.25262, 1.2493, 1.24547, 1.24265, 1.2376, 1.23423, 1.2304]
closes = []

### put your token key and secret in env var
access_key = os.environ['access_key']
secret_key = os.environ['secret_key']
buy_price = ""
close = []
high_list = []
low_list = []
client = Client(access_key,secret_key,tld='us')
in_position = False


def ema():
  ema_short_list = closes[-40:]
  ema_long_list =  closes[-20:]
  ema_short = sum(ema_short_list) / len(ema_short_list)
  ema_long_list = sum(ema_long_list) / len(ema_long_list)
  print(ema_long_list,ema_short)
  return ema_long_list,ema_short





def supres(low, high, min_touches=2, stat_likeness_percent=1.5, bounce_percent=5):
    """Support and Resistance Testing
    Identifies support and resistance levels of provided price action data.
    Args:
        low(pandas.Series): A pandas Series of lows from price action data.
        high(pandas.Series): A pandas Series of highs from price action data.
        min_touches(int): Minimum # of touches for established S&R.
        stat_likeness_percent(int/float): Acceptable margin of error for level.
        bounce_percent(int/float): Percent of price action for established bounce.

    ** Note **
        If you want to calculate support and resistance without regard for
        candle shadows, pass close values for both low and high.
    Returns:
        sup(float): Established level of support or None (if no level)
        res(float): Established level of resistance or None (if no level)
    """
    # Setting default values for support and resistance to None
    sup = None
    res = None

    # Identifying local high and local low
    maxima = high.max()
    minima = low.min()

    #print(maxima,minima)
    # Calculating distance between max and min (total price movement)
    move_range = maxima - minima

    # Calculating bounce distance and allowable margin of error for likeness
    move_allowance = move_range * (stat_likeness_percent / 100)
    bounce_distance = move_range * (bounce_percent / 100)
    print(move_allowance,bounce_distance)
    # Test resistance by iterating through data to check for touches delimited by bounces
    touchdown = 0
    awaiting_bounce = False
    for x in range(0, len(high)):
        #print(maxima,high[x])
        #print(maxima - high[x])
        #print("!!!!!!!!!!!")
        #print(move_allowance)
        if abs(maxima - high[x]) < move_allowance and not awaiting_bounce:
            touchdown = touchdown + 1
            awaiting_bounce = True
        elif abs(maxima - high[x]) > bounce_distance:
            awaiting_bounce = False
    if touchdown >= min_touches:
        res = maxima

    # Test support by iterating through data to check for touches delimited by bounces
    touchdown = 0
    awaiting_bounce = False
    for x in range(0, len(low)):
        if abs(low[x] - minima) < move_allowance and not awaiting_bounce:
            touchdown = touchdown + 1
            awaiting_bounce = True
        elif abs(low[x] - minima) > bounce_distance:
            awaiting_bounce = False
    if touchdown >= min_touches:
        sup = minima
    return sup, res



#support =  supres(low=low, high=high, min_touches=2, stat_likeness_percent=1.5, bounce_percent=5)




def order(side,symble,quantity,order_type):
    try:
        print("sending order")
        order = Client.create_order(symble=symble,side=side,type=order_type,quantity=quantity)
        print(order)
    except Exception as e:
        return False
    return True


def wrightSellBuyCsv(Action,coin,Price,date):
    sttime = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    logger.info("writing to csv")
    f = open("results/results.csv", "a")
    f.write(Action+","+coin+","+Price+","+sttime+"\n")
    f.close()


def on_close(ws):
    print("closed connection")


def on_open(ws,message):
    print("open connection")
    #print(message)

def on_message(ws,message):
    global closes
    global in_position
    global buy_price
    global high_list
    global low_list
    json_message =  json.loads(message)
    candle = json_message['k']['x']
    close = json_message['k']['c']

    high = json_message['k']['h']
    low = json_message['k']['l']

    #print(high,low)
    if candle == True:
        #print("candle price close was",close)
        closes.append(float(close))
        high_list.append(float(high))
        low_list.append(float(low))
        #logger.info("close price list: "+str(closes))
        logger.info("close price list: " + str(closes))
    if len(closes) > RSI_PERIOD:

     #######
        data_low = np.array(low_list)
        low = pd.Series(data_low)
        data_high = np.array(high_list)
        high = pd.Series(data_high)
        support = supres(low=low, high=high, min_touches=2, stat_likeness_percent=1.5, bounce_percent=5)
        print("support !!!! :  ")
        print(support)
     #######
        np_close = numpy.array(closes)
        rsi = talib.RSI(np_close,RSI_PERIOD)
        last_rsi = rsi[-1]
        closes = closes[-100:]
        high_list = high_list[-100:]
        low_list = low_list[-100:]
        print(closes)
        if last_rsi > RSI_OVERBOUGHT_THRESHOLD:
            if in_position:
                current_price = json_message['k']['c']
                ### check if current price is not below last buying
                buy_price_fee = float(buy_price) + (float(buy_price) * fees)
                logger.info("checking if current_price is higher than buying price , buying price:"+str(buy_price)+" buying price + fees: "+str(buy_price_fee))
                if current_price > buy_price_fee:
                    logger.warning("sell !!!!!!!!!!!!!")
                    logger.warning("last rsi is: ",str(last_rsi) , "selling price is: ",str(current_price))
                    ## for real transaction run enable the below
                    #order_sucesses = order(TRADE_SYMBOL,SIDE_SELL,TRADE_QUANTITY)
                    order_sucesses = True
                    if order_sucesses:
                        Date = datetime.now()
                        wrightSellBuyCsv(Action="sell", coin=coin,Price=json_message['k']['c'], date=Date)
                        in_position = False        #print("rsi total vaule")

            #else:
            #    logger.info("not in position nothing to do")

        if last_rsi < RSI_OVERSOLD_THRESHOLD:
            if in_position:
                logger.info("in position nothing to do , won't buy, last rsi: "+str(last_rsi))
            else:
                logger.info(last_rsi)
                logger.warning("buying !!!!!!!!!!!")
                logger.info("last rsi is: "+str(last_rsi)+" buying price is: "+str(json_message['k']['c']))
                buy_price = json_message['k']['c']
                order_sucesses = True
                ## for real transaction run enable the below
                #order_sucesses = order(TRADE_SYMBOL,SIDE_SELL,TRADE_QUANTITY)
                if order_sucesses:
                    in_position = True
                    Date = datetime.now()

                    write = wrightSellBuyCsv(Action="buy", coin=coin, Price=json_message['k']['c'], date=Date)
                    #print(write)
    #else:
    #    logger.info("starting to collect candle stick , only after 15 candle sticks , bot will start trading now it's: "+str(len(closes)))



dateTimeObj = datetime.now()
#print(dateTimeObj)

ws = websocket.WebSocketApp(SOCKET,on_open=on_open,on_message=on_message,on_close=on_close)
ws.run_forever()


ws = websocket.WebSocketApp(SOCKET)

print(ws)