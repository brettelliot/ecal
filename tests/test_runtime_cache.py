import unittest
import ecal
import pandas as pd


class MockRuntimeCache(ecal.RuntimeCache):
    """Setup a mock cache with announcements on 1/4/2018 cached.
    """

    def __init__(self):
        # Seed the cache with some data
        sample_dict = {'ticker': ['CMC', 'LNDC', 'NEOG', 'RAD', 'RECN', 'UNF'],
                         'when': ['bmo', 'amc', 'bmo', 'amc', 'amc', 'bmo'],
                         'date': ['2018-01-04', '2018-01-04', '2018-01-04', '2018-01-04', '2018-01-04', '2018-01-04']}

        sample_df = pd.DataFrame.from_dict(sample_dict)
        sample_df = sample_df.set_index('date')
        sample_df = sample_df[['ticker', 'when']]
        self._cache_df = sample_df

        # Add the date to the cache set
        self._index_set = set(['2018-01-04'])


class TestRuntimeCache(unittest.TestCase):

    def setUp(self):
        self.cache = MockRuntimeCache()

    def test_check_for_missing_dates_returns_empty_datetimeindex_when_dates_are_not_missing(self):
        date_range = pd.date_range(start='2018-01-04', end='2018-01-04')
        date_list = date_range.strftime('%Y-%m-%d').tolist()
        actual = self.cache.check_for_missing_dates(date_list)
        assert(len(actual) == 0)

    def test_check_for_missing_dates_returns_datetimeindex_when_dates_are_missing(self):
        date_range = pd.date_range(start='2018-01-01', end='2018-01-10')
        date_list = date_range.strftime('%Y-%m-%d').tolist()
        actual = self.cache.check_for_missing_dates(date_list)
        assert(len(actual) == 9)

    def test_add(self):
        # Build a dataframe of uncached_announcements to add to the cache

        # to create the uncached_announcements df run this code to get a dict you can copy:
        #uncached_announcements['date'] = uncached_announcements.index
        #print(uncached_announcements.to_dict(orient='list'))
        uncached_announcements = {'ticker': ['AEHR', 'ANGO', 'FC', 'LW', 'PKE', 'PSMT', 'RPM', 'SONC', 'WBA'],
                       'when': ['amc', 'bmo', 'amc', 'bmo', 'bmo', 'amc', 'bmo', 'amc', 'bmo'],
                       'date': ['2018-01-05', '2018-01-05', '2018-01-05', '2018-01-05', '2018-01-05', '2018-01-05',
                                '2018-01-05', '2018-01-05', '2018-01-05']}
        uncached_announcements = pd.DataFrame.from_dict(uncached_announcements)
        uncached_announcements = uncached_announcements.set_index('date')
        uncached_announcements = uncached_announcements[['ticker', 'when']]

        dates_list = ['2018-01-05']
        assert('2018-01-05' not in self.cache._index_set)
        self.cache.add(dates_list, uncached_announcements)
        actual_df = self.cache._cache_df
        expected_df = {'date': ['2018-01-04', '2018-01-04', '2018-01-04', '2018-01-04', '2018-01-04', '2018-01-04',
                                '2018-01-05', '2018-01-05', '2018-01-05', '2018-01-05', '2018-01-05', '2018-01-05',
                                '2018-01-05', '2018-01-05', '2018-01-05'],
                       'ticker': ['CMC', 'LNDC', 'NEOG', 'RAD', 'RECN', 'UNF', 'AEHR', 'ANGO', 'FC', 'LW', 'PKE',
                                  'PSMT', 'RPM', 'SONC', 'WBA'],
                       'when': ['bmo', 'amc', 'bmo', 'amc', 'amc', 'bmo', 'amc', 'bmo', 'amc', 'bmo', 'bmo', 'amc',
                                'bmo', 'amc', 'bmo']}
        expected_df = pd.DataFrame.from_dict(expected_df)
        expected_df = expected_df.set_index('date')
        expected_df = expected_df[['ticker', 'when']]

        assert(actual_df.index.equals(expected_df.index))
        assert ('2018-01-05' in self.cache._index_set)
        assert(actual_df['ticker'].equals(expected_df['ticker']))
        assert(actual_df['when'].equals(expected_df['when']))


if __name__ == '__main__':
    unittest.main()
