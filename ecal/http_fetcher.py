import time
import datetime
import requests
import pandas as pd
from .abstract_fetcher import AbstractFetcher

__all__ = [
    'HttpFetcher'
]


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

    def fetch_calendar(self, start_date_str, end_date_str=None):
        """Returns the earnings calendar as a pandas DataFrame.

        Args:
            * start_date_str (str): The start date of the earnings calendar in
              the format ``YYYY-MM-DD``.
            * end_date_str (str): The end date of the earnings calendar in
              the format ``YYYY-MM-DD``. If left out, we will fetch only the
              announcements for the start date.

        Returns:
            * DataFrame: Returns a pandas DataFrame indexed by 'date',
              that has columns: 'ticker', 'when', and 'market_cap_mm'
              and a row for each announcement.
        """

        if end_date_str is None:
            end_date_str = start_date_str

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
