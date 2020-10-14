Primary DMA (Matriz) python connector
=====================================

Overview
--------
**pymatriz** is a python library that allows interactions with Primary DMA (Matriz) Rest and Websocket APIs.

Installing
----------
*pymatriz* is available at the `Python Package Index <https://pypi.org/project/pymatriz>`_ repository. Install and update using `pip <https://pip.pypa.io/en/stable/quickstart/>`_\ :

.. code-block::

   pip install pymatriz


API Credentials
---------------

Credentials provided by your broker which use Primary DMA (Matriz) platform.

Usage
~~~~~~~~~~~~~~~~~
.. code::

    import datetime

    from pymatriz.enums import MarketDataEntry, Market
    from pymatriz.matriz_api_client import MatrizAPIClient

    client = MatrizAPIClient(username="", password="")

    # Real-time message handling
    client.add_market_data_handler(lambda msg: print(msg))

    # Error handling
    client.set_exception_handler(lambda e: print(e))

    # Negotiate Auth Token and connects to websocket
    client.connect()

    # Rest API call + websocket subscription
    print(client.get_daily_history(["GGAL"], terms=[MarketDataEntry.TERM_48HS], market=Market.MERVAL, start_date=datetime.date(2020, 10, 5)))

    # Ends websocket connection
    client.close()

Disclaimer
----------

The library is built as a result of a reverse engineering process, so use it on your own behalf.

This library is provided 'as is' without warranty of any kind, either express or implied, including, but not limited to, the implied warranties of fitness for a purpose, or the warranty of non-infringement.
