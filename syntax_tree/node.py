#▓█████▄  ▄▄▄       ███▄    █ ▒██░ ██░ ███▄ ▄███░ ▒█████   ██▀███  
#▒██▀ ██▌▒████▄     ██ ▀█   █ ▒██▒▒██▒▓██▒▀█▀ ██▒▒██▒  ██▒▓██ ▒ ██▒
#░██   █▌▒██  ▀█▄  ▓██  ▀█ ██▒▒██▒▒██▒▓██    ▓██░▒██░  ██▒▓██ ░▄█ ▒
#░▓█▄   ▌░██▄▄▄▄██ ▓██▒  ▐▌██▒░██░░██░▒██    ▒██ ▒██   ██░▒██▀▀█▄  
#░▒████▓  ▓█   ▓██▒▒██░   ▓██░░██░░██░▒██▒   ░██▒░ ████▓▒░░██▓ ▒██▒
# ▒▒▓  ▒  ▒▒   ▓▒█░░ ▒░   ▒ ▒ ░▓  ░▓  ░ ▒░   ░  ░░ ▒░▒░▒░ ░ ▒▓ ░▒▓░
# ░ ▒  ▒   ▒   ▒▒ ░░ ░░   ░ ▒░ ▒ ░ ▒ ░░  ░      ░  ░ ▒ ▒░   ░▒ ░ ▒░
# ░ ░  ░   ░   ▒      ░   ░ ░  ▒ ░ ▒ ░░      ░   ░ ░ ░ ▒    ░░   ░ 
#   ░          ░  ░         ░  ░   ░         ░       ░ ░     ░     
import os
import subprocess as command
import sys
from graphviz import Digraph

class node():
    TYPE = {
        #leaf
		"ID"    : 0, 
		"NUM"   : 1,
        "FLOAT" : 2,
        "STRING": 3, 
		"STRUCT": 4,
		#root
		"IF"    : 5, 
		"PRINT" : 6,
		"ADD"   : 7,
		"SUB"   : 8,
		"MUL"   : 9,
		"DIV"   : 10,
		"POT"   : 11,
		"MOD"   : 12,
		"POINT" : 13,
		"GTHAN" : 14,
		"GE_OP" : 15,
		"LTHAN" : 16,
		"LE_OP" : 17,
		"EQUAL" : 18,
		"NOT"   : 19,
		"AND"   : 20,
		"OR"    : 21,
		"NOEQUAL":22,
        "GOTO"  : 23,
        "ASSIGN": 24,
        "LABEL" : 25,
        "BNOT"  : 26,
        "BAND"  : 27,
        "BOR"   : 28,
        "BXOR"  : 29,
        "SLEFT" : 30,
        "SRIGHT": 31,
        "TOINT" : 32,
        "TOFLOAT":33,
        "TOCHAR": 34,
        "ABS"   : 35,
        "ARRAY" : 36,
        "ACCESS": 37,
        "UNSET" : 38,
        "EXIT"  : 39,
        "READ"  : 40,
        "XOR"   : 41
		}

    _value = None
    _type = None
    __contador = 0
    root = None

    # calls all for make the ast

    def graph(self):
        # make dir dot if not exist
        dot_path = r'./dot/' 
        if not os.path.exists(dot_path):
            os.makedirs(dot_path)

        # dir for generated files
        dot_file = r'./dot/ast.dot'
        png_file = r'./dot/ast.gif'
        
        if self.root != None:
            # dot generation
            self.__build_dot(dot_file)       
            
            # png generation 
            self.__build_png(dot_file, png_file)
        else:
            print("AST>> is empty")
    
    def __build_dot(self, dot_file):
        self.__contador = 0
        # setting digraph
        buffer = Digraph(comment='Titus v1.0.0 by @danii_mor', node_attr={'style': 'filled', 'fontcolor': 'white' })        
        buffer.graph_attr['bgcolor'] = 'black'
        buffer.edge_attr.update(color='grey')

        # node generation
        self.__mk_nodes(self.root, buffer)

        self.__contador = 1
        # node binding
        self.__bind_nodes(self.root, buffer, 0)  

        # file generation
        self.__mk_file(dot_file, str(buffer.source))

    def __mk_nodes(self, top_node, buffer):      
        if top_node.getType() > 4:
            buffer.node('node' + str(self.__contador),  str(top_node.getValue()), color='brown4', shape='house')
            self.__contador += 1
        else:
            buffer.node('node' + str(self.__contador),  str(top_node.getValue()), shape='egg', color='darkolivegreen')
            self.__contador += 1

        x = 0
        y = 0

        hijo = top_node.getChild(y)
        y += 1 
        padre = top_node

        while padre != None:
            while hijo != None:
                self.__mk_nodes(hijo,buffer)
                hijo = padre.getChild(y)
                y += 1
        
            padre = padre.getChild(x)
            x += 1

    def __bind_nodes(self, top_node, buffer, cpadre):
        y = 0
        
        hijo = top_node.getChild(y)
        y += 1
        padre = top_node
        
        while hijo != None:
            buffer.edge('node' + str(cpadre), 'node' + str(self.__contador))        
            
            self.__contador += 1
            self.__bind_nodes(hijo, buffer, self.__contador-1)
            
            
            hijo = padre.getChild(y)
            y += 1
        
    def __build_png(self, ruta_dot, ruta_png):
        tParam = "-Tgif"   
        tOParam = "-o"        
        
        cmd = [
            self.__verify_os(),
            tParam,
            ruta_dot,
            tOParam,
            ruta_png
            ]
        if cmd[0] != None:
            try:
                command.run(cmd)                            
            except:
                print("AST>> export to png error")
        
    def __verify_os(self):
        if sys.platform.startswith("win"):
            return "./graphviz_port/bin/dot.exe"
        elif sys.platform.startswith("linux") or sys.platform.startswith("aix"):
            return "dot"
        else:
            print("Titus>> OS:" + str(sys.platform) + " not supported")
    
        return None

    def __mk_file(self, dot_file, buffer):
        with open(dot_file, "w+") as f:
            f.write(buffer)
