#!/usr/bin/python
import os, sys, getopt, json, traceback
import gdax, time
from decimal import *

class EvansOrderBook(gdax.WebsocketClient):
    curr_seq = 0; message_count = 0; exit_on_count = 10000
    bid_dict = {}; ask_dict = {}
    type_codes = dict(open='open_order',done='done_order',match='match_order',change='change_order')
    dict_codes = dict(buy='bid_dict',sell='ask_dict')
    product = 'BTC-USD'; levels = 5; show_stats = False; use_json = False
    opens = 0; dones = 0; changes = 0; matches = 0
    getcontext().prec = 6
    def init(self,product='BTC-USD',levels=5,show_stats=False,exit_on_count=1000):
        self.product = product
        self.levels = int(levels)
        self.show_stats = bool(show_stats)
        self.exit_on_count = int(exit_on_count)
    def on_open(self):
        self.url = "wss://ws-feed.gdax.com/"
        #self.products = ["BTC-USD"]
        self.products = [self.product]
        self.message_count = 0
    def on_message(self,msg):
        self.message_count += 1
        self.process_message(msg)
        if self.message_count > self.exit_on_count:
            self.close()
            sys.exit()
    def on_close(self):
        print("-- Hasta La Vista Baby! --")
    def read_json(self, json_input):
        json_fp = open(json_input,"r")
        json_dict = json.load(json_fp)
        self.use_json = True
        jcnt = 0
        for msg in json_dict:
            self.process_message(msg)
            jcnt += 1
        json_output = "SEQU:%d MSGS:%d OPEN:%d DONE:%d CHNG:%d MATC:%d ASKS:%d BIDS:%d BBOS: %0.2f/%0.2f" % \
            (self.curr_seq,jcnt,self.opens,self.dones,self.changes,self.matches,len(self.ask_dict),len(self.bid_dict),max(self.bid_dict.keys()),min(self.ask_dict.keys()))
        return json_output 
    def process_message(self,msg):
        try:
            new_seq = msg.get('sequence',self.curr_seq)
            if new_seq <= self.curr_seq:
                print new_seq," out of sync with prior seq:",self.curr_seq
            self.curr_seq = new_seq
            type = msg.get('type','NA')
            if type not in ['open','change','match','done']: return
            side = msg.get('side','NA')
            if side == 'NA': return
            if not msg.has_key('price'): return
            prc = Decimal(msg['price'])
            if type == 'match': ord = msg.get('maker_order_id','NA')
            else: ord = msg.get('order_id','NA')
            call_this = "self.%s(self.%s,'%s',%f,msg)" % (self.type_codes.get(type,'NA'),self.dict_codes.get(side,'NA'),ord,prc)
            eval(call_this)
            self.print_inside()
        except Exception as e:
            print "ERROR"
            print e
            traceback.print_exc()
    def is_market_crossed(self):
        if len(self.bid_dict) == 0: return False
        if len(self.ask_dict) == 0: return False
        if max(self.bid_dict.keys()) >= min(self.ask_dict.keys()): return True
        return False;
    def print_inside(self):
        if self.use_json: return
        os.system('clear')
        if self.is_market_crossed(): print "MARKET CROSSED"
        print "   ===>\t",self.product
        if self.show_stats:
            print "   SEQU:\t",self.curr_seq,"\n   MSGS:\t",self.message_count
            print "   OPEN:\t",self.opens,"\n   DONE:\t",self.dones,"\n   MATC:\t",self.matches,"\n   CHNG:\t",self.changes
            print "   ASKS:\t", len(self.ask_dict),"\n   BIDS:\t",len(self.bid_dict),"\n"
        for adict in [self.ask_dict,self.bid_dict]:
            prcs = adict.keys()
            prcs.sort(reverse=True)
            if adict == self.bid_dict:
                sub_prcs = prcs[0:self.levels]
            else:
                sub_prcs = prcs[-self.levels:]
            for prc in sub_prcs:
                siz = Decimal(0.000000) 
                ords = 0
                for ord in adict[prc].keys():
                    siz += Decimal(adict[prc][ord]['remaining_size'])
                    ords += 1
                if self.show_stats:
                    if siz >= 100.0: print " %0.5f @ %0.2f\t%d" % (siz,prc,ords)
                    elif siz >= 10.0: print "  %0.5f @ %0.2f\t%d" % (siz,prc,ords)
                    else: print "   %0.5f @ %0.2f\t%d" % (siz,prc,ords)
                else:
                    if siz >= 100.0: print " %0.5f @ %0.2f" % (siz,prc)
                    elif siz >= 10.0: print "  %0.5f @ %0.2f" % (siz,prc)
                    else: print "   %0.5f @ %0.2f" % (siz,prc)
            if adict == self.ask_dict: print "---------------------"
            else: print ""
    def open_order(self,adict,ord,prc,msg):
        self.opens += 1
        if adict.has_key(prc):
            adict[prc].setdefault(ord,msg)
        else:
	    ord_dict = {}; ord_dict[ord] = msg
            adict.setdefault(prc,ord_dict)
        if self.is_market_crossed():
            del adict[prc]
    def done_order(self,adict,ord,prc,msg):
        self.dones += 1
        if adict.has_key(prc):
            adict.get(prc).pop(ord,None)
            if len(adict.get(prc)) == 0: adict.pop(prc)
    def match_order(self,adict,ord,prc,msg):
        self.matches += 1
        if not adict.has_key(prc): return
        if not adict[prc].has_key(ord): return
        adict[prc][ord]['remaining_size'] = Decimal(adict[prc][ord]['remaining_size']) - Decimal(msg['size'])
    def change_order(self,adict,ord,prc,msg):
        self.changes += 1
        if not adict.has_key(prc): return
        if not adict[prc].has_key(ord): return
        adict[prc][ord]['remaining_size'] = Decimal(msg['new_size'])

