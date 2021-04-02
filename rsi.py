import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import talib

plt.style.use('fivethirtyeight')
#df = pd.read_csv('results/test.csv')
df = pd.read_csv('results/last_2_month.csv')

df = df.set_index(pd.DatetimeIndex(df['date'].values))
# print(df)
shortEma = df.close.ewm(span=20, adjust=False).mean()
MiddleEma = df.close.ewm(span=50, adjust=False).mean()
longEma = df.close.ewm(span=100, adjust=False).mean()

close = df['close']
volume = df['volume']
high = df['high']
low = df['low']
rsi = talib.RSI(close, timeperiod=14)
adx = talib.ADX(high,low,close)
real = talib.OBV(close, volume)

exp1 = df.ewm(span=12, adjust=False).mean()
exp2 = df.ewm(span=26, adjust=False).mean()
macd = exp1-exp2
exp3 = macd.ewm(span=9, adjust=False).mean()



#df = df.set_index(pd.DatetimeIndex(df['date'].values))
df['short'] = shortEma
df['middle'] = MiddleEma
df['long'] = longEma
df['rsi'] = rsi
df['adx'] = adx
df['real'] = real
def buy_sell_function(data):
    position = False
    buy_list = []
    sell_list = []
    last_buy = None
    last_sell = None
    stop_lose = 0.01
    stop_up = 0.03
    print(data)
    for i in range(0, len(data)):
        #print(data['middle'][i])
        #print('!!!!!!!!!!!!!!')
        ### sell if we loose more than 1%
        #print(float(last_sell*stop_up)+float(last_sell))
        #print((float(last_buy*stop_lose)+float(last_buy)))

        #elif last_sell != None and position == True  and  last_sell*stop_lose > data['close'][i]:
        if data['rsi'][i] < 30 and position == False and df['adx'][i] > 25 :
            buy_list.append(data['close'][i])
            last_buy = data['close'][i]
            sell_list.append(np.nan)
            position = True

        elif data['rsi'][i] > 80  and position == True and df['adx'][i] > 25 :
            sell_list.append(data['close'][i])
            buy_list.append(np.nan)
            last_sell = data['close'][i]
            position = False
        ## stop lose
        elif last_buy != None and position == True and float(df['close'][i])+((float(df['close'][i]))*0.06) < last_buy:
            sell_list.append(data['close'][i])
            print(df['close'][i])
            buy_list.append(np.nan)
            last_sell = data['close'][i]
            position = False
        else:
            buy_list.append(np.nan)
            sell_list.append(np.nan)
    return (buy_list, sell_list)


df['buy'] = buy_sell_function(data=df)[0]
df['sell'] = buy_sell_function(data=df)[1]

plt.figure(figsize=(15.2, 4.5))
plt.title('close Price')
plt.plot(df['close'], label='close',alpha =0.5,LineWidth=1)
#plt.plot(shortEma, label='shortEma', color='purple',alpha =1,LineWidth=1)
#plt.plot(MiddleEma, label='middle', color='blue',alpha =1,LineWidth=1)
#plt.plot(longEma, label='Long', color='black',alpha =1,LineWidth=1)
#plt.plot(adx, label='adx', color='pink',alpha =1,LineWidth=1)
#plt.plot(df.index, macd, label='AMD MACD', color = '#EBD2BE')
#plt.plot(df.index, exp3, label='Signal Line', color='#E5A4CB')

plt.scatter(df.index,df['buy'],color='green',marker='^',alpha =1)
plt.scatter(df.index,df['sell'],color='red',marker='v',alpha =1)
#print(df)


plt.plot()
plt.savefig('moving_average.png')



buy = buy_sell_function(data=df)[0]
sell = buy_sell_function(data=df)[1]

def profit_calc(buy,sell):

    profit_list = []
    for i in range (len(buy)):
        if np.isnan(buy[i]) == False:
           profit_list.append(buy[i])
        if np.isnan(sell[i]) == False:
           profit_list.append(sell[i])
    print(profit_list)

    coin = 1
    position = False
#    first_price = {profit_list[0]: 1}
    for i in range (len(profit_list)):
        if i == 0:
            buy = profit_list[i]
            coin = 1
            position = True
        ### selll position
        elif position == True:
             sell = profit_list[i]
             money_in_hand = coin*sell
             print('sell: i have money in hand' ,str(money_in_hand))
             position = False
             coin = 0
        elif position == False:
            coin = money_in_hand / profit_list[i]
            print('buy: i have coin',str(coin))
            position = True
    print(len(profit_list))

profit_calc(buy,sell)