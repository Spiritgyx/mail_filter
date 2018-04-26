from scapy.all import *
import json, os, time
import threading as TH
from dbhash import checkHash


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
        self.exitFlag = False
        self.data = []
        self.thread = TH.Thread(target=self.test)
        pass

    def sniff(self):
        while True:
            sn = sniff(filter='smtp', count=1)
            # sn.display()
            p = hexRaw(sn)
            self.data.append((sn[0], p[0]))
        pass

    def test(self):
        while True:
            js = input('Enter test json: ')
            if js == 'Q':
                self.exitFlag = True
                break
            try:
                js = json.loads(js)
                path = js['path']
                time_ = js['time']
                ip = js['ip']
                if os.path.exists(path):
                    hash = checkHash(path)
                    js.update({'hash': hash})
                    self.data.append(js)
                else:
                    print('File "{}" not exist.'.format(path))
            except:
                print('InputError')
            time.sleep(0.01)

# {"ip": "200.200.200.200", "time": "2018-04-20;12:24:48", "path": "./test_img/test.png"}
# {"ip": "200.200.200.200", "time": "2018-04-20;12:24:48", "path": "./images/3.jpg"}
