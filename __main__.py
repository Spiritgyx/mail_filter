import sys
from dbhash import *


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
        # test
        self.dbh = DBHash(debug=self.debug)
        self.dbh.jsonLoad()
        self.dbh.jsonCheckCurrentData()
        self.dbh.jsonCheckNewData()
        self.dbh.jsonSave()
        pass


if __name__ == '__main__':
    obj = Main(sys.argv)
