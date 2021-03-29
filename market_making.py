from binance_client import binance_client

idx = 0
price_that_bought = 100000000000000.0
price_that_sold = 100000000000000.0
profit = 0
buy_flag = True

while True:

    price = float(binance_client.get_symbol_ticker(symbol='ETHUSD')['price'])

    if price > price_that_bought and not buy_flag:
        profit += price - price_that_bought
        print("sell sell sell!!")
        buy_flag = True
        price_that_sold = price
    if price < price_that_sold and buy_flag:
        print("buy buy buy!!")
        buy_flag = False
        price_that_bought = price

    idx += 1

    if idx % 100 == 0:
        print(f"price: {price}")
        print(f"profit: {profit}")
