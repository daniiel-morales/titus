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
                # COMPARE
                self.TYPE["EQUAL"] : operate.EQUAL,
                self.TYPE["NOEQUAL"] : operate.NOEQUAL,
                self.TYPE["GTHAN"] : operate.GTHAN,
                self.TYPE["GE_OP"] : operate.GE_OP,
                self.TYPE["LTHAN"] : operate.LTHAN,
                self.TYPE["LE_OP"] : operate.LE_OP,
                # STRUCT
                self.TYPE["ACCESS"] : operate.ACCESS,

                self.TYPE["PRINT"] : operate.PRINT,
                self.TYPE["ASSIGN"] : operate.ASSIGN
                }
        #TODO need to return semantic errors
        has_print = False
        for label in range(self.getSize()):
            label_node = self.getChild(label)
            if label_node.getType() == self.TYPE["LABEL"]:
                for child in range(label_node.getSize()):
                    child_node = label_node.getChild(child)
                    func=switch.get(child_node.getType(),lambda :'Node not defined')
                    result = func(child_node, sym_table)
                    if child_node.getType() == self.TYPE["PRINT"]:
                        has_print = True
                    # save the ast node in reference for goto
                    label_ref = sym_table.get(label_node.getValue())
                    label_ref.setRef(label_node)
                    sym_table.update(label_node.getValue(), label_ref)
            else:
                func=switch.get(self.getType(),lambda :'Node not defined')
                return func(self, sym_table)
        if has_print:
            return sym_table.getLog()
        return None