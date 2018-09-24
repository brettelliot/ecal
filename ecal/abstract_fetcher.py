__all__ = [
    'AbstractFetcher'
]


class AbstractFetcher(object):
    """Abstract base class for earnings calendar fetchers."""

    def __init__(self):
        raise NotImplementedError('AbstractFetcher is an abstract base class')

    def fetch_calendar(self, start_date_str, end_date_str=None):
        """Implement this method! Your method should returns pandas DataFrame.

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
        raise NotImplementedError('AbstractFetcher is an abstract base class')
