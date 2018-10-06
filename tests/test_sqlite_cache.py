import unittest
import tempfile
import ecal
import pandas as pd


class TestSqliteCache(unittest.TestCase):

    def test_cached_dates_table_created(self):

        # GIVEN a database file
        f = tempfile.NamedTemporaryFile()

        # WHEN it's passed to SqliteCache's constructor
        cache = ecal.SqliteCache(f.name)

        # THEN the cached_dates table is created
        cursor = cache._conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        actual = cursor.fetchall()
        expected = ('cached_dates',)
        self.assertTrue(expected in actual)

        f.close()

    def test_announcements_table_created(self):

        # GIVEN a database file
        f = tempfile.NamedTemporaryFile()

        # WHEN it's passed to SqliteCache's constructor
        cache = ecal.SqliteCache(f.name)

        # THEN the announcements table is created
        cursor = cache._conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        actual = cursor.fetchall()
        expected = ('announcements',)
        self.assertTrue(expected in actual)

        f.close()

    def test_create_string_of_rows_for_VALUES_clause(self):

        # Given a SqliteCache and list of date strings
        f = tempfile.NamedTemporaryFile()
        cache = ecal.SqliteCache(f.name)
        date_list = ['2018-01-01', '2018-01-02', '2018-01-03', '2018-01-04', '2018-01-05']

        # When passed to _create_string_of_rows_for_VALUES_clause()
        actual = cache._create_string_of_rows_for_VALUES_clause(date_list)

        # Then it should be a string of tuples where each tuple only has one element and each is a row.
        # And also, these aren't python tuples with one element so they don't look like: (element,)
        expected = "('2018-01-01'),('2018-01-02'),('2018-01-03'),('2018-01-04'),('2018-01-05')"
        self.assertEqual(actual, expected)

    def test_check_for_missing_dates_that_are_not_in_the_cache(self):

        # GIVEN SqliteCache without any cached dates
        f = tempfile.NamedTemporaryFile()
        cache = ecal.SqliteCache(f.name)

        # When a the cache is asked to identify missing dates and the date is in the cache
        date_list = ['2018-01-01', '2018-01-02', '2018-01-03', '2018-01-04', '2018-01-05']
        actual = cache.check_for_missing_dates(date_list)

        # Then the cached dates are not returned
        expected = ['2018-01-01', '2018-01-02', '2018-01-03', '2018-01-04', '2018-01-05']
        self.assertListEqual(actual, expected)

        f.close()

    def test_check_for_missing_dates_that_are_in_the_cache(self):

        # GIVEN SqliteCache with a cached date
        f = tempfile.NamedTemporaryFile()
        cache = ecal.SqliteCache(f.name)
        cursor = cache._conn.cursor()
        cursor.execute("insert into cached_dates values('2018-01-03')")

        # When a the cache is asked to identify missing dates and the date is in the cache
        date_list = ['2018-01-01', '2018-01-02', '2018-01-03', '2018-01-04', '2018-01-05']
        actual = cache.check_for_missing_dates(date_list)

        # Then the cached dates are not returned
        expected = ['2018-01-01', '2018-01-02', '2018-01-04', '2018-01-05']
        self.assertListEqual(actual, expected)

        f.close()

    def test_add_missing_dates(self):

        # Given an SqliteCache
        f = tempfile.NamedTemporaryFile()
        cache = ecal.SqliteCache(f.name)

        # When some missing dates are added
        missing_dates = ['2018-01-01', '2018-01-02', '2018-01-03', '2018-01-04', '2018-01-05']
        cache.add(missing_dates, None)

        # Then they should be found in the cached_dates tables.
        expected = [('2018-01-01',), ('2018-01-02',), ('2018-01-03',), ('2018-01-04',), ('2018-01-05',)]
        c = cache._conn.cursor()
        c.execute('select * from cached_dates;')
        actual = c.fetchall()
        self.assertListEqual(actual, expected)

    def test_add_missing_dates_and_announcements(self):

        # Given an SqliteCache
        f = tempfile.NamedTemporaryFile()
        cache = ecal.SqliteCache(f.name)

        # When some missing dates and announcements are added
        missing_dates = ['2018-01-01', '2018-01-02', '2018-01-03', '2018-01-04', '2018-01-05']

        uncached_announcements = {'ticker': ['AEHR', 'ANGO', 'FC', 'LW', 'PKE', 'PSMT', 'RPM', 'SONC', 'WBA'],
                       'when': ['amc', 'bmo', 'amc', 'bmo', 'bmo', 'amc', 'bmo', 'amc', 'bmo'],
                       'date': ['2018-01-05', '2018-01-05', '2018-01-05', '2018-01-05', '2018-01-05', '2018-01-05',
                                '2018-01-05', '2018-01-05', '2018-01-05']}
        uncached_announcements_df = pd.DataFrame.from_dict(uncached_announcements)
        uncached_announcements_df = uncached_announcements_df.set_index('date')
        uncached_announcements_df = uncached_announcements_df[['ticker', 'when']]
        cache.add(missing_dates, uncached_announcements_df)

        # Then they should be found in the cached_dates tables.
        expected = [('2018-01-01',), ('2018-01-02',), ('2018-01-03',), ('2018-01-04',), ('2018-01-05',)]
        c = cache._conn.cursor()
        c.execute('select * from cached_dates;')
        actual = c.fetchall()
        self.assertListEqual(actual, expected)

        # And they should be found in the announcements table
        expected = [('2018-01-05', 'AEHR', 'amc'), ('2018-01-05', 'ANGO', 'bmo'), ('2018-01-05', 'FC', 'amc'),
                    ('2018-01-05', 'LW', 'bmo'), ('2018-01-05', 'PKE', 'bmo'), ('2018-01-05', 'PSMT', 'amc'),
                    ('2018-01-05', 'RPM', 'bmo'), ('2018-01-05', 'SONC', 'amc'), ('2018-01-05', 'WBA', 'bmo')]

        c = cache._conn.cursor()
        c.execute('select * from announcements;')
        actual = c.fetchall()
        self.assertListEqual(actual, expected)


