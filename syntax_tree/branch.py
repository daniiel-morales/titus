# pylint: disable=W,import-error
from syntax_tree.node import node

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
        pass