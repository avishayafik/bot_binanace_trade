import pandas as pd
import logging
import datetime

from ai.candlestick import CandleStick
from ai.binance_api import binance_client


logger = logging.getLogger(__name__)


def generate_csv(candle_sticks, csv_name):
    """
    generates a CSV file for a particular candle sticks data.

    Args:
        candle_sticks (list[list[str]]]: candle sticks data.
        csv_name (str): name that this CSV file should be created with (including absolute path).

    candle stick fields example:

        [
            [
                1499040000000,      // Open time
                "0.01634790",       // Open
                "0.80000000",       // High
                "0.01575800",       // Low
                "0.01577100",       // Close
                "148976.11427815",  // Volume
                1499644799999,      // Close time
                "2434.19055334",    // Quote asset volume
                308,                // Number of trades
                "1756.87402397",    // Taker buy base asset volume
                "28.46694368",      // Taker buy quote asset volume
                "17928899.62484339" // Ignore
            ]
        ]

    Returns:
        bool: True if CSV was created successfully, False otherwise.

    """
    file = None

    try:
        file = open(csv_name, "a")
        file.write("date,open,high,low,close,volume\n")

        for cstick in candle_sticks:
            candle_stick = CandleStick(
                timestamp=cstick[0],
                open=cstick[1],
                high=cstick[2],
                low=cstick[3],
                close=cstick[4],
                volume=cstick[5]
            )
            file.write(f"{candle_stick}\n")
    except Exception as e:
        logger.error(e)
        return False
    finally:
        file.close()
    return True


def read_csv(csv_name):
    """
    Loads a CSV file into a pandas DataFrame.

    Args:
        csv_name (str): CSV file to load.

    Returns:
        DataFrame: a pandas data frame object in case loaded successfully, None otherwise.
    """
    try:
        return pd.read_csv(filepath_or_buffer=csv_name)
    except Exception as e:
        logger.error(e)
        return None


def get_previous_date(days=30):
    """
    Returns the previous requested date in the following format.

    Args:
        days (int): number of days for a previous date since the current date.

    Examples:
        '17 Feb, 2021'
        '16 March, 2021'

    Returns:
        str: a custom datetime as a string.
    """
    return (datetime.datetime.now() - datetime.timedelta(days)).strftime('%d %b, %Y')


def construct_date_times(since_year=2016, since_month=1, since_day=1):
    """
    Constructs a data set of start & end date times of each month since the requested date until today.

    Args:
        since_year (int): since which year should the data set be configured.
        since_month (int): since which month in that year should the data set be configured.
        since_day (int): since which day in the specified month should the data set be configured

    Returns:
        list[tuple[str, str]]: matching start & end dates for each month since a given year, month and day.

    Example:

        construct_date_times(since_year=2020, since_month=4, since_day=14) will produce the following:

        [
            ('14 Apr, 2020', '30 Apr, 2020'),
            ('01 May, 2020', '31 May, 2020'),
            ('01 Jun, 2020', '30 Jun, 2020'),
            ('01 Jul, 2020', '31 Jul, 2020'),
            ('01 Aug, 2020', '31 Aug, 2020'),
            ('01 Sep, 2020', '30 Sep, 2020'),
            ('01 Oct, 2020', '31 Oct, 2020'),
            ('01 Nov, 2020', '30 Nov, 2020'),
            ('01 Dec, 2020', '31 Dec, 2020'),
            ('01 Jan, 2021', '31 Jan, 2021'),
            ('01 Feb, 2021', '28 Feb, 2021'),
            ('01 Mar, 2021', '31 Mar, 2021'),
            ('01 Apr, 2021', '01 Apr, 2021')
        ]
    """
    current_date = datetime.datetime.now()
    current_year = current_date.year

    if since_month > 12 or since_month < 1 or since_year > current_year or since_day < 1 or since_day > 31:
        return []

    month_with_31_days = 31
    month_with_28_days = 28
    month_with_30_days = 30

    last_day_of_each_month = {  # a dict that represents that last day in the month for every month in the year.
        1: month_with_31_days,
        2: month_with_28_days,
        3: month_with_31_days,
        4: month_with_30_days,
        5: month_with_31_days,
        6: month_with_30_days,
        7: month_with_31_days,
        8: month_with_31_days,
        9: month_with_30_days,
        10: month_with_31_days,
        11: month_with_30_days,
        12: month_with_31_days
    }

    start_end_month_dates = []

    to_month = 12

    for year in range(since_year, current_year + 1):
        if year == current_year:
            to_month = current_date.month

        for month in range(since_month, to_month + 1):
            last_day = current_date.day if month == to_month and year == current_year else last_day_of_each_month[month]

            start_month_date = datetime.date(year=year, month=month, day=since_day).strftime('%d %b, %Y')
            end_month_date = datetime.date(year=year, month=month, day=last_day).strftime('%d %b, %Y')

            start_end_month_dates.append((start_month_date, end_month_date, year))
            since_day = 1

        since_month = 1

    return start_end_month_dates


def generate_csvs(
    symbol, since_year=2016, since_month=1, since_day=1, interval=binance_client.client.KLINE_INTERVAL_1MINUTE
):

    date_times = construct_date_times(since_year=since_year, since_month=since_month, since_day=since_day)
    for start_date, end_date, year in date_times:

        csv_name = f"csvs/{year}/{interval}/{start_date}---{end_date}.csv"
        candle_sticks = binance_client.get_historical_klines(
            symbol=symbol, start_str=start_date, end_str=end_date, interval=interval
        )
        if not generate_csv(candle_sticks=candle_sticks, csv_name=csv_name):
            raise Exception(f"unable to generate CSV {csv_name}")


generate_csvs(symbol='ETHUSD', since_year=2020, since_month=3)
