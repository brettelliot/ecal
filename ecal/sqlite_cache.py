import pandas as pd
from .abstract_cache import AbstractCache
import sqlite3

__all__ = [
    'SqliteCache'
]

"""
Testing queries is faster using the command line. To do that:

Start the sqlite3 shell:
$ sqlite3

Create the cached_dates table:
sqlite> CREATE TABLE IF NOT EXISTS cached_dates (date text NOT NULL PRIMARY KEY);

Insert something into that table:
sqlite> insert into cached_dates values('2018-01-03'); 

Check if a query works. For example, this takes a list of dates and returns the ones that aren't in the cached_dates
table:

sqlite>
SELECT *
FROM
(
    VALUES('2018-01-01'),('2018-01-02'),('2018-01-03'),('2018-01-04'),('2018-01-05')
)
EXCEPT
SELECT date FROM cached_dates;


Check adding to the cached_dates:
sqlite>
REPLACE INTO cached_dates (date) VALUES ('2018-01-01'),('2018-01-02'),('2018-01-03'),('2018-01-04'),('2018-01-05');

"""


class SqliteCache(AbstractCache):
    """SqliteCache provides persistent storage for earnings announcements so repeated calls to ``ecal.get()`` are fast.

        Attributes:
            _conn (Connection):
                The sqlite3 database connection.

    """

    def __init__(self, db_file_path='ecal.db'):
        """"

            Args:
                db_file_path (str):
                    A string containing the file path to the sqlite database file.

        """

        self._conn = self._create_connection(db_file_path)
        if self._conn is not None:
            self._create_cached_dates_table()
            self._create_announcements_table()
        else:
            print('Error! cannot create the database connection.')

    def _create_connection(self, db_file):
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            # print(sqlite3.version)
        except sqlite3.Error as e:
            print(e)

        return conn

    def _create_cached_dates_table(self):

        sql = ('CREATE TABLE IF NOT EXISTS cached_dates ('
               'date text NOT NULL PRIMARY KEY);')
        try:
            c = self._conn.cursor()
            c.execute(sql)
        except sqlite3.Error as e:
            print(e)

    def _create_announcements_table(self):

        sql = ('CREATE TABLE IF NOT EXISTS announcements ('
               'date text NOT NULL,'
               'ticker text NOT NULL,'
               'period text NOT NULL,'
               'PRIMARY KEY (date, ticker));')
        try:
            c = self._conn.cursor()
            c.execute(sql)
        except sqlite3.Error as e:
            print(e)

    def _create_string_of_rows_for_VALUES_clause(self, str_list):
        """Create a string that can be passed into the SQL VALUES clause to create a row for each string in str_list.

        The sqlite VALUES clause creates a temporary table from the tuples passed in, where each tuple is a row.
        In this case, the cached_dates table has one column and I'm having trouble creating a tuple of one to pass
        into it. This is my workaround.


        Args:
            str_list (list):
                A list of date strings, that will be combined into a new string for VAULES

        Returns:
            str:
                A string that can be passed into the SQL VALUES clause to create a row for each string in str_list.

        """
        string_of_rows = ''
        for string in str_list:
            string_of_rows = string_of_rows + "('{}'),".format(string)
        string_of_rows = string_of_rows[:-1]

        return string_of_rows

    def check_for_missing_dates(self, date_list):
        """Look in the cache for dates and return the dates that aren't in the cache.

        Args:
            date_list (list):
                The list of dates to check the cache for.

        Returns:
            list:
                The dates from the date_list that are not in the cache.

        """

        # Convert to string that can be passed to VALUES
        date_list_str = self._create_string_of_rows_for_VALUES_clause(date_list)

        """
        Create a query like this one:
            SELECT *
            FROM
            (
                VALUES('2018-01-01'),('2018-01-02'),('2018-01-03'),('2018-01-04'),('2018-01-05')
            )
            EXCEPT
            SELECT date FROM cached_dates;
            
            
        Not sure why this query doesn't work: 
            SELECT d.date
            FROM
            (
                VALUES('2018-01-01'),('2018-01-02'),('2018-01-03'),('2018-01-04'),('2018-01-05')
            ) AS d(date)
            EXCEPT
            SELECT d.date FROM cached_dates;
        """

        sql = ( 'SELECT * '
                'FROM ' 
                '('
                'VALUES {}'
                ') '
                'EXCEPT '
                'SELECT date FROM cached_dates;').format(date_list_str)

        try:
            df = pd.read_sql(sql, self._conn, index_col='column1')
        except Exception as e:
            print(e)
            # create an empty dataframe to return
            df = pd.DataFrame({'A': []})

        missing_dates_list = df.index.tolist()
        return missing_dates_list

    def add(self, missing_dates, uncached_announcements_df):
        """Add the uncached announcements to the cache.

        Args:
            missing_dates (list):
                The dates that were fetched and should be added to the cache index.
                Even dates that have no data should be added to the cache index so that if requested again, we return
                nothing for them without using the fetcher.
            uncached_announcements_df (DataFrame):
                A Dataframe containing uncached announcements that should be added to the cache.
        """

        if not missing_dates:
            return

        #
        # add all the dates cached_dates table
        #

        # First create a string for the VALUES clause
        date_list_str = self._create_string_of_rows_for_VALUES_clause(missing_dates)

        """
        Create a query like this one:
        REPLACE INTO cached_dates (date) 
        VALUES ('2018-01-01'),('2018-01-02'),('2018-01-03'),('2018-01-04'),('2018-01-05');
        """

        sql = ( 'REPLACE INTO cached_dates '
                '(date) '
                'VALUES {};').format(date_list_str)

        cur = self._conn.cursor()
        cur.execute(sql)
        self._conn.commit()

        if uncached_announcements_df is None:
            return

        #
        # Add the uncached announcements to the announcements table
        #

        # first generate a list of tuples for each row in the dataframe
        values = list(uncached_announcements_df.itertuples())

        sql = ('REPLACE INTO announcements'
               '(date, ticker, period)'
               'VALUES (?, ?, ?);')

        cur = self._conn.cursor()
        cur.executemany(sql, values)
        self._conn.commit()

    def fetch_calendar(self, start_date_str, end_date_str=None):
        """Returns the earnings calendar from the cache as a pandas DataFrame.

        Args:
            start_date_str (str):
                The start date of the earnings calendar in the format ``YYYY-MM-DD``.
            end_date_str (str):
                The end date of the earnings calendar in the format ``YYYY-MM-DD``.
                If left out, we will fetch only the announcements for the start date.

        Returns:
            DataFrame:
                Returns a pandas DataFrame indexed by ``date``, that has columns: ``ticker``, and ``when``
                and a row for each announcement.
        """
        if end_date_str is None:
            end_date_str = start_date_str

        # Create a query like this one:
        # SELECT * FROM announcements WHERE date between '2018-01-01' AND '2018-01-05';
        values = (start_date_str, end_date_str)
        sql = "SELECT * FROM announcements WHERE date BETWEEN ? AND ?;"

        try:
            df = pd.read_sql(sql, self._conn, index_col='date', params=values)
            df.rename(columns={'period': 'when'}, inplace=True)
        except Exception as e:
            print(e)
            # create an empty dataframe to return
            df = pd.DataFrame({'A': []})
        return df
