#▓█████▄  ▄▄▄       ███▄    █ ▒██░ ██░ ███▄ ▄███░ ▒█████   ██▀███  
#▒██▀ ██▌▒████▄     ██ ▀█   █ ▒██▒▒██▒▓██▒▀█▀ ██▒▒██▒  ██▒▓██ ▒ ██▒
#░██   █▌▒██  ▀█▄  ▓██  ▀█ ██▒▒██▒▒██▒▓██    ▓██░▒██░  ██▒▓██ ░▄█ ▒
#░▓█▄   ▌░██▄▄▄▄██ ▓██▒  ▐▌██▒░██░░██░▒██    ▒██ ▒██   ██░▒██▀▀█▄  
#░▒████▓  ▓█   ▓██▒▒██░   ▓██░░██░░██░▒██▒   ░██▒░ ████▓▒░░██▓ ▒██▒
# ▒▒▓  ▒  ▒▒   ▓▒█░░ ▒░   ▒ ▒ ░▓  ░▓  ░ ▒░   ░  ░░ ▒░▒░▒░ ░ ▒▓ ░▒▓░
# ░ ▒  ▒   ▒   ▒▒ ░░ ░░   ░ ▒░ ▒ ░ ▒ ░░  ░      ░  ░ ▒ ▒░   ░▒ ░ ▒░
# ░ ░  ░   ░   ▒      ░   ░ ░  ▒ ░ ▒ ░░      ░   ░ ░ ░ ▒    ░░   ░ 
#   ░          ░  ░         ░  ░   ░         ░       ░ ░     ░     
# pylint: disable=W,import-error
from syntax_tree.node import node
import syntax_tree.calculate as operate
class branch(node):
    # child amount
    __counter = 0
    # node id
    __id = ''

    # _value and _type inherits from node class
    def __init__(self):
        self._value = {}

    def add(self, value):
        self._value[self.__counter] = value
        self.__counter += 1

    def setType(self, typ):
        self._type = node.TYPE[typ]
        self.__id = typ

    def setValue(self, id):
        self.__id = id

    def getValue(self):
        return self.__id

    def getSize(self):
        return len(self._value)

    def getType(self):
        return self._type

    def getChild(self, index):
        if index < len(self._value) and index >= 0:
            return self._value[index]
        return None

    def execute(self, sym_table):
        #TODO switch for execute each node.TYPE of branch
        switch={
                # MATH
                self.TYPE["ADD"] : operate.ADD,
                self.TYPE["SUB"] : operate.SUB,
                self.TYPE["MUL"] : operate.MUL,
                self.TYPE["DIV"] : operate.DIV,
                self.TYPE["MOD"] : operate.MOD,
                # LOGIC
                self.TYPE["AND"] : operate.AND,
                self.TYPE["OR"] : operate.OR,
                self.TYPE["XOR"] : operate.XOR,

                self.TYPE["ASSIGN"] : operate.ASSIGN
                }
        #TODO need to return semantic errors and print to terminal
        for label in range(self.getSize()):
            label_node = self.getChild(label)
            if label_node.getType() == self.TYPE["LABEL"]:
                for child in range(label_node.getSize()):
                    child_node = label_node.getChild(child)
                    func=switch.get(child_node.getType(),lambda :'Node not defined')
                    result = func(child_node, sym_table)
                    if result != None:
                        return result
            else:
                func=switch.get(self.getType(),lambda :'Node not defined')
                return func(self, sym_table)