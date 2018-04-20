#!/usr/bin/python
import sys, getopt
from EvansOrderBook import EvansOrderBook

def dump_help():
    print "Usage: ./RunOrderBook.py [--help --gdax --stats --count=<count> --json=<json> --product=<product> --levels=<levels>]"
    print "Options and arguments:"
    print "--help\t\t: displays this screen"
    print "--json=<...>\t: uses the specified JSON file,"
    print "\t\t  otherwise defaults to the GDAX feed"
    print "--gdax\t\t: uses the GDAX feed (default:True)"
    print "--stats\t\t: displays stats during updates (default:False)"
    print "--count=<...>\t: program stops after these many messages (default:1000)"
    print "--product=<...>\t: specifies the product (default:BTC-USD)"
    print "--levels=<...>\t: specifies the number of bid/ask levels"
    print "\t\t  to display (default:5)"
    sys.exit(0)

if __name__ == "__main__":
    json_input = 'gdax_sample_01.json'
    exit_on_count = 10000
    use_gdax = True
    show_stats = False
    product = 'BTC-USD'
    levels = 5
    try:
        opts, args = getopt.getopt(sys.argv[1:],'hgsj:c:p:l:', ['help','gdax','stats','levels=','json=','count=','product='])
        for key, value in opts:
            if key in ('-h', '--help'): dump_help()
            if key in ('-j', '--json'): json_input = value; use_gdax = False
            if key in ('-w', '--gdax'): use_gdax = True
            if key in ('-s', '--stats'): show_stats = True
            if key in ('-c', '--count'): exit_on_count = value
            if key in ('-p', '--product'): product = value
            if key in ('-l', '--levels'): levels = value
    except Exception as e:
        print e; dump_help()
    ob = EvansOrderBook();
    if use_gdax:
        ob.init(product,levels,show_stats,exit_on_count)
        ob.start()
    else:
        json_output = ob.read_json(json_input)
        print json_output
