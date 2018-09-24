__all__ = [
    'AbstractCache'
]


class AbstractCache(object):
    """AbstractCache is the base class for all cache classes.

        Derived classes must implement:
            * check_for_missing_dates
            * add
            * fetch_calendar

    """

    def __init__(self):
        pass

    def check_for_missing_dates(self, date_list):
        """Look in the cache for dates and return the dates that aren't in the cache.

        Args:
            * date_list (list): The list of dates to check the cache for.

        Returns:
            * list: The dates from the date_list that are not in the cache.

        """
        raise NotImplementedError('AbstractCache is an abstract base class')

    def add(self, missing_dates, uncached_announcements):
        """Add the uncached announcements to the cache.

        Args:
            * missing_dates (list): The dates that were fetched and should be added to the cache index.
              Even dates that have no data should be added to the cache index so that if requested again, we return
              nothing for them without using the fetcher.
            * uncached_announcements (DataFrame): A DataFrame containing uncached announcements that should be added
              to the cache.
        """
        raise NotImplementedError('AbstractCache is an abstract base class')

    def fetch_calendar(self, start_date_str, end_date_str=None):
        """Returns the earnings calendar from the cache as a pandas DataFrame.

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
        raise NotImplementedError('AbstractCache is an abstract base class')
