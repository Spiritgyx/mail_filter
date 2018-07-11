import sys, json
from dbhash import *
import traffic_sniff as TS


class Main:
    def __init__(self, *args):
        # Start parameters
        self.debug = True
        self.mode = 'console'
        # Changed parameters (python __main__.py mode=console debug=0)
        for i in args:
            if (i.count('=') == 1) and (i.split('=') == 2):
                param, value = i.split('=')
                if param == 'debug':
                    if value == 1 or value == 'true':
                        self.debug = True
                elif param == 'mode':
                    if value == 'gui':
                        self.mode = 'gui'
        dprint(self.debug, 'DEBUG = TRUE')
        # test hash
        self.dbh = DBHash(debug=self.debug)
        self.dbh.jsonLoad()
        self.dbh.jsonCheckCurrentData()
        self.dbh.jsonCheckNewData()
        self.dbh.jsonSave()
        # test sniffer
        self.ts = TS.TSniffer(debug=self.debug)
        #print('st')
        self.ts.thread.start()
        #print('con')
        summ = hashlib.sha256()

        logs = {"data": []}
        '''
        while True:
            if len(self.ts.data) > 0:
                packet = self.ts.data.pop(0)
                summ.update(packet[1])
                if self.dbh.jsonCheckExist(summ.hexdigest()):
                    pass'''
        while not self.ts.exitFlag:
            if len(self.ts.data) > 0:
                packet = self.ts.data.pop(0)

                if not self.dbh.jsonCheckExist(packet['hash']):
                    logFile = open('log.txt', mode='w')
                    logs['data'].append(packet)
                    logFile.write(json.dumps(logs, indent=2, sort_keys=True))
                    print('WARNING!',
                          '\nhash: {}\nip: {}\npath: {}\ntime: {}'.format(
                              packet['hash'], packet['ip'], packet['path'], packet['time']
                          ))
                    logFile.close()

        pass


if __name__ == '__main__':
    obj = Main(sys.argv)
