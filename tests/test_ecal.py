import unittest
import ecal
import pandas as pd


class MockFetcher(ecal.AbstractFetcher):

    def __init__(self):
        sample_dict = {'ticker': ['CMC', 'LNDC', 'NEOG', 'RAD', 'RECN', 'UNF'],
                         'when': ['bmo', 'amc', 'bmo', 'amc', 'amc', 'bmo'],
                         'date': ['2018-01-04', '2018-01-04', '2018-01-04', '2018-01-04', '2018-01-04', '2018-01-04']}

        sample_df = pd.DataFrame.from_dict(sample_dict)
        sample_df = sample_df.set_index('date')
        sample_df = sample_df[['ticker', 'when']]
        self.calendar_df = sample_df

    def fetch_calendar(self, start_date_str, end_date_str=None):
        return self.calendar_df


class TestEcalGet(unittest.TestCase):
    """
    This class uses MockFetcherMock to ecal.get
    """

    def setUp(self):
        self.mock_fetcher = MockFetcher()

    def test_fetch_calendar(self):

        actual_df = ecal.get('2018-01-04', fetcher=self.mock_fetcher)

        expected_dict = {'ticker': ['CMC', 'LNDC', 'NEOG', 'RAD', 'RECN', 'UNF'],
                         'when': ['bmo', 'amc', 'bmo', 'amc', 'amc', 'bmo'],
                         'date': ['2018-01-04', '2018-01-04', '2018-01-04', '2018-01-04', '2018-01-04', '2018-01-04']}

        expected_df = pd.DataFrame.from_dict(expected_dict)
        expected_df = expected_df.set_index('date')
        expected_df = expected_df[['ticker', 'when']]

        assert(actual_df.index.equals(expected_df.index))
        assert(actual_df['ticker'].equals(expected_df['ticker']))
        assert(actual_df['when'].equals(expected_df['when']))


if __name__ == '__main__':
    unittest.main()
