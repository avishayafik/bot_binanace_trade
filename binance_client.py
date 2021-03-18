import os
import logging
from binance.client import Client


def catch_client_errors(func):
    """
    Decorator to catch all the exceptions that may occur to a client operation.
    """
    def wrapper(self, *args, **kwargs):
        """
        Tries to run the function that should interact with the binance API, in case it encounters any error,
        it will log the error and returns empty dict as an indication of failure.
        """
        try:
            return func(self, *args, **kwargs)
        except Exception as error:
            self._logger.error(error)
            return {}
    return wrapper


class BinanceApi(object):
    """
    This class is used to interact with the binance API.

    Documentation:
        https://github.com/binance/binance-spot-api-docs/blob/master/rest-api
    """
    def __init__(
        self,
        access_key=os.environ.get("BINANCE_ACCESS_KEY"),
        secret_key=os.environ.get("BINANCE_SECRET_KEY"),
        requests_params=None,
        tld='us',
        logger=logging.getLogger(__name__)
    ):
        self._client = Client(api_key=access_key, api_secret=secret_key, requests_params=requests_params, tld=tld)
        self._logger = logger

    @property
    @catch_client_errors
    def tickers(self):
        """
        Gets the latest price for all symbols.

        Returns:
            list[dict]: a list of symbols and their prices.

        Examples:
             [
                {
                    "symbol": "LTCBTC",
                    "price": "4.00000200"
                },
                {
                    "symbol": "ETHBTC",
                    "price": "0.07946600"
                }
            ]
        """
        return self._client.get_all_tickers()

    @catch_client_errors
    def withdraw(self, asset, address, amount, **withraw_params):
        """
        Submit a withdraw request.

        Args:
            asset (str): crypto currency type. e.g.: 'ETH'
            address (str): address to send to.
            amount (int): amount fee.

        Returns:
            dict: API response in case of a success, empty dict otherwise.
        """
        return self._client.withdraw(asset=asset, address=address, amount=amount, **withraw_params)

    @catch_client_errors
    def withdraw_history(self, **params):
        """
        Gets withdraw history of a single/all assets.

        Note: you can choose to look all the withdraw history of a specific asset such as ETHERIUM ('ETH').


        Part of the keyword arguments:

        Keyword Arguments:
            asset (str): indicate to show all the history withdraw of a specific currency such as 'ETH'

        Returns:
            dict[list]: withdraw history.


         {
                "withdrawList": [
                    {
                        "amount": 1,
                        "address": "0x6915f16f8791d0a1cc2bf47c13a6b2a92000504b",
                        "asset": "ETH",
                        "applyTime": 1508198532000
                        "status": 4
                    },
                    {
                        "amount": 0.005,
                        "address": "0x6915f16f8791d0a1cc2bf47c13a6b2a92000504b",
                        "txId": "0x80aaabed54bdab3f6de5868f89929a2371ad21d666f20f7393d1a3389fad95a1",
                        "asset": "ETH",
                        "applyTime": 1508198532000,
                        "status": 4
                    }
                ],
                "success": true
            }
        """
        return self._client.get_withdraw_history(**params)

    @catch_client_errors
    def create_order(self, **create_order_params):
        """
        Creates a new order.

        Keyword Arguments:
            https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#new-order--trade

        Returns:
            dict: a valid API response in case of success, empty dict in case of a failure.
        """
        return self._client.create_order(**create_order_params)

    @catch_client_errors
    def get_asset_balance(self, asset, **params):
        """
        Gets current asset balance.

        Args:
            asset (str): currency name. e.g.: 'ETH'

        Keyword Arguments:
            https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#account-information-user_data

        Returns:
            dict: a valid API response in case of success, empty dict otherwise.
        """
        asset_balance_response = self._client.get_asset_balance(asset=asset, **params)
        return asset_balance_response if asset_balance_response else {}

    @catch_client_errors
    def order_market_buy(self, symbol, quantity, **params):
        """
        Send in a new market buy order.

        Args:
            symbol (str): symbol name.
            quantity (int): the amount to buy.

        Returns:
            dict: a valid API response in case of success, empty dict otherwise.
        """
        return self._client.order_market_buy(symbol=symbol, quantity=quantity, **params)

    @catch_client_errors
    def order_market_sell(self,  symbol, quantity, **params):
        """
        Send in a new market sell order.

        Args:
            symbol (str): symbol name.
            quantity (int): the amount to sell.

        Returns:
            dict: a valid API response in case of success, empty dict otherwise.
        """
        return self._client.order_market_sell(symbol=symbol, quantity=quantity, **params)

    @catch_client_errors
    def get_klines(self, symbol, interval, **params):
        """
        Gets Kline/CandleSticks for a symbol.

        https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#klinecandlestick-data

        Args:
            symbol (str): symbol name.
            interval (str): interval time in minutes. e.g. '1m', '1h'

        Returns:
            dict: a valid API response in case of success, empty dict otherwise.
        """
        return self._client.get_klines(symbol=symbol, interval=interval, **params)

    @catch_client_errors
    def get_historical_klines(
        self,
        symbol,
        start_str=get_previous_date(),
        end_str=None,
        interval=Client.KLINE_INTERVAL_1MINUTE,
        limit=500
    ):
        """
        Get all the history of the candle sticks.

        Args:
            symbol (str): the symbol name.
            start_str (str): the start date time in UTC. e.g.: "1 March 2020"
            end_str (str): the end start date in UTC. e.g.: "15 March 2020", defaults to the current date.
            interval (str): candle stick interval. e.g.: "1m", "3m", "8h", "1w"
            limit (int): TODO: need to check the meaning of that?

        Returns:
            list: all candle sticks statistics in the last period of time. e.g.: last 30 days.
        """
        return self._client.get_historical_klines(
            symbol=symbol, interval=interval, start_str=start_str, end_str=end_str, limit=limit
        )

    @catch_client_errors
    def get_symbol_tickers(self):
        """
        Gets the symbol price for all available symbols.

        Returns:
            list[dict]: API response of all the symbols and their prices, empty dict in case of a failure.

        Examples:
             [
                {
                    "symbol": "LTCBTC",
                    "price": "4.00000200"
                },
                {
                    "symbol": "ETHBTC",
                    "price": "0.07946600"
                }
            ]
        """
        return self._client.get_symbol_ticker()

    @catch_client_errors
    def get_symbol_ticker(self, symbol):
        """
        Gets the symbol price of a specific symbol.

        Args:
            symbol (str): symbol name.

        Returns:
            dict: API response of the symbol price.

        Examples:
            {
                "symbol": "LTCBTC",
                "price": "4.00000200"
            }
        """
        return self._client.get_symbol_ticker(symbol=symbol)


binance_client = BinanceApi()
