What is ecal?
=============

``ecal`` is a package for getting a US equity earnings announcement calendar.

Installation
------------

``ecal`` can be easily installed with pip::

    $ pip install ecal

Usage
-----
Let's look at a simple example of using ``ecal``:

.. literalinclude:: ../../examples/example_single.py
    :language: python

The results will be an earnings calendar in a pandas Dataframe:

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

``ecal.get`` uses the ``ECNFetcher`` by default. It fetches earnings announcements from ``api.earningscalendar.net1``. However, ``ecal`` supports using other fetchers by deriving from ``AbstractFetcher``.

Let's look at an example to get the earnings calendar for a range of dates:

.. literalinclude:: ../../examples/example_range.py
    :language: python

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

This example will take about 8 seconds to run. This is because ``ecal`` throttles the calls to the API to prevent rate limiting.

Caching
-------

``ecal`` supports caching so that repeated calls don't actually make server calls. This is important as the source APIs are throttled, at approximately one second per call. By default ``ecal`` will use a ``RuntimeCache`` to keep data in memory and make repeated calls to ``ecal.get`` go much quicker. This example demonstrates the default ``RuntimeCache``:

.. literalinclude:: ../../examples/example_runtime_cache.py
    :language: python

.. code-block:: none

    Getting the earnings announcements for a date range and cache it.
    This first call will take ~ 8 seconds...
    The first call to ecal.get took 10.922043085098267 seconds
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
    By default, ecal uses an instance of RuntimeCache.
    The second time, ecal.get will use the cache.
    The second call to ecal.get took 0.0022749900817871094 seconds
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
    The third call, ecal.get will use the cache. This one asks for dates with no announcements:
    The third call to ecal.get took 0.0020399093627929688 seconds
    Empty DataFrame
    Columns: [ticker, when]
    Index: []

``ecal`` supports using other cache systems by deriving from ``AbstractCache``. ``ecal`` comes with a persistent cache that uses SQLite called ``SQLiteCache``. Using it is very easy:

.. literalinclude:: ../../examples/example_sqlite_cache.py
    :language: python


