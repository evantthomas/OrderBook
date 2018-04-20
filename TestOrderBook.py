#!/usr/bin/python
import unittest
from EvansOrderBook import EvansOrderBook

class OrderBookTest(unittest.TestCase):
    def test_is_market_crossed(self):
        ob = EvansOrderBook()
        ob.read_json('gdax_sample_01.json')
        self.assertEqual(ob.is_market_crossed(),False)
    def test_is_logic_complete(self):
        ob = EvansOrderBook()
        json_output = ob.read_json('gdax_sample_01.json')
        expected_output = "SEQU:13 MSGS:13 OPEN:5 DONE:3 CHNG:1 MATC:2 ASKS:1 BIDS:1 BBOS: 199.80/200.40"
        self.assertEqual(json_output,expected_output)

if __name__ == "__main__":
    unittest.main()
