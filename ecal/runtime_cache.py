import pandas as pd
from .abstract_cache import AbstractCache

__all__ = [
    'RuntimeCache'
]


class RuntimeCache(AbstractCache):
    """RuntimeCache keeps a DataFrame of earnings announcements so that repeated calls to ecal.get are fast.

        Attributes:
            _cache_df (DataFrame): DataFrame storing all the earnings announcements that have been fetched.
            _index_set (set): Set containing all the dates that earnings announcements have been fetched for.
              This set is needed because some days don't have earnings announcements (so they won't appear in
              the cache.
    """

    def __init__(self):

        # Create the cache
        col_names = ['date', 'ticker', 'when']
        self._cache_df = pd.DataFrame(columns=col_names)
        self._cache_df = self._cache_df.set_index('date')

        # And the cache index
        self._index_set = set()

    def check_for_missing_dates(self, date_list):
        """Look in the cache for dates and return the dates that aren't in the cache.

        Args:
            date_list (list): The list of dates to check the cache for.

        Returns:
            list: The dates from the date_list that are not in the cache.

        """
        missing_dates_list = []
        for date in date_list:
            if date not in self._index_set:
                missing_dates_list.append(date)

        return missing_dates_list

    def add(self, missing_dates, uncached_announcements):
        """Add the uncached announcements to the cache.

        Args:
            missing_dates (list): The dates that were fetched and should be added to the cache index.
              Even dates that have no data should be added to the cache index so that if requested again, we return
              nothing for them without using the fetcher.
            uncached_announcements (DataFrame): A Dataframe containing uncached announcements that should be added
              to the cache.
        """
        # add all the dates to the index set
        self._index_set |= set(missing_dates)

        # add the uncached announcements to the cache
        self._cache_df = pd.concat([self._cache_df, uncached_announcements])

    def fetch_calendar(self, start_date_str, end_date_str=None):
        """Returns the earnings calendar from the cache as a pandas DataFrame.

        Args:
            start_date_str (str): The start date of the earnings calendar in
              the format ``YYYY-MM-DD``.
            end_date_str (str): The end date of the earnings calendar in
              the format ``YYYY-MM-DD``. If left out, we will fetch only the
              announcements for the start date.

        Returns:
            DataFrame: Returns a pandas DataFrame indexed by 'date',
              that has columns: 'ticker', and 'when'
              and a row for each announcement.
        """
        if end_date_str is None:
            end_date_str = start_date_str

        return self._cache_df[start_date_str:end_date_str]
