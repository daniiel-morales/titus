#▓█████▄  ▄▄▄       ███▄    █ ▒██░ ██░ ███▄ ▄███░ ▒█████   ██▀███  
#▒██▀ ██▌▒████▄     ██ ▀█   █ ▒██▒▒██▒▓██▒▀█▀ ██▒▒██▒  ██▒▓██ ▒ ██▒
#░██   █▌▒██  ▀█▄  ▓██  ▀█ ██▒▒██▒▒██▒▓██    ▓██░▒██░  ██▒▓██ ░▄█ ▒
#░▓█▄   ▌░██▄▄▄▄██ ▓██▒  ▐▌██▒░██░░██░▒██    ▒██ ▒██   ██░▒██▀▀█▄  
#░▒████▓  ▓█   ▓██▒▒██░   ▓██░░██░░██░▒██▒   ░██▒░ ████▓▒░░██▓ ▒██▒
# ▒▒▓  ▒  ▒▒   ▓▒█░░ ▒░   ▒ ▒ ░▓  ░▓  ░ ▒░   ░  ░░ ▒░▒░▒░ ░ ▒▓ ░▒▓░
# ░ ▒  ▒   ▒   ▒▒ ░░ ░░   ░ ▒░ ▒ ░ ▒ ░░  ░      ░  ░ ▒ ▒░   ░▒ ░ ▒░
# ░ ░  ░   ░   ▒      ░   ░ ░  ▒ ░ ▒ ░░      ░   ░ ░ ░ ▒    ░░   ░ 
#   ░          ░  ░         ░  ░   ░         ░       ░ ░     ░     
# pylint: disable=import-error
from sym_table.sym import sym
class table:
    __table = None
    __log = None
    __scope = None
    __grammar = None

    def __init__(self):
        self.__table = {}
        self.__log = ''
        self.__scope = 'GLOBAL'
        self.__grammar = {}

    def add(self, identifier, typ, size, value, scope):
        if self.get(identifier) == None:
            # value for instance in __table diccionary
            ins = sym(identifier, typ, size, value, scope, typ)
            
            # adds the instance in the table
            self.__table[identifier] = ins
            return True
        return False
        
    def update(self, identifier, ins):
        # check if exists
        if self.get(identifier) != None:
            # updates the instance in the table
            self.__table[identifier] = ins
            return True
        return False

    def remove(self, identifier):
        if identifier:
            try:
                self.__table.pop(identifier)
                return True
            except:
                return False
        return False

    def get(self, identifier):
        # returns sym class
        try:
            return self.__table[identifier]
        except:
            return None

    def setScope(self, scope):
        self.__scope = scope

    def getScope(self):
        return self.__scope

    def appendLog(self, txt):
        self.__log += '>> ' + str(txt) + '\n'

    def appendGrammar(self, index, txt):
        try:
            self.__grammar[index]
        except:
            self.__grammar[index] = txt

    def getGrammar(self):
        return self.__grammar

    def getLog(self):
        return self.__log

    def printTable(self):
        return self.__table
