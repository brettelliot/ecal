What is ecal?
-------------

``ecal`` is a package for getting a US equity earnings announcement calendar.

For more documentation, please see http://ecal.readthedocs.io.

Installation
------------

``ecal`` can be easily installed with pip::

    $ pip install ecal

Quickstart
----------

.. code-block:: python

    import ecal
    cal_df = ecal.get('2017-03-30')

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


    *ticker* is the ticker symbol on NYSE or NASDAQ.

    *when* can be: ``bmo`` which means *before market open*, ``amc`` which means *after market close* or ``--`` which means *no time reported*.

Caching
--------

``ecal`` supports caching so that repeated calls don't actually make server calls. This is important as the source APIs are throttled, at approximately one second per call. Runtime caching in enabled by default but persistent on disk caching (via sqlite) is very easily used:

.. code-block:: python

    import ecal
    ecal.default_cache = ecal.SqliteCache('ecal.db')
    cal_df = ecal.get('2017-03-30')

Extension
---------

``ecal`` is very easy to extend in case you want to support another caching system or even use another earnings announcement provider. For more documentation, please see http://ecal.readthedocs.io.