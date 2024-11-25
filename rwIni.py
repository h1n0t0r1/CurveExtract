import configparser
from os.path import expanduser, exists

class RWIni(configparser.ConfigParser):
    path = 'CurveExtract.ini'
    def __init__(self):
        super().__init__()
        self.checkIni()
        self.path = RWIni.path
        self.read(self.path)


    def readIni(self, section, key):
        val = self.get(section, key)
        return val

    def writeIni(self, section, key, value):
        self.set(section, key, value)
        with open(self.path, 'w') as configfile:
            self.write(configfile)

    def checkIni(self):
        if not exists(self.path):
            self['FTP'] = {
                'Path' : '',
                'IP'   : '',
                'User' : '',
                'Password' : ''
            }


            with open(self.path, 'w') as configfile:
                self.write(configfile)