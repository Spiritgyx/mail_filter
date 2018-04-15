from scapy.all import *
import json
import threading as TH


def hexRaw(sn):
    p = []
    for i, res in enumerate(sn.res):
        a = sn._elt2pkt(res)
        if a.haslayer(conf.raw_layer):
            p.append(a.getlayer(conf.raw_layer).load)
        else:
            p.append(b'')
    return p


class TSniffer:
    def __init__(self, debug=False):
        self.debug = debug
        self.data = []
        self.thread = TH.Thread(target=sniff)
        pass

    def sniff(self):
        while True:
            sn = sniff(filter='smtp', count=1)
            # sn.display()
            p = hexRaw(sn)
            self.data.append((sn[0], p[0]))
        pass
