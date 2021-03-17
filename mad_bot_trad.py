import websocket,json ,numpy
import pprint
#config,pprit
import talib
import logging ,sys
from binance.enums import *
from binance.client import Client
import os
#from datetime import datetime
import time
import datetime
import CoreFunctions as cf


#Client = Client(api_key, api_secret)


#ts = time.time()
#sttime = datetime.now().strftime('%Y%m%d_%H:%M:%S - ')


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

## percentage fee
low_profit_precentage = 0.003
fees = 0.001
coin = "eth"
in_position = False
RSI_PERIOD = 27
RSI_OVERSOLD_THRESHOLD = 30
RSI_OVERBOUGHT_THRESHOLD = 70




client = Client(access_key,secret_key,tld='us')
#closes = []
market = "ETHUSD"
trade = "ETH"
#currentBtc = cf.getCoinBalance(client, 'btc')
#print(currentBtc)
#currentBnb = cf.getCoinBalance(client, 'bnb')
#print(currentBnb)
##currentTRX = cf.getCoinBalance(client, 'TRX')
#print(currentTRX)
firstRun = True
sell_price = None
buy_price = ""
close = []
#client = Client(access_key,secret_key,tld='us')
in_position = False


#candles = client.get_klines(symbol=market, interval=Client.KLINE_INTERVAL_1MINUTE)


#print(candles)

def ema():
  ema_short_list = closes[-13:]
  ema_long_list =  closes[-26:]
  ema_short = sum(ema_short_list) / len(ema_short_list)
  ema_long = sum(ema_long_list) / len(ema_long_list)
  #logger.info(str(ema_long)+"  "+str(ema_short))
  return ema_long,ema_short



def order(side,symble,quantity,order_type):
    try:
        print("sending order")
        order = Client.create_order(symble=symble,side=side,type=order_type,quantity=quantity)
        print(order)
    except Exception as e:
        return False
    return True


def wrightSellBuyCsv(Action,coin,Price,date):
    sttime = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    logger.info("writing to csv")
    f = open("results/results.csv", "a")
    f.write(Action+","+coin+","+Price+","+sttime+"\n")
    f.close()


#candles = client.get_klines(symbol=market, interval=Client.KLINE_INTERVAL_5MINUTE)


#########
#f = open("results/results1111.csv", "a")
f = open("results/test.csv", "a")

#data_list = [["
# "]]
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

    #print(Date)
    #print(data[i])
    #return data_list

#print(data_list)
data_list

#with open('test.csv', 'w', newline='') as file:
#    writer = csv.writer(file)
#    writer.writerows(data_list)
##############




while(True):
        current_price = client.get_symbol_ticker(symbol=market)
        logger.info("current price :"+current_price['price'])

        candles = client.get_klines(symbol=market, interval=Client.KLINE_INTERVAL_1MINUTE)
        # print(candles)
        #prevTime = datetime.datetime.fromtimestamp(candles[498][0] / 1e3)
        #print(prevTime)
        ### if first run append list
        if firstRun == True:
            prevTime = datetime.datetime.fromtimestamp(candles[498][0] / 1e3)
            firstRun = False
            for i in range(499):
                #print(candles[i])
                data.append(candles[i])
        else:
            currTime = datetime.datetime.fromtimestamp(candles[498][0] / 1e3)
            if prevTime != currTime:
                data.append(candles[498])
                prevTime = currTime
                makeTrade = True
        #print(data)
        signals = cf.makeTrainingData(data)
        #print(signals)
        #logger.info(signals)

        time.sleep(2)
        current = signals[len(signals) - 1]
        logger.info("current signal : "+str(current))
        signals = cf.makeTrainingData(data)
        if current[0] > current[1]:
             #logger.info("checking signal: "+ str(current))
             if in_position:
                logger.warning("sell !!!!!!!!!!!!!")
# order_sucesses = order(TRADE_SYMBOL,SIDE_SELL,TRADE_QUANTITY)
                # order_sucesses = order(TRADE_SYMBOL,SIDE_SELL,TRADE_QUANTITY)
                order_sucesses = True
                if order_sucesses:
                    Date = datetime.datetime.now()
                    wrightSellBuyCsv(Action="sell", coin=coin, Price=current_price['price'], date=Date)
                    in_position = False  # print("rsi total vaule")
             else:
                 logger.info("not in position to sell")
### for debug see last signals
        #for i in signals:
        #    print(i)
        if current[0] < current[1]:
            if in_position:
                logger.info("in position nothing to do , won't buy, last signal: "+str(current))
            else:
                logger.warning("buying !!!!!!!!!!!")
                logger.info("last signal is: "+str(current)+" buying price is: "+str(current_price['price']))
                order_sucesses = True
                ## for real transaction run enable the below
                #order_sucesses = order(TRADE_SYMBOL,SIDE_SELL,TRADE_QUANTITY)
                if order_sucesses:
                    in_position = True
                    #from datetime import datetime
                    Date = datetime.datetime.now()
                    write = wrightSellBuyCsv(Action="buy", coin=coin, Price=current_price['price'], date=Date)
