import pandas as pd
import logging
import datetime

from ai.candlestick import CandleStick


logger = logging.getLogger(__name__)


def generate_csv(candle_sticks, csv_name='candle_sticks_data.csv'):
    """
    generates a CSV file for a particular candle sticks data.

    Args:
        candle_sticks (list[list[str]]]: candle sticks data.
        csv_name (str): name that this CSV file should be created with.

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


def load_csv(csv_name='candle_sticks_data.csv'):
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

    Examples:
        '17 Feb, 2021'
        '16 March, 2021'

    Returns:
        str: a custom datetime as a string.
    """
    return (datetime.datetime.now() - datetime.timedelta(days)).strftime('%d %b, %Y')
