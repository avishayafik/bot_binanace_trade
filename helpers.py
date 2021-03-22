import datetime


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
