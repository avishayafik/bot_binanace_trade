import datetime


class CandleStick(object):
    """
    A class that represents the main fields of a candle stick.
    """
    def __init__(self, timestamp, open, high, low, close, volume):
        self._date = (datetime.datetime.utcfromtimestamp(int(str(timestamp)[:-3])).strftime('%Y-%m-%d %H:%M:%S'))
        self._open = open
        self._high = high
        self._low = low
        self._close = close
        self._volume = volume

    @property
    def date(self):
        """
        Returns candle stick date value.
        """
        return self._date

    @property
    def high(self):
        return self._high

    @property
    def open(self):
        """
        Returns candle stick open value.
        """
        return self._open

    @property
    def low(self):
        """
        Returns candle stick low value.
        """
        return self._low

    @property
    def close(self):
        """
        Returns candle stick close value.
        """
        return self._close

    @property
    def volume(self):
        """
        Returns candle stick volume value.
        """
        return self._volume

    def is_close_lower_than_open(self):
        return float(self.close) < float(self.open)

    def __repr__(self):
        return f"{self.date}, {self.open}, {self.high}, {self.low}, {self.close}, {self.volume}"

    def __str__(self):
        return f"{self.date}, {self.open}, {self.high}, {self.low}, {self.close}, {self.volume}"
