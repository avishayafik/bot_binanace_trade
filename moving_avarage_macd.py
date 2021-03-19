import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')
#df = pd.read_csv('results/test.csv')
df = pd.read_csv('results/2021-03-19.csv')

#df = df.set_index(pd.DatetimeIndex(df['date'].values))
# print(df)
shortEma = df.close.ewm(span=6000, adjust=False).mean()
MiddleEma = df.close.ewm(span=50, adjust=False).mean()
longEma = df.close.ewm(span=13000, adjust=False).mean()
macd = shortEma - longEma
signal = macd.ewm(span=9, adjust=False).mean()

df['short'] = shortEma
df['middle'] = MiddleEma
df['long'] = longEma
df['macd'] = macd
df['signal'] = signal

def buy_sell_function(data):
    position = False
    buy_list = []
    sell_list = []
    print('data lengh', str(len(data)))
    #print(data)
    for i in range(0, len(data)):
        #print(data['middle'][i])
        #print('!!!!!!!!!!!!!!')
        #print(data['macd'][i], data['signal'][i])
        if data['macd'][i] > data['signal'][i]  and position == False :
            buy_list.append(data['close'][i])
            sell_list.append(np.nan)
            position = True
        elif data['macd'][i] < data['signal'][i] and position == True:
            sell_list.append(data['close'][i])
            buy_list.append(np.nan)
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
#plt.plot(df['macd'] ,color='purple',alpha =1,LineWidth=1)
#plt.plot(df['signal'] ,color='blue',alpha =1,LineWidth=1)
#plt.plot(shortEma, label='shortEma', color='purple',alpha =1,LineWidth=1)
#plt.plot(MiddleEma, label='middle', color='blue',alpha =1,LineWidth=1)
#plt.plot(longEma, label='Long', color='black',alpha =1,LineWidth=1)
plt.scatter(df.index,df['buy'],color='green',marker='^',alpha =1)
plt.scatter(df.index,df['sell'],color='red',marker='v',alpha =1)
#print(df)


plt.plot()
plt.savefig('test.png')



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

    in_hand = None
    first_price = {profit_list[0]: 1}
    for i in range (len(profit_list)):
        #print(profit_list[i])
        if i != 0:
            a = (i-1)
            if in_hand != None:
               profit_price = (in_hand/profit_list[i])
               print("profit price: ",str(profit_price))
               sell_profit = profit_price * in_hand
               print("sel profit",str(sell_profit))
               in_hand = profit * profit_list[i]
               profit = (in_hand / profit_list[i])
            else:
                print(profit_list[i],profit_list[a])
                profit = (profit_list[i]/profit_list[a])
                print(profit)
                ## selling
                in_hand = profit*profit_list[a]
                print('in hand:' ,str(in_hand))
    print(len(profit_list))

profit_calc(buy,sell)