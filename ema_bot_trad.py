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
fees = 0.001
coin = "eth"
in_position = False
RSI_PERIOD = 27
RSI_OVERSOLD_THRESHOLD = 30
RSI_OVERBOUGHT_THRESHOLD = 70
TRADE_SYMBOL = 'ADAUSD'
SOCKET = "wss://stream.binance.com:9443/ws/"+coin+"usdt@kline_1m"
TRADE_QUANTITY = 0.05
#closes = [1.26351, 1.26092, 1.26412, 1.26201, 1.25921, 1.24827, 1.25593, 1.24785, 1.25214, 1.25262, 9, 1.24547, 1.24265, 1.2376, 1.23423, 1.2304,1.26351, 1.26092, 1.26412, 1.26201, 1.25921, 1.24827, 1.25593, 1.24785, 1.25214, 1.25262, 1.2493, 1.24547, 1.24265, 1.2376, 1.23423, 9]
closes = [1551.73, 1555.81, 1559.51, 1557.95, 1557.59, 1557.69, 1553.3, 1553.49, 1556.33, 1558.45, 1558.65, 1558.83, 1559.17, 1558.52, 1560.25, 1560.11, 1560.93, 1561.46, 1561.0, 1563.16, 1562.83, 1561.9, 1561.4, 1560.67, 1560.49, 1561.45, 1560.46, 1560.53, 1559.57, 1559.13, 1559.06, 1559.16, 1560.3, 1560.48, 1563.99, 1564.3, 1563.02, 1561.88, 1562.0, 1562.26, 1560.6, 1562.51, 1564.01, 1564.33, 1561.29, 1557.56, 1557.63, 1555.22, 1552.42, 1557.17]
#closes = []
sell_price = None

### put your token key and secret in env var
#access_key = os.environ['access_key']
#secret_key = os.environ['secret_key']
buy_price = ""
close = []
#client = Client(access_key,secret_key,tld='us')
in_position = False


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
    global sell_price
    json_message =  json.loads(message)
    candle = json_message['k']['x']
    close = json_message['k']['c']

    #print(json_message)
    if candle == True:
        #print("candle price close was",close)
        closes.append(float(close))
        #logger.info("close price list: "+str(closes))
    if len(closes) > RSI_PERIOD:
        average_ema = ema()
        ema_long_avg = average_ema[0]
        ema_short_avg = average_ema[1]
        logger.info(" short avg is : " + str(ema_short_avg) + " long avg is: " + str(ema_long_avg))

        np_close = numpy.array(closes)
        rsi = talib.RSI(np_close,RSI_PERIOD)
        last_rsi = rsi[-1]
        closes = closes[-50:]
        print(closes)

        if ema_short_avg > ema_long_avg:
            if in_position:
                current_price = json_message['k']['c']
                ### check if current price is not below last buying
                #buy_price = 1462.94000000
                buy_price_fee = (float(buy_price) + (float(buy_price) * fees))
                logger.info("checking if current_price is higher than buying price , buying price: "+str(buy_price)+" buying price fees: "+str(buy_price_fee))
                if float(current_price) > float(buy_price_fee):
                    logger.info("sell !!!!!!!!!!!!!")
                    sell_price = current_price
                    logger.warning("last rsi is: "+str(last_rsi) +" selling price is: "+str(current_price))

                    order_sucesses = True
                    if order_sucesses:
                        Date = datetime.now()
                        wrightSellBuyCsv(Action="sell", coin=coin,Price=json_message['k']['c'], date=Date)
                        in_position = False        #print("rsi total vaule")
                else:
                    logger.info('no profit , wont sell')
            else:
                logger.info("not in position nothing to do")

        if float(ema_short_avg) < float(ema_long_avg):
            if in_position:
                logger.info("in position nothing to do , won't buy, last rsi: "+str(last_rsi)+" short avg is : "+str(ema_short_avg) +" long avg is: "+str(ema_long_avg) )
            else:
                if sell_price is None:
                    logger.info(last_rsi)
                    logger.warning("buying !!!!!!!!!!! "+"short avg is : "+str(ema_short_avg) +" long avg is: "+str(ema_long_avg))
                    logger.info("last rsi is: "+str(last_rsi)+" buying price is: "+str(json_message['k']['c']))
                    buy_price = json_message['k']['c']
                    order_sucesses = True
                    ## for real transaction run enable the below
                    #order_sucesses = order(TRADE_SYMBOL,SIDE_SELL,TRADE_QUANTITY)
                else:
                    logger.info("checking if last sell is higher than current buy")
                    if float(sell_price) > float(json_message['k']['c']):
                        logger.info(last_rsi)
                        logger.warning("buying !!!!!!!!!!! " + "short avg is : " + str(ema_short_avg) + " long avg is: " + str(ema_long_avg))
                        logger.info("last rsi is: " + str(last_rsi) + " buying price is: " + str(json_message['k']['c']))
                        buy_price = json_message['k']['c']
                        order_sucesses = True
                    else:
                        logger.warning("won't buy !!!!!!!!!!! sell price is lower than buy price " + "sell_price: " + str(sell_price) + " buy price: " + (json_message['k']['c']))

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