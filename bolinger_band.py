import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import talib
plt.style.use('fivethirtyeight')
#df = pd.read_csv('results/test.csv')
df = pd.read_csv('results/2021-03-23.csv')

period = 80
df['SMA'] = df['close'].rolling(window=period).mean()

df['STD'] = df['close'].rolling(window=period).std()

df['Upper'] = df['SMA'] + (df['STD']*2)
df['Lower'] =df['SMA'] - (df['STD']*2)

high = df['high']
low = df['low']
close = df['close']

colun_list = ['close','SMA','Upper','Lower']
df[colun_list].plot(figsize=(12.2,6.4))
plt.ylabel = ('price')
plt.savefig('bolinger.png')


def buy_sell_function(data):
    position = False
    buy_list = []
    sell_list = []
    print(data)
    for i in range(0, len(data)):
        #print(data['middle'][i])
        #print('!!!!!!!!!!!!!!')
        if data['close'][i] > data['Upper'][i]  and  position == False :
            sell_list.append(data['close'][i])
            buy_list.append(np.nan)
            position = True
        elif   data['close'][i] < data['Lower'][i] and position == True:
            buy_list.append(data['close'][i])
            sell_list.append(np.nan)
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
plt.scatter(df.index,df['buy'],color='green',marker='^',alpha =1)
plt.scatter(df.index,df['sell'],color='red',marker='v',alpha =1)
plt.savefig('bolinger_sell.png')

