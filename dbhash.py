import json
import hashlib
import os


def checkHash(path):
    if os.path.exists(path):
        file = open(path, mode='rb')
        data = file.read()
        file.close()
        summ = hashlib.sha256()
        summ.update(data)
        return summ.hexdigest()
    else:
        return 1


def dprint(debug=False, *args):
    if debug:
        print(*args)


class DBHash:
    def __init__(self, debug=False):
        self.debug = debug
        self.json_path = 'db.json'
        self.json_data = {}
        self.types = ['jpg', 'png', 'bmp', 'jpeg']
        self.paths = []

    # Load DB
    def jsonLoad(self):
        try:
            if os.path.exists(self.json_path):
                file = open(self.json_path, mode='r')
                self.json_data = json.loads(file.read())
                file.close()
                return 0
            else:
                self.json_data = {'types': ['jpg', 'png', 'bmp', 'jpeg'],
                                  'paths': ['./images'],
                                  'data': []}
                return 1
        except:
            self.json_data = {'types': ['jpg', 'png', 'bmp', 'jpeg'],
                              'paths': ['./images'],
                              'data': []}
            return 1

    # Save DB
    def jsonSave(self):
        data = json.dumps(self.json_data, indent=4, sort_keys=True)
        file = open(self.json_path, mode='w')
        file.write(data)
        file.close()

    # Checking existing files
    def jsonCheckCurrentData(self):
        if self.json_data == {}:
            return 1
        jsD = self.json_data
        ind = 0
        indToDel = []
        self.types = jsD['types']
        self.paths = jsD['paths']
        for i in jsD['data']:
            fPath = i['path'] + '\\' + i['name']
            if os.path.exists(fPath):
                summ = checkHash(fPath)
                if summ == 1:
                    dprint(self.debug, 'File "{}" not exist'.format(fPath))
                else:
                    if i['hash'] != summ:
                        dprint(self.debug,
                               'Mismatch detected: "{}"\ncurrent "{}"\nlast    "{}"'.format(fPath, summ, i['hash']))
                        i['hash'] = summ
            else:
                dprint(self.debug, 'File "{}" not exist'.format(fPath))
                indToDel.append(ind)
            ind += 1
        indToDel.reverse()
        for i in indToDel:
            jsD['data'].pop(i)

    # Check new images
    def jsonCheckNewData(self):
        jsD = self.json_data
        types = self.types
        for path in self.paths:
            fileList = os.listdir(path)
            # dprint(self.debug, 'fileList: ', fileList)
            res = [[i for j in types if j in i] for i in fileList]
            # dprint(self.debug, 'res: ', res)
            fileList = [i[0] for i in res if len(i) > 0]
            # dprint(self.debug, fileList)
            for i in fileList:
                jCFID = self.jsonCheckFileInData(path + '\\' + i)
                if jCFID[0]:
                    flagExist = False
                    for j in jsD['data']:
                        if j['hash'] == jCFID[1]['hash']:
                            flagExist = True
                    if not flagExist:
                        jsD['data'].append(jCFID[1])

    def jsonCheckFileInData(self, path):
        summ = checkHash(path)
        if summ == 1:
            dprint(self.debug, 'File "{}" not exist'.format(path))
            return False
        dirPath = os.path.dirname(path)
        name = os.path.basename(path)
        type_ = str(name).split('.')[-1]
        return True, {'name': name, 'type': type_, 'path': dirPath, 'hash': summ}
