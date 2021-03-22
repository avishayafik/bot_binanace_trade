import pandas as pd
import matplotlib.pyplot as plt
from candlestick import CandleStick


class DataManager(object):

    def __init__(self, csv_name='test.csv', load_data=True):
        self._csv_name = csv_name  # csv_name
        self._data = self.load_csv() if load_data else None  # dataFrame of pandas

    @property
    def data(self):
        return self._data

    def mean(self, span, adjust, **params):

        return self._data.close.ewm(span=span, adjust=adjust, **params).mean()

    def get_column(self, attr):

        return self._data[attr]

    def set_column(self, attr, data):

        self._data[attr] = data

    @property
    def index(self):
        return self._data.index

    def generate_csv(self, klines_data, load_data=True):

        f = open(self._csv_name, "a")
        f.write("date,open,high,low,close,volume\n")

        for kline in klines_data:
            candle_stick = CandleStick(
                timestamp=kline[0],
                open=kline[1],
                high=kline[2],
                low=kline[3],
                close=kline[4],
                volume=kline[5]
            )
            f.write(f"{candle_stick}\n")
        f.close()

        if load_data:
            self._data = self.load_csv()

        short_ema = self.mean(span=20, adjust=False)
        middle_ema = self.mean(span=100, adjust=False)
        long_ema = self.mean(span=200, adjust=False)

        for attr, data in zip(['short', 'middle', 'long'], [short_ema, middle_ema, long_ema]):
            self.set_column(attr=attr, data=data)

    def load_csv(self):
        return pd.read_csv(self._csv_name)

    def to_graph(self):
        plt.style.use('fivethirtyeight')
        plt.figure(figsize=(15.2, 4.5))
        plt.title('close Price')
        plt.plot(self.get_column(attr='close'), label='close', alpha=0.5, LineWidth=1)
        plt.plot(self.mean(span=20, adjust=False), label='shortEma', color='purple', alpha=1, LineWidth=1)
        plt.plot(self.mean(span=100, adjust=False), label='middle', color='blue', alpha=1, LineWidth=1)
        plt.plot(self.mean(span=200, adjust=False), label='Long', color='black', alpha=1, LineWidth=1)
        plt.scatter(self.index, self.get_column(attr='buy'), color='green', marker='^', alpha=1)
        plt.scatter(self.index, self.get_column(attr='sell'), color='red', marker='v', alpha=1)
        plt.plot()
        plt.savefig('graph.png')
