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

    def start_execute(self, sym_table, start_from):
        delete_label_up_to = 0
        for label in range(self.getSize()):
            label_node = self.getChild(label)
            if label_node.getValue() == start_from:
                break
            else:
                delete_label_up_to += 1

        # pop labels to make a goto simulation
        for label in range(delete_label_up_to):
            self._value.pop(label)

        return self.execute(sym_table)

    switch={
            # MATH
            node.TYPE["ADD"] : operate.ADD,
            node.TYPE["SUB"] : operate.SUB,
            node.TYPE["MUL"] : operate.MUL,
            node.TYPE["DIV"] : operate.DIV,
            node.TYPE["MOD"] : operate.MOD,

            node.TYPE["ABS"] : operate.ABS,
            # LOGIC
            node.TYPE["AND"] : operate.AND,
            node.TYPE["OR"]  : operate.OR,
            node.TYPE["XOR"] : operate.XOR,

            node.TYPE["NOT"] : operate.NOT,
            # COMPARE
            node.TYPE["EQUAL"]  : operate.EQUAL,
            node.TYPE["NOEQUAL"]: operate.NOEQUAL,
            node.TYPE["GTHAN"]  : operate.GTHAN,
            node.TYPE["GE_OP"]  : operate.GE_OP,
            node.TYPE["LTHAN"]  : operate.LTHAN,
            node.TYPE["LE_OP"]  : operate.LE_OP,
            # BITWISE
            node.TYPE["BAND"]   : operate.BAND,
            node.TYPE["BOR"]    : operate.BOR,
            node.TYPE["BXOR"]   : operate.BXOR,
            node.TYPE["SLEFT"]  : operate.SLEFT,
            node.TYPE["SRIGHT"] : operate.SRIGHT,

            node.TYPE["BNOT"]   : operate.BNOT,
            # STRUCT
            node.TYPE["ACCESS"] : operate.ACCESS,
            
            node.TYPE["UNSET"]  : operate.UNSET,
            node.TYPE["PRINT"]  : operate.PRINT,
            node.TYPE["ASSIGN"] : operate.ASSIGN
            }

    def execute(self, sym_table):
        #TODO need to return semantic errors
        has_print = False
        label_list = list(self._value.keys())
        for label in label_list:
            label_node = self._value[label]
            if label_node.getType() == self.TYPE["LABEL"]:
                for child in range(label_node.getSize()):
                    child_node = label_node.getChild(child)
                    if child_node.getType() == self.TYPE["EXIT"]:
                        if has_print:
                            return [sym_table.getLog(), None]
                        return [None, None]
                    elif child_node.getType() != self.TYPE["GOTO"]:
                        func=self.switch.get(child_node.getType(),lambda :'Node not defined')
                        result = func(child_node, sym_table)
                        if child_node.getType() == self.TYPE["PRINT"]:
                            has_print = True
                    else:
                        # need to finish the execution
                        # and return a value for restart execution for other point
                        goto_label = child_node.getChild(0).getValue()
                        if has_print:
                            return [sym_table.getLog(), goto_label]
                        return [None, goto_label]
            else:
                func=self.switch.get(self.getType(),lambda :'Node not defined')
                return func(self, sym_table)
        if has_print:
            return [sym_table.getLog(), None]
        return [None,None]