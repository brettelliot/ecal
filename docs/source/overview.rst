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

.. code-block:: python

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

.. code-block:: python

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

By default ``ecal`` will use a ``RuntimeCache`` to keep data in memory and make repeated calls to ``ecal.get`` go much quicker. This example demonstrates the default ``RuntimeCache``:

.. literalinclude:: ../../examples/example_runtime_cache.py
    :language: python

``ecal`` supports using other cache systems by deriving from ``AbstractCache``.
