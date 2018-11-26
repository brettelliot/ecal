import unittest
import ecal
import pandas as pd


class TestHttpFetcher(unittest.TestCase):
    """
    This class actually makes calls to the API using the EarningsFetcherHttp
    """

    def setUp(self):
        self.fetcher = ecal.ECNFetcher()

    def test_earnings_announcements_for_date(self):

        actual = self.fetcher._earnings_announcements_for_date('2017-03-30')

        self.assertEqual(actual[0]['ticker'], 'AEHR')
        self.assertEqual(actual[0]['when'], 'amc')

        self.assertEqual(actual[1]['ticker'], 'ANGO')
        self.assertEqual(actual[1]['when'], 'bmo')

        self.assertEqual(actual[2]['ticker'], 'BSET')
        self.assertEqual(actual[2]['when'], '--')

        self.assertEqual(actual[3]['ticker'], 'FC')
        self.assertEqual(actual[3]['when'], 'amc')

        self.assertEqual(actual[4]['ticker'], 'LNN')
        self.assertEqual(actual[4]['when'], 'bmo')

        self.assertEqual(actual[5]['ticker'], 'SAIC')
        self.assertEqual(actual[5]['when'], 'bmo')

        self.assertEqual(actual[6]['ticker'], 'TITN')
        self.assertEqual(actual[6]['when'], 'bmo')

    def test_earnings_announcements_for_date_rate_limit_test(self):
        """
        Call the function twice. It should rate limit but still work.
        :return:
        """
        actual1 = self.fetcher._earnings_announcements_for_date('2017-03-30')
        actual2 = self.fetcher._earnings_announcements_for_date('2017-03-30')

        self.assertEqual(actual1[0]['ticker'], 'AEHR')
        self.assertEqual(actual1[0]['when'], 'amc')

        self.assertEqual(actual1[1]['ticker'], 'ANGO')
        self.assertEqual(actual1[1]['when'], 'bmo')

        self.assertEqual(actual1[2]['ticker'], 'BSET')
        self.assertEqual(actual1[2]['when'], '--')

        self.assertEqual(actual1[3]['ticker'], 'FC')
        self.assertEqual(actual1[3]['when'], 'amc')

        self.assertEqual(actual1[4]['ticker'], 'LNN')
        self.assertEqual(actual1[4]['when'], 'bmo')

        self.assertEqual(actual1[5]['ticker'], 'SAIC')
        self.assertEqual(actual1[5]['when'], 'bmo')

        self.assertEqual(actual1[6]['ticker'], 'TITN')
        self.assertEqual(actual1[6]['when'], 'bmo')

        self.assertEqual(actual2[0]['ticker'], 'AEHR')
        self.assertEqual(actual2[0]['when'], 'amc')

        self.assertEqual(actual2[1]['ticker'], 'ANGO')
        self.assertEqual(actual2[1]['when'], 'bmo')

        self.assertEqual(actual2[2]['ticker'], 'BSET')
        self.assertEqual(actual2[2]['when'], '--')

        self.assertEqual(actual2[3]['ticker'], 'FC')
        self.assertEqual(actual2[3]['when'], 'amc')

        self.assertEqual(actual2[4]['ticker'], 'LNN')
        self.assertEqual(actual2[4]['when'], 'bmo')

        self.assertEqual(actual2[5]['ticker'], 'SAIC')
        self.assertEqual(actual2[5]['when'], 'bmo')

        self.assertEqual(actual2[6]['ticker'], 'TITN')
        self.assertEqual(actual2[6]['when'], 'bmo')

    def test_fetch_calendar_for_singe_date(self):
        expected_dict = {'ticker': ['CMC', 'LNDC', 'NEOG', 'RAD', 'RECN', 'UNF'],
                         'when': ['bmo', 'amc', 'bmo', 'amc', 'amc', 'bmo'],
                         'date': ['2018-01-03', '2018-01-03', '2018-01-03', '2018-01-03', '2018-01-03', '2018-01-03']}

        expected_df = pd.DataFrame.from_dict(expected_dict)
        expected_df = expected_df.set_index('date')
        expected_df = expected_df[['ticker', 'when']]

        actual_df = self.fetcher.fetch_calendar('2018-01-03')

        assert(actual_df.index.equals(expected_df.index))
        assert(actual_df['ticker'].equals(expected_df['ticker']))
        assert(actual_df['when'].equals(expected_df['when']))

    def test_fetch_calendar_for_date_range(self):
        expected_dict = {'ticker': ['CMC', 'LNDC', 'NEOG', 'RAD', 'RECN', 'UNF'],
                         'when': ['bmo', 'amc', 'bmo', 'amc', 'amc', 'bmo'],
                         'date': ['2018-01-03', '2018-01-03', '2018-01-03', '2018-01-03', '2018-01-03', '2018-01-03']}

        expected_df = pd.DataFrame.from_dict(expected_dict)
        expected_df = expected_df.set_index('date')
        expected_df = expected_df[['ticker', 'when']]

        actual_df = self.fetcher.fetch_calendar('2018-01-03', '2018-01-03')
        assert(actual_df.index.equals(expected_df.index))
        assert(actual_df['ticker'].equals(expected_df['ticker']))
        assert(actual_df['when'].equals(expected_df['when']))


if __name__ == '__main__':
    unittest.main()
