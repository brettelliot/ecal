"""A package for getting a US equity earnings announcement calendar.

.. moduleauthor:: Brett Elliot <brett@theelliots.net>

"""
import pandas as pd
import time
import datetime
import requests

__all__ = [
    'get',
    'AbstractFetcher',
    'HttpFetcher'
]


def get(start_date_str, end_date_str=None, fetcher=None, cache=None):
    """
    This function returns an earnings announcement calendar as a DataFrame.

    Args:
        * fetcher (AbstractFetcher): The fetcher to use for downloading data.
          By default it will use ecal.DEFAULT_FETCHER.
        * cache (AbstractCache): The cache to use for storing data.
          By default ecal will not cache.
        * start_date_str (str): The start date of the earnings calendar in
          the format ``YYYY-MM-DD``.
        * end_date_str (str): The end date of the earnings calendar in
          the format ``YYYY-MM-DD``. If left out, we will fetch only the
          announcements for the start date.

    Returns:
        * DataFrame: Returns a pandas DataFrame  indexed by 'date',
          that has columns: 'ticker', 'when', and 'market_cap_mm'
          and a row for each announcement:

            .. code-block:: python

                           ticker when  market_cap_mm
                date
                2018-01-04    CMC  bmo           2475
                2018-01-04   LNDC  amc            362
                2018-01-04   NEOG  bmo           5002
                2018-01-04    RAD  amc           1376
                2018-01-04   RECN  amc            551
                2018-01-04    UNF  bmo           3567

    """

    if end_date_str is None:
        end_date_str = start_date_str

    if fetcher is None:
        fetcher = DEFAULT_FETCHER

    if cache is None:
        return fetcher.fetch_calendar(start_date_str, end_date_str)
    else:
        # Get a DatetimeIndex
        calendar_date_range = pd.date_range(start_date_str, end_date_str)

        # Check the cache to make sure it has all the announcements for the date range
        missing_dates = cache.check_for_missing_dates(calendar_date_range)

        if missing_dates:
            fetcher.fetch_calendar(start_date_str, end_date_str, cache)

        return cache.get(start_date_str, end_date_str)


class AbstractFetcher(object):
    """Abstract base class for earnings calendar fetchers."""

    def __init__(self):
        raise NotImplementedError('AbstractFetcher is an abstract base class')

    def fetch_calendar(self, start_date_str, end_date_str):
        """Implement this method! Your method should returns pandas DataFrame.

        Args:
            * start_date_str (str): The start date of the earnings calendar in
              the format ``YYYY-MM-DD``.
            * end_date_str (str): The end date of the earnings calendar in
              the format ``YYYY-MM-DD``.

        Returns:
            * DataFrame: Returns a pandas DataFrame indexed by 'date',
              that has columns: 'ticker', 'when', and 'market_cap_mm'
              and a row for each announcement.
        """
        raise NotImplementedError('AbstractFetcher is an abstract base class')


class HttpFetcher(AbstractFetcher):
    """This class fetches earnings announcements from ``api.earningscalendar.net``.

    One of the main things HttpFetcher does is prevent calling the API too many times to prevent throttling.
    """

    def __init__(self, rate_limit=1.5):
        """
        Args:

            * rate_limit (float): The time (in seconds) to wait in between calls to the API.
        """
        self._rate_limit = rate_limit
        self._last_call_time = time.time()

    def fetch_calendar(self, start_date_str, end_date_str):
        """Returns the earnings calendar as a pandas DataFrame.

        Args:
            * start_date_str (str): The start date of the earnings calendar in
              the format ``YYYY-MM-DD``.
            * end_date_str (str): The end date of the earnings calendar in
              the format ``YYYY-MM-DD``.

        Returns:
            * DataFrame: Returns a pandas DataFrame indexed by 'date',
              that has columns: 'ticker', 'when', and 'market_cap_mm'
              and a row for each announcement.
        """
        announcements_list = []
        date_range = pd.date_range(start_date_str, end_date_str)

        for single_date in date_range:
            date_str = single_date.strftime("%Y-%m-%d")
            results = self._earnings_announcements_for_date(date_str)
            for result in results:
                row = [date_str, result['ticker'], result['when'], result['market_cap_mm']]
                announcements_list.append(row)

        df = pd.DataFrame(announcements_list, columns=['date', 'ticker', 'when', 'market_cap_mm'])
        df.set_index('date', inplace=True)
        return df

    def _earnings_announcements_for_date(self, date_str):
        """
        Return a list of earnings announcements for a date.

        Args:
            * date_str (str): A date in the format ``YYYY-MM-DD``

        Returns:
            * list: A list of earnings announcements for a date.

                .. code-block:: python

                        [
                            {
                                'ticker': 'AEHR',
                                'market_cap_mm': 54,
                                'when': 'amc'
                            },
                            ...
                        ]

                *ticker*
                    is the ticker symbol on NYSE or NASDAQ.

                *market_cap_mm*
                    is the market cap of the company at the time of the API call (not at the time of the \
                    announcement).

                *when*
                    can be: ``bmo`` which means *before market open*, ``amc`` which means *after market close* or \
                    ``--`` which means *no time reported*.

        """
        # Be sure not to exceed the api throttling of 1 call per second
        current_time = time.time()
        if current_time <= self._last_call_time + 1:
            time.sleep(self._rate_limit)

        formatted_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y%m%d')
        payload = {'date': formatted_date}
        self._last_call_time = time.time()
        r = requests.get('https://api.earningscalendar.net/', params=payload)

        try:
            raw_announcements_list = r.json()
            transformed_announcements_list = self._transform_cap_mm_to_market_cap_mm(raw_announcements_list)
            return transformed_announcements_list
        except ValueError as e:
            print(e)
            return None

    def _transform_cap_mm_to_market_cap_mm(self, announcements_list):
        for announcement in announcements_list:
            # The cap_mm is a string with commas like: '2,329'
            # Get rid of the commas then convert to int.
            announcement['market_cap_mm'] = int(announcement['cap_mm'].replace(',', ''))
            announcement.pop('cap_mm', None)
        return announcements_list


DEFAULT_FETCHER = HttpFetcher()
#DEFAULT_CACHE = SqliteCache()