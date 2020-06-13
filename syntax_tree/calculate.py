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
from syntax_tree.leaf import leaf
def ADD(node, sym_table):
    return MATH('+', node, sym_table)

def SUB(node, sym_table):
    return MATH('-', node, sym_table)

def MUL(node, sym_table):
    return MATH('*', node, sym_table)

def DIV(node, sym_table):
    return MATH('/', node, sym_table)

def MOD(node, sym_table):
    return MATH('%', node, sym_table)

def AND(node, sym_table):
    return LOGIC('*', node, sym_table)

def OR(node, sym_table):
    result = LOGIC('+', node, sym_table)
    if result == 2:
        return 1
    else:
        return result

def EQUAL(node, sym_table):
    exp = TOVALUE(node.getChild(0), sym_table)
    exp2 = TOVALUE(node.getChild(1), sym_table)

    if exp.getValue() == exp2.getValue():
        return 1
    return 0

def NOEQUAL(node, sym_table):
    exp = TOVALUE(node.getChild(0), sym_table)
    exp2 = TOVALUE(node.getChild(1), sym_table)

    if exp.getValue() != exp2.getValue():
        return 1
    return 0

def GTHAN(node, sym_table):
    exp = TOVALUE(node.getChild(0), sym_table)
    exp2 = TOVALUE(node.getChild(1), sym_table)

    if exp.getValue() > exp2.getValue():
        return 1
    return 0

def GE_OP(node, sym_table):
    exp = TOVALUE(node.getChild(0), sym_table)
    exp2 = TOVALUE(node.getChild(1), sym_table)

    if exp.getValue() >= exp2.getValue():
        return 1
    return 0

def LTHAN(node, sym_table):
    exp = TOVALUE(node.getChild(0), sym_table)
    exp2 = TOVALUE(node.getChild(1), sym_table)

    if exp.getValue() < exp2.getValue():
        return 1
    return 0

def LE_OP(node, sym_table):
    exp = TOVALUE(node.getChild(0), sym_table)
    exp2 = TOVALUE(node.getChild(1), sym_table)

    if exp.getValue() <= exp2.getValue():
        return 1
    return 0

def PRINT(node, sym_table):
    exp = node.getChild(0)
    if exp.getType() == exp.TYPE["ACCESS"]:
        exp = TOVALUE(node.getChild(0).execute(sym_table), sym_table)
    else:
        exp = node.getChild(0).execute(sym_table)
        try:
            result = exp.getValue()
            exp = result
        except:
            pass
    if exp:
        sym_table.appendLog(exp)
        return "No value to print"
    return None

def ACCESS(node, sym_table):
    exp = node.getChild(0)
    if exp.getType() == exp.TYPE["ID"]:
        exp = exp.execute(sym_table)
        # now we have sym instance
        if exp:
            exp2 = TOVALUE(node.getChild(1), sym_table)
            exp.setRef(str(exp2.getValue()))
            return exp
        # error
        return None
    else:
        exp = exp.execute(sym_table)
        if exp:
            new_index = exp.getRef()
            exp2 = TOVALUE(node.getChild(1), sym_table)
            exp.setRef(str(new_index) + ',' + str(exp2.getValue()))
            return exp
        # error
        return None

def XOR(node, sym_table):
    return LOGIC('^', node, sym_table)

def MATH(op, node, sym_table):
    exp = TOVALUE(node.getChild(0), sym_table)
    exp2 = TOVALUE(node.getChild(1), sym_table)

    if exp == None or exp2 == None:
            exp = None
    elif exp.getType() == node.TYPE["STRING"] and exp2.getType() == node.TYPE["STRING"] :
        if op == '+':
            exp = str(exp.getValue()) + str(exp2.getValue())
        else:
            # error handling
            exp = "Error at <" + str(exp.getValue()) + "> " + op + " <" + str(exp2.getValue()) + ">"
            sym_table.appendLog(exp)
            exp = None
    elif (exp.getType() == node.TYPE["NUM"] and exp2.getType() == node.TYPE["NUM"]):
        exp = OPERAND(op, int(exp.getValue()), int(exp2.getValue()))
        if type(exp) == str:
            sym_table.appendLog(exp)
            exp = None
    elif (exp.getType() == node.TYPE["NUM"] or exp.getType() == node.TYPE["FLOAT"]) and (exp2.getType() == node.TYPE["NUM"] or exp2.getType() == node.TYPE["FLOAT"]):
        exp = OPERAND(op, float(exp.getValue()), float(exp2.getValue()))
        if type(exp) == str:
            sym_table.appendLog(exp)
            exp = None
    else:
        # error handling
        exp = "Error at <" + str(exp.getValue()) + "> " + op + " <" + str(exp2.getValue()) + ">"
        sym_table.appendLog(exp)
        exp = None
    return exp

def LOGIC(op, node, sym_table):
    exp = TOVALUE(node.getChild(0), sym_table)
    exp2 = TOVALUE(node.getChild(1), sym_table)

    if (exp.getValue() != 0 and exp.getValue() != 1) and (exp2.getValue() != 0 and exp2.getValue() != 1):
        # error handling
        exp = "Error at <" + str(exp.getValue()) + "> " + op + " <" + str(exp2.getValue()) + ">"
        sym_table.appendLog(exp)
        exp = None
    else:
        exp = OPERAND(op, int(exp.getValue()), int(exp2.getValue()))     
    return exp

def OPERAND(op, val, val2):
    if op == '+':
        return val + val2
    elif op == '-':
        return val - val2
    elif op == '*':
        return val * val2
    elif op == '/':
        if val2 != 0:
            return val / val2
        else:
            return "Can't divide by zero"
    elif op == '%':
        if val2 != 0:
            return val % val2
        else:
            return "Can't divide by zero"
    # only for LOGIC
    elif op == '^':
        return val ^ val2
    else:
        return "No recognized operand"

def ASSIGN(node, sym_table):
    exp = node.getChild(0)
    TYPE = exp.TYPE
    if exp.getType() == TYPE["ACCESS"]:
        exp = exp.execute(sym_table)
    exp2 = node.getChild(1)
    if exp2.getType() == TYPE["ARRAY"]:
        exp2 = {}
    else:
        exp2 = exp2.execute(sym_table)
        try:
            if exp2.getType() == TYPE["STRUCT"]:
                identifier = exp2.getID()
                exp2 = sym_table.get(identifier)
                index = exp2.getRef()
                array = exp2.getValue()
                exp2 = array[index]
            result = exp2.getValue()
            exp2 = result
        except:
            pass

    if exp.getType() == TYPE["ID"]:
        identifier = exp.getValue()
        exp = sym_table.get(identifier)
        exp.setValue(exp2) 
        exp.setType(TYPEOF(exp2))
    else:
        # array
        identifier = exp.getID()
        exp = sym_table.get(identifier)
        index = exp.getRef()
        array = exp.getValue()
        array[index] = exp2
        exp.setValue(array)

    sym_table.update(identifier, exp)
    return None

def TYPEOF(value):
    if type(value) == int:
        return "NUM"
    elif type(value) == float:
        return "FLOAT" 
    elif type(value) == str:
        return "STRING"
    elif type(value) == dict:
        return "STRUCT"
    else:
        try:
            value.getRef()
            return "STRUCT"
        except:
            return "NONE"

def TOVALUE(value, sym_table):
    try:
        if value.getType() == value.TYPE["ID"]:
            return value.execute(sym_table)
        elif value.getType() == value.TYPE["ACCESS"]:
            result = value.execute(sym_table)
            index = result.getRef()
            array = result.getValue()
            value = array[index]
            return leaf(array[index], TYPEOF(value))
        return value
    except:
        # error 
        return None