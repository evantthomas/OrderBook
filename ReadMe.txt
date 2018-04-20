EvansOrderBook is a continuously updating order book for the GDAX crypto exchange.
It was written with Python 2.7.9 on an Ubuntu 15.04 box.
The market data feed connects to 'wss://ws-feed.gdax.com' via a websocket.

There are four files here:
1. EvansOrderBook.py (the order book class)
2. RunOrderBook.py (collects user parameters and runs the order book class)
3. TestOrderBook.py (runs unit tests for the order book class)
4. gdax_sample_01.json (sample JSON text)

Initial development was done with a sample JSON file to control the logic.
When I moved to the real feed, I included a few tests like:
1. checking the sequence numbers to ensure I’m not dropping any packets,
2. looking over the messages to make sure they are mostly adequate, 
3. including a real-time count of the different order types,and, of course,
4. watching for crossed markets.

By default, it subscribes to the bitcoin market data feed (BTC-USD).
After each tick, it outputs the inside (i.e. best) 5 ask and 5 bid levels (quantity and price).

The default behavior of EvansOrderBook is to provide 5 levels of bid/ask for BTC-USD.
However, you can specify other parameters, such as
1. product,
2. number of displayed levels,
3. statistics output,
4. a JSON file,
5. and so on.

For a complete list of available options, enter this from a Linux shell:

% ./RunOrderBook.py --help

Usage: ./RunOrderBook.py [--help --gdax --stats --count=<count> --json=<json> --product=<product> --levels=<levels>]
Options and arguments:
--help          : displays this screen
--json=<...>    : uses the specified JSON file,
                  otherwise defaults to the GDAX feed
--gdax          : uses the GDAX feed (default:True)
--stats         : displays stats during updates (default:False)
--count=<...>   : program stops after these many messages (default:1000)
--product=<...> : specifies the product (default:BTC-USD)
--levels=<...>  : specifies the number of bid/ask levels
                  to display (default:5)

Here are some examples: 

% ./RunOrderBook.py

   ===>	BTC-USD
   0.00112 @ 8506.95
   0.00112 @ 8506.94
   0.00147 @ 8506.93
   0.00112 @ 8506.92
   6.58059 @ 8506.00
---------------------
  17.17009 @ 8505.99
   0.00235 @ 8505.80
   0.03500 @ 8505.01
   0.29394 @ 8505.00
   0.02700 @ 8503.66

% ./RunOrderBook.py --count=1000 --levels=10 --stats

   ===>	BTC-USD
   SEQU:	5719144485 
   MSGS:	1001
   OPEN:	334 
   DONE:	326 
   MATC:	4 
   CHNG:	0
   ASKS:	23 
   BIDS:	25 

   0.00194 @ 8510.90	1
   0.50000 @ 8509.27	1
   1.17545 @ 8508.85	1
   0.10000 @ 8507.09	1
   0.00135 @ 8507.08	1
   0.00112 @ 8507.07	1
   0.00182 @ 8507.06	1
   0.00135 @ 8507.05	1
   0.05000 @ 8506.84	1
   8.00906 @ 8506.00	7
---------------------
   0.30000 @ 8500.00	1
   0.10000 @ 8497.03	1
   0.10000 @ 8496.69	1
   0.02169 @ 8496.48	1
   0.12322 @ 8494.50	1
   1.80000 @ 8488.97	2
   0.90000 @ 8486.42	1
   0.90000 @ 8484.72	1
   0.50000 @ 8482.09	1
   2.00000 @ 8479.04	1

% ./RunOrderBook.py --product=ETH-EUR --levels=1

   ===>	ETH-EUR
   2.08619 @ 478.78
---------------------
   0.15600 @ 478.65


