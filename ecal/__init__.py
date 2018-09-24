"""A package for getting a US equity earnings announcement calendar.
"""
import pandas as pd
from .abstract_fetcher import AbstractFetcher
from .runtime_cache import AbstractCache
from .ecn_fetcher import ECNFetcher
from .runtime_cache import RuntimeCache

name = 'ecal'


"""
Module level global vars. 
"""
_default_fetcher = ECNFetcher()
_default_cache = RuntimeCache()

__all__ = [
    'get',
    'AbstractFetcher',
    'ECNFetcher',
    'AbstractCache',
    'RuntimeCache'
]


def get(start_date_str, end_date_str=None, fetcher=None, cache=_default_cache):
    """
    This function returns an earnings announcement calendar as a DataFrame.

    Args:
        fetcher (AbstractFetcher): The fetcher to use for downloading data.
          If no fetcher is provided, it will use ``_default_fetcher``.
          There must be a fetcher (you do want an earnings calendar don't you?).
        cache (AbstractCache): The cache to use for storing data.
          If no cache is provided, it will use ``_default_cache``.
          Pass ``None`` to not cache anything.
        start_date_str (str): The start date of the earnings calendar in
          the format ``YYYY-MM-DD``.
        end_date_str (str): The end date of the earnings calendar in
          the format ``YYYY-MM-DD``. If left out, we will fetch only the
          announcements for the start date.

    Returns:
        DataFrame: Returns a pandas DataFrame  indexed by 'date',
          that has columns: 'ticker', and 'when' and a row for each announcement:

            .. code-block:: python

                           ticker when
                date
                2018-01-04    CMC  bmo
                2018-01-04   LNDC  amc
                2018-01-04   NEOG  bmo
                2018-01-04    RAD  amc
                2018-01-04   RECN  amc
                2018-01-04    UNF  bmo

    """

    if end_date_str is None:
        end_date_str = start_date_str

    if fetcher is None:
        fetcher = _default_fetcher

    if cache is None:
        return fetcher.fetch_calendar(start_date_str, end_date_str)
    else:
        # Create a list of dates strings in the format: YYYY-MM-DD
        calendar_date_range = pd.date_range(start_date_str, end_date_str)
        date_list = calendar_date_range.strftime('%Y-%m-%d').tolist()

        # Check the cache to make sure it has all the announcements for the date range
        missing_dates = cache.check_for_missing_dates(date_list)

        col_names = ['date', 'ticker', 'when']
        uncached_announcements_df = pd.DataFrame(columns=col_names)
        uncached_announcements_df = uncached_announcements_df.set_index('date')

        for date_str in missing_dates:
            results_df = fetcher.fetch_calendar(date_str)
            uncached_announcements_df = pd.concat([uncached_announcements_df, results_df])

        cache.add(missing_dates, uncached_announcements_df)

        return cache.fetch_calendar(start_date_str, end_date_str)

