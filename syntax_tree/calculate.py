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

def XOR(node, sym_table):
    return LOGIC('^', node, sym_table)

def MATH(op, node, sym_table):
    exp = node.getChild(0)
    if exp.getType() == node.TYPE["ID"]:
        exp = exp.execute(sym_table)

    exp2 = node.getChild(1)
    if exp2.getType() == node.TYPE["ID"]:
        exp2 = exp2.execute(sym_table)

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
    exp = node.getChild(0)
    if exp.getType() == node.TYPE["ID"]:
        exp = exp.execute(sym_table)

    exp2 = node.getChild(1)
    if exp2.getType() == node.TYPE["ID"]:
        exp2 = exp2.execute(sym_table)

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
    if exp.getType() == exp.TYPE["ACCESS"]:
        exp = exp.execute(sym_table)
    exp2 = node.getChild(1).execute(sym_table)

    identifier = exp.getValue()
    exp = sym_table.get(identifier)
    exp.setValue(exp2) 
    exp.setType(TYPEOF(exp2))
    sym_table.update(identifier, exp)
    return None

def TYPEOF(value):
    if type(value) == int:
        return "NUM"
    elif type(value) == float:
        return "FLOAT" 
    elif type(value) == str:
        return "STRING"