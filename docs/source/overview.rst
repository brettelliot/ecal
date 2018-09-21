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

               ticker when  market_cap_mm
    date
    2017-03-30   AEHR  amc             54
    2017-03-30   ANGO  bmo            843
    2017-03-30   BSET   --            227
    2017-03-30     FC  amc            325
    2017-03-30    LNN  bmo           1039
    2017-03-30   SAIC  bmo           3249
    2017-03-30   TITN  bmo            384

The ``market_cap_mm`` will be different for you when you run this. That is because the API returns the market cap at the time it was called and not on the earnings announcement date. That may be important if you use this for backtesting.

Let's look at an example to get the earnings calendar for a range of dates:

.. literalinclude:: ../../examples/example_range.py
    :language: python

.. code-block:: python

               ticker when  market_cap_mm
    date
    2018-01-04    CMC  bmo           2523
    2018-01-04   LNDC  amc            372
    2018-01-04   NEOG  bmo           4728
    2018-01-04    RAD  amc           1419
    2018-01-04   RECN  amc            526
    2018-01-04    UNF  bmo           3365
    2018-01-05   AEHR  amc             54
    2018-01-05   ANGO  bmo            843
    2018-01-05     FC  amc            325
    2018-01-05     LW  bmo           9556
    2018-01-05    PKE  bmo            393
    2018-01-05   PSMT  amc           2547
    2018-01-05    RPM  bmo           9003
    2018-01-05   SONC  amc           1316
    2018-01-05    WBA  bmo          70739

This example will take about 8 seconds to run. This is because ``ecal`` throttles the calls to the API to prevent rate limiting.

