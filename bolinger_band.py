import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import talib
plt.style.use('fivethirtyeight')
#df = pd.read_csv('results/test.csv')
df = pd.read_csv('results/last_2_month.csv')

period = 80
df = df.set_index(pd.DatetimeIndex(df['date'].values))
df['SMA'] = df['close'].rolling(window=period).mean()

df['STD'] = df['close'].rolling(window=period).std()

df['Upper'] = df['SMA'] + (df['STD']*3)
df['Lower'] =df['SMA'] - (df['STD']*3)


high = df['high']
low = df['low']
close = df['close']
rsi = talib.RSI(close, timeperiod=14)
df['rsi'] = rsi
adx = talib.ADX(high,low,close,timeperiod=140)
df['adx'] = adx

colun_list = ['close','SMA','Upper','Lower']
df[colun_list].plot(figsize=(12.2,6.4))
plt.ylabel = ('price')
plt.savefig('bolinger.png')


def buy_sell_function(data):
    position = False
    buy_list = []
    sell_list = []
    last_buy = None
    print(data)
    for i in range(0, len(data)):
        #print(data['middle'][i])
        #print('!!!!!!!!!!!!!!')
        if data['close'][i] > data['Upper'][i] and position == True  and df['rsi'][i] > 80:
            sell_list.append(data['close'][i])
            buy_list.append(np.nan)
            position = False
        elif data['close'][i] < data['Lower'][i] and position == False  and df['adx'][i] < 30:
            buy_list.append(data['close'][i])
            last_buy = data['close'][i]
            sell_list.append(np.nan)
            position = True
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


plt.figure(figsize=(15.2, 4.5))
plt.title('close Price')
plt.plot(df['close'], label='close',alpha =0.5,LineWidth=1)
plt.scatter(df.index,df['buy'],color='green',marker='^',alpha =1)
plt.scatter(df.index,df['sell'],color='red',marker='v',alpha =1)
plt.savefig('bolinger_sell.png')



plt.figure(figsize=(15.2, 4.5))
plt.title('close Price')
plt.plot(df['adx'], label='close',alpha =0.5,LineWidth=1)


plt.plot()
plt.savefig('adx_boll.png')