# pylint: disable=W,import-error
import ply.lex as lex
import ply.yacc as yacc
from syntax_tree.branch import branch as branch
from syntax_tree.leaf import leaf as leaf
'''
s -> code

code -> code LABEL ':' list
      | MAIN ':' list

list -> list statement ';'
      | statement ';'

statement -> is_array_term '='  expression 
            | PRINT '(' term ')'
            | UNSET '(' term ')'
            | IF '(' expression ')' GOTO LABEL
            | GOTO LABEL
            | EXIT

term -> is_array_term
        | NUMBER 
        | FLOAT 

is_array_term -> is_array_term '[' term ']'
	  	| NAME

expression -> term '+' term
            | term '-' term
            | term '*' term
            | term '/' term
            | term '%' term
            | term '&' term 
            | term '|' term
            | term '^' term
            | term '<' term
            | term '>' term
            | term XOR term

            | term '&''&' term
            | term '|''|' term
            | term '<''<' term
            | term '>''>' term
            | term '!''=' term
            | term '=''=' term
            | term '>''=' term
            | term '<''=' term
            
            | '(' INT ')' term
            | '(' FLOAT ')' term
            | '(' CHAR ')' term
            | ABS '(' term ')'
            | '~' term
            | '!' term
            | ARRAY '(' ')'
            | term
'''


def parse():
    # tokenizing rules
    reserved = {
                'main'  : 'MAIN',
                'if'    : 'IF',
                'print' : 'PRINT',
                'abs'   : 'ABS',
                'goto'  : 'GOTO',
                'xor'   : 'XOR',
                'read'  : 'READ',
                'unset' : 'UNSET',
                'array' : 'ARRAY',
                'int'   : 'INT',
                'float' : 'FLOAT',
                'char'  : 'CHAR',
                'exit'  : 'EXIT'
                }

    tokens = [
                'NAME',
                'NUMBER',
                'DECIMAL',
                'LABEL'
            ] + list(reserved.values())

    literals = ['=', '+', '-', '*', '/', '%', '&', '|', '^', '<', '>', '!', '~', '(', ')', '[', ']', ';', ':'] 

    t_ignore = " \t"

    t_NAME = r'[$] ( [tavTAV][0-9]*| s(p|[0-9]*) | ra)'

    t_ignore_COMMENT = r'[#].*'

    def t_NUMBER(t):
        r'\d+'
        t.value = int(t.value)
        return t
    
    def t_DECIMAL(t):
        r'\d+[.]\d+'
        t.value = float(t.value)
        return t

    def t_LABEL(t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        # check if reserved word
        if t.value in reserved:
            t.type = reserved.get(t.value)    
        return t

    def t_newline(t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def find_column(input, token):
        line_start = input.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1

    # build the lexer
    lexer = lex.lex()

    # parsing rules

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS')
    )

    def p_code(p):
        '''code : code LABEL ":" list
                | MAIN ":" list '''
        global __ast
        if len(p) == 4:
            p[3].setType("LABEL")
            p[3].setValue("MAIN")
            __ast.add(p[3])
        else:
            p[4].setType("LABEL")
            p[4].setValue(str(p[2]))
            __ast.add(p[4])
        p[0] = __ast

    def p_statement_list(p):
        '''list : list statement ";" 
                | statement  ";" '''

        if len(p) == 3:
            new_branch = branch()
            new_branch.add(p[1])
            p[0] = new_branch
        else:
            p[1].add(p[2])
            p[0] = p[1]

    def p_statement_assign(p):
        'statement : is_array_term "=" expression'

        l_leaf = p[1]
        r_leaf = p[3]

        new_branch = branch()
        new_branch.add(l_leaf)
        new_branch.add(r_leaf)
        new_branch.setType("ASSIGN")

        p[0] = new_branch

    def p_statement_expr(p):
        'statement : PRINT "(" term  ")" '
        leaf = p[3]
        new_branch = branch()
        new_branch.add(leaf)
        new_branch.setType("PRINT")

        p[0] = new_branch

    def p_expression_binop(p):
        '''expression : term '+' term
                      | term '-' term
                      | term '*' term
                      | term '/' term
                      | term '%' term
                      | term '&' term
                      | term '|' term
                      | term '^' term
                      | term '<' term
                      | term '>' term
                      | term XOR term
                      '''
        l_leaf = p[1]
        r_leaf = p[3]

        new_branch = branch()
        new_branch.add(l_leaf)
        new_branch.add(r_leaf)

        if p[2] == '+':
            new_branch.setType("ADD")
        elif p[2] == '-':
            new_branch.setType("SUB")
        elif p[2] == '*':
            new_branch.setType("MUL")
        elif p[2] == '/':
            new_branch.setType("DIV")
        elif p[2] == '%':
            new_branch.setType("MOD")
        elif p[2] == '&':
            new_branch.setType("BAND")
        elif p[2] == '|':
            new_branch.setType("BOR")
        elif p[2] == '^':
            new_branch.setType("BXOR")
        elif p[2] == '<':
            new_branch.setType("LTHAN")
        elif p[2] == '>':
            new_branch.setType("GTHAN")
        else:
            new_branch.setType("XOR")
        p[0] = new_branch

    def p_expression_binop2(p):
        '''expression : term '&' '&' term
                      | term '|' '|' term
                      | term '<' '<' term
                      | term '>' '>' term
                      | term '!' '=' term
                      | term '=' '=' term
                      | term '<' '=' term
                      | term '>' '=' term
                                    '''
        l_leaf = p[1]
        r_leaf = p[4]

        new_branch = branch()
        new_branch.add(l_leaf)
        new_branch.add(r_leaf)

        if p[2] == '&':
            new_branch.setType("OR")
        elif p[2] == '|':
            new_branch.setType("OR")
        elif p[2] == '<' and p[3] == '<':
            new_branch.setType("SLEFT")
        elif p[2] == '>' and p[3] == '>':
            new_branch.setType("SRIGHT")
        elif p[2] == '!':
            new_branch.setType("NOEQUAL")
        elif p[2] == '=':
            new_branch.setType("EQUAL")
        elif p[2] == '<' and p[3] == '=':
            new_branch.setType("LE_OP")
        elif p[2] == '>' and p[3] == '=':
            new_branch.setType("GE_OP")
        else:
            new_branch.setType("XOR")

    def p_expression(p):
        'expression : term '
        p[0] = p[1]

    def p_term_uminus(p):
        "term : '-' number %prec UMINUS"
        number = p[2].getValue()
        p[2].setValue( number * -1)
        p[0] = p[2]
    
    def p_term_group(p):
        '''term : '(' INT ')' term
                | '(' FLOAT ')' term
                | '(' CHAR ')' term
                | '(' term ')'
                | '~' term
                | '!' term
                | ABS '(' term ')'
                | ARRAY '(' ')'
                | factor        
                                '''
        new_branch = branch()
        if p[1] == '(':
            l_leaf = p[4]
            new_branch.add(l_leaf)
            if p[2].type == 'INT':
                new_branch.setType("TOINT")
            elif p[2].type == 'FLOAT':
                new_branch.setType("TOFLOAT")
            elif p[2].type == 'CHAR':
                new_branch.setType("TOCHAR")
            else:
                new_branch = p[2]
        elif p[1] == '~':
            l_leaf = p[2]
            new_branch.add(l_leaf)
            new_branch.setType("BNOT")
        elif p[1] == '!':
            l_leaf = p[2]
            new_branch.add(l_leaf)
            new_branch.setType("NOT")
        #TODO fix how to check this two cases
        elif p[1] == 'ABS':
            l_leaf = p[3]
            new_branch.add(l_leaf)
            new_branch.setType("ABS")
        elif p[1] == 'ARRAY':
            new_branch.setType("ARRAY")
        ##
        else:
            new_branch = p[1]

        p[0] = new_branch

    def p_expression_number(p):
        'number : NUMBER'
        l_leaf = leaf(p[1], "NUM")
        p[0] = l_leaf

    def p_expression_decimal(p):
        'number : DECIMAL'
        l_leaf = leaf(p[1], "FLOAT")
        p[0] = l_leaf

    def p_term_array(p):
        '''is_array_term : is_array_term '[' term ']'
	  	                | NAME
                                                '''
        if len(p) > 2:
            new_branch = branch()
            new_branch.add(p[1])
            new_branch.add(p[3])
            new_branch.setType("ACCESS")
            p[0] = new_branch
        else:
            l_leaf = leaf(p[1], "ID")
            p[0] = l_leaf

    def p_factor_id(p):
        "factor : is_array_term"
        p[0] = p[1]

    def p_factor_number(p):
        "factor : number"
        p[0] = p[1]

    def p_error(p):
        if p:
            global __text
            print("Syntax error at '" + str(p.value) + "', line:" + str(p.lineno) + ", column:" + str(find_column(__text, p)))
        else:
            print("Syntax error at EOF")

    # build the parser
    parser = yacc.yacc()

    # called when send param to parser function
    def input(self, text):
        global __ast
        global __text
        __ast = branch()
        __text = text
        result = parser.parse(text, lexer=lexer)
        return result

    return input
