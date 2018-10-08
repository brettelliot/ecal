=============
What is ecal?
=============

``ecal`` (pronounced ee-cal) is a package for getting a US equity earnings announcement calendar.

For more documentation, please see http://ecal.readthedocs.io.

Installation
------------

``ecal`` can be easily installed with pip::

    $ pip install ecal

Usage
-----
``ecal`` is really simple to use. Below you'll find the basics.

Getting the earnings announcements for a single date
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To get the earnings announcements for a single date simply import ``ecal`` and call ``get()``:

.. code-block:: python

    import ecal

    cal_df = ecal.get('2017-03-30')

The results will be an earnings calendar in a pandas DataFrame:

.. code-block:: none

               ticker when
    date
    2017-03-30   AEHR  amc
    2017-03-30   ANGO  bmo
    2017-03-30   BSET   --
    2017-03-30     FC  amc
    2017-03-30    LNN  bmo
    2017-03-30   SAIC  bmo
    2017-03-30   TITN  bmo


The returned DataFrame has the following columns:

    *ticker*
        is the ticker symbol on NYSE or NASDAQ.

    *when*
        can be ``bmo`` which means *before market open*, ``amc`` which means *after market close* or
        ``--`` which means *no time reported*.

If there were no announcements for this day, an empty DataFrame will be returned.

Getting the earnings announcements for a date range
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is equally easy to get the earnings announcements for a date range:

.. code-block:: python

    import ecal

    cal_df = ecal.get('2018-01-01', '2018-01-05')

Once again the results will be an earnings calendar in a pandas DataFrame:

.. code-block:: none

               ticker when
    date
    2018-01-04    CMC  bmo
    2018-01-04   LNDC  amc
    2018-01-04   NEOG  bmo
    2018-01-04    RAD  amc
    2018-01-04   RECN  amc
    2018-01-04    UNF  bmo
    2018-01-05   AEHR  amc
    2018-01-05   ANGO  bmo
    2018-01-05     FC  amc
    2018-01-05     LW  bmo
    2018-01-05    PKE  bmo
    2018-01-05   PSMT  amc
    2018-01-05    RPM  bmo
    2018-01-05   SONC  amc
    2018-01-05    WBA  bmo

Days with no earnings announcements will have no rows in the DataFrame. In the example above, there were no announcements on Jan first, second and third.

It should be noted that ``ecal`` fetches earnings announcements from ``api.earningscalendar.net`` by default. This source limits us to 1 call per second. However you don't have to worry about this because the ``ecal.ECNFetcher`` throttles calls to the API to prevent rate limiting. That said, please note that this fetcher gets announcements one day at a time which means if you want 30 days, it's going to take 30 seconds to get that data. Yikes. Fear not... that's why ``ecal`` comes with caching.

Caching
~~~~~~~

``ecal`` supports caching so that repeated calls to ``ecal.get()`` don't actually make calls to the server. Runtime caching is enabled by default which means calls during your program's execution will be cached. However, the ``ecal.RuntimeCache`` is only temporary and the next time your program runs it will call the API again.

Persistent on disk caching is provided via ``ecal.SqliteCache`` and can be easily enabled by setting ``ecal.default_cache`` once before calls to ``ecal.get()``:

.. code-block:: python

    import ecal
    ecal.default_cache = ecal.SqliteCache('ecal.db')

    cal_df = ecal.get('2017-03-30')

Extension
~~~~~~~~~

``ecal`` is very easy to extend in case you want to support another caching system or even create an earnings announcement fetcher. For more documentation, please see http://ecal.readthedocs.io.