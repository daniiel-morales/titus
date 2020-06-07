# pylint: disable=W,import-error
from syntax_tree.node import node

class leaf(node):
    # _value and _type inherits from node class
    def __init__(self, value, typ):
        self._value = value
        self._type = node.TYPE[typ]

    def setValue(self, value):
        self._value = value

    def setType(self, typ):
        self._type = node.TYPE[typ]

    def getValue(self):
        return self._value

    def getType(self):
        return self._type

    def getChild(self, index):
        return None

    def execute(self, sym_table):
        if self._type == node.TYPE["ID"]:
            return sym_table[self._value]
        return self._value
        