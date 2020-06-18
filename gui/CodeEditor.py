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
import tkinter.font as tkFont
from tkinter.ttk import Notebook
from tkinter import Frame, Label, Menu, Message, Text, Scrollbar, PhotoImage, Label, Toplevel, filedialog, messagebox, Button
from gui.TextArea import TextArea as Editor
from gui.AstViewer import showAST
from gui.TableViewer import showTable
import analysis.bottom_up as left
import os
class App:
    # need it for generate reports
    __ast = None
    __sym_table = None

    def __init__(self, ide):

        # setting title
        ide.title("Titus @danii_mor")

        # setting window size
        width=700
        height=400
        screenwidth = ide.winfo_screenwidth()
        screenheight = ide.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        ide.geometry(alignstr)
        ide.resizable(width=True, height=True)

        # create menubar
        menubar = Menu(ide)

        # file menu
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.newFile)
        filemenu.add_command(label="Open", command=self.file_open)
        filemenu.add_command(label="Save", command=self.file_save)
        filemenu.add_command(label="Save as...", command=self.file_save_as)
        filemenu.add_command(label="Close", command=self.exitTab)

        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=ide.quit)
        

        # edit menu
        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Cut", command=self.donothing)
        editmenu.add_command(label="Copy", command=self.copy_to_clipboard)
        editmenu.add_command(label="Paste", command=self.donothing)

        editmenu.add_separator()

        editmenu.add_command(label="Find", command=self.donothing)
        editmenu.add_command(label="Replace", command=self.donothing)


        # run menu
        runmenu = Menu(menubar, tearoff=0)
        runmenu.add_command(label="Top-Down Analysis", command=self.donothing)
        runmenu.add_command(label="Bottom-Up Analysis", command=self.execute_current_tab_lef)

        runmenu.add_separator()

        runmenu.add_command(label="Symbol Table", command=self.show_sym_table)
        runmenu.add_command(label="Error Report", command=self.show_error)
        runmenu.add_command(label="Abstract Syntax Tree", command=self.show_ast)
        runmenu.add_command(label="Grammar", command=self.show_grammar)

        runmenu.add_separator()
        
        runmenu.add_command(label="Debugging", command=self.execute_debug)


        # option menu
        #optionmenu = Menu(menubar, tearoff=0)
        #optionmenu.add_command(label="Theme...", command=self.donothing)
        #optionmenu.add_command(label="Line Numbers...", command=self.donothing)


        # help menu
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help", command=self.donothing)
        helpmenu.add_command(label="About...", command=self.show_info)
        

        # setting menu
        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label="Edit", menu=editmenu)
        menubar.add_cascade(label="Run", menu=runmenu)
        menubar.add_cascade(label="Help", menu=helpmenu)
        ide.config(menu=menubar)

        # setting editor area
        self.tabs = Notebook(ide)
        f1 = Frame(self.tabs)
        self.tabs.add(f1, text="+")
        self.tabs.pack(side="top", fill="both", expand=True, padx=10, pady=0)

        self.tabs.bind("<<NotebookTabChanged>>", self.addTab)


        # setting terminal area
        self.terminal= Text(ide)
        ft = tkFont.Font(family="Lucinda Console", size=10)
        self.terminal["font"] = ft
        self.terminal["wrap"] = "word"
        self.terminal["fg"] = "white"
        self.terminal["bg"] = "black"
        self.terminal["insertbackground"] ="white"
        self.terminal["height"] = 5
        self.terminal["width"] = 5
        self.terminal.pack( side = "left", fill = "both", expand=True,  padx=10, pady=10)

        terminal_scroll = Scrollbar(ide)
        terminal_scroll["orient"] = "vertical"
        terminal_scroll["command"] = self.terminal.yview
        terminal_scroll.pack(side="right", fill="y")

        self.terminal.configure(yscrollcommand=terminal_scroll.set)
        self.terminal.bind("<Return>", self.execute_command)

    def copy_to_clipboard(self):
        selectedTab = self.tabs.index("current")
        currentTextArea = self.tabs.winfo_children()[selectedTab+1].textarea
        try:
            selected_text= currentTextArea.get("sel.first", "sel.last")
            currentTextArea.clipboard_append(selected_text)
        except:
            pass

    def show_grammar(self):
        if self.__sym_table:
            window = Toplevel()
            window['bg'] = 'black'
            productions = self.__sym_table.getGrammar()
            keys = list(productions.keys())
            keys.sort()
            grammar = Message(window)
            txt = ''
            for production in keys:
                txt += productions[production] + '\n' 
            grammar['fg'] = 'white'
            grammar['bg'] = 'black'
            grammar['text'] = txt
            grammar.pack(side='left')
    
    def show_error(self):
        if self.__sym_table:
            if self.__sym_table.error != '':
                window = Toplevel()
                window['bg'] = 'black'

                grammar = Message(window)
                grammar['fg'] = 'white'
                grammar['bg'] = 'black'
                grammar['text'] = self.__sym_table.error
                grammar.pack(side='left')
            else:
                window = Toplevel()
                window['bg'] = 'black'

                grammar = Message(window)
                grammar['fg'] = 'white'
                grammar['bg'] = 'black'
                grammar['text'] = 'Not Errors Found'
                grammar.pack(side='left')

    def show_sym_table(self):
        if self.__sym_table:
            showTable(self.__sym_table)

    def show_ast(self):
        showAST()

    def show_info(self):
        window = Toplevel()
        window['bg'] = 'black'

        grammar = Message(window)
        grammar['fg'] = 'white'
        grammar['bg'] = 'black'
        grammar['text'] = 'Augus code by Engr. Espino\nTitus 1.46.13a Developed by @danii_mor\n 201314810'
        grammar.pack(side='left')

    def update_line_debugg(self, event= None):
        self.count["text"] = "Line: %s" % str(self.c+1)

        # split lines
        selectedTab = self.tabs.index("current")
        currentTextArea = self.tabs.winfo_children()[selectedTab+1].textarea
        lines = currentTextArea.get('1.0','end-1c').split('\n')

        # start execute line by self.c counter
        ply_left = left.parse()
        if self.c < len(lines):
            if "main:" not in lines[self.c]:
                line = "main:" + lines[self.c]
                result  = ply_left(left, line)
                if result:
                    ast = result[0]
                    ast.setType("LABEL")
                    ast.setValue("S")
                    ast.root = result[0]

                    if self.__sym_table != None:
                        new_table =  {**self.__sym_table.printTable(), **result[1].printTable()}
                        for sym_id in new_table:
                            sym = new_table[sym_id]
                            if sym != None:
                                if sym.getValue() == None:
                                    try:
                                        new_table[sym_id] = self.__sym_table.printTable()[sym_id]
                                    except:
                                        pass
                        self.__sym_table.setTable({**self.__sym_table.printTable(), **new_table})
                    else:
                        self.__sym_table = result[1]

                    compute = [None, None]

                    # start execute
                    self.__sym_table.terminal = self.terminal
                    compute = ast.start_execute(self.__sym_table, "MAIN")
                    # lookup the last line
                    index = self.terminal.search(r'\n', "insert", backwards=True, regexp=True)
                    txt = self.terminal.get(str(index),'end-1c')
                    if txt == "":
                        index ="1.0"
                    else:
                        index = self.terminal.index("%s+1c" % index)
                    if compute[0]:
                        self.terminal.insert(str(float(index)+1), compute[0])
                        self.__sym_table.cleanLog()
                    if compute[1]:
                        goto_line = 0
                        for l in lines:
                            if (compute[1]+":") in l:
                                break
                            goto_line = goto_line + 1
                        
                        self.c = goto_line - 1

            if self.__sym_table != None:
                if self.__sym_table.error != '':
                    # lookup the last line
                    index = self.terminal.search(r'\n', "insert", backwards=True, regexp=True)
                    txt = self.terminal.get(str(index),'end-1c')
                    if txt == "":
                        index ="1.0"
                    else:
                        index = self.terminal.index("%s+1c" % index)
                    self.terminal.insert(str(float(index)+1), "\nTitus>> Error Report Generated\n")

            self.c = self.c + 1
            self.label_last_line["text"] = "Line: %s" % str(self.c+1)

    c = 0
    def execute_debug(self, event = None):
        self.__sym_table = None
        self.c = 0
        # create debug player
        window = Toplevel()
        window['bg'] = 'black'

        label_count = Label(window, text="Execute Now:", 
                            borderwidth=0, width=10, bg = "black", fg = "white")
        label_count.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)

        label_last = Label(window, text="Executed Before:", 
                            borderwidth=0, width=10, bg = "black", fg = "white")
        label_last.grid(row=0, column=2, sticky="nsew", padx=1, pady=1)

        self.label_last_line = Label(window, text="Line: 1", 
                            borderwidth=0, width=10, bg = "black", fg = "white")
        self.label_last_line.grid(row=1, column=0, sticky="nsew", padx=1, pady=1)

        execute = Button(window, text='>',
                                   command=self.update_line_debugg)
        execute.grid(row=1, column=1, sticky="nsew", padx=1, pady=1)

        self.count = Label(window, text="Line: 0", 
                            borderwidth=0, width=10, bg = "black", fg = "white")
        self.count.grid(row=1, column=2, sticky="nsew", padx=1, pady=1)

        window.grid_columnconfigure(0, weight=1)
        window.grid_columnconfigure(1, weight=1)
        window.grid_columnconfigure(2, weight=1)
        window.resizable(width=True, height=False)

    def execute_current_tab_lef(self):
        selectedTab = self.tabs.index("current")
        currentTextArea = self.tabs.winfo_children()[selectedTab+1].textarea
        input = currentTextArea.get('1.0','end-1c')
        ply_left = left.parse()
        result  = ply_left(left, input)
        if result:
            self.__ast = result[0]
            self.__ast.setType("LABEL")
            self.__ast.setValue("S")
            self.__ast.root = result[0]
            self.__ast.graph()
            self.__sym_table = result[1]
            self.__sym_table.error != ''
            goto_called = True
            start_from = "MAIN"
            compute = [None, None]
            while goto_called:
                goto_called = False
                self.__sym_table.terminal = self.terminal
                compute = self.__ast.start_execute(self.__sym_table, start_from)
                # lookup the last line
                index = self.terminal.search(r'\n', "insert", backwards=True, regexp=True)
                txt = self.terminal.get(str(index),'end-1c')
                if txt == "":
                    index ="1.0"
                else:
                    index = self.terminal.index("%s+1c" % index)
                if compute[0]:
                    self.terminal.insert(str(float(index)+1), compute[0])
                    self.__sym_table.cleanLog()
                if compute[1]:
                    goto_called = True
                    start_from = compute[1]
            
            if self.__sym_table.error != '':
                # lookup the last line
                index = self.terminal.search(r'\n', "insert", backwards=True, regexp=True)
                txt = self.terminal.get(str(index),'end-1c')
                if txt == "":
                    index ="1.0"
                else:
                    index = self.terminal.index("%s+1c" % index)
                self.terminal.insert(str(float(index)+1), "\nTitus>> Error Report Generated\n")
    
    def execute_command(self, event):
        # lookup the last line
        index = self.terminal.search(r'\n', "insert", backwards=True, regexp=True)
        input = self.terminal.get(str(index),'end-1c')
        if input == "":
            index ="1.0"
        else:
            index = self.terminal.index("%s+1c" % index)
        input = self.terminal.get(index,'end-1c')
        # send the input to the calculate 
        self.__sym_table.read_input.set(input)

    def newFile(self):
        lastindex = self.tabs.index("end")-1

        textarea = Editor(self.tabs)
        self.tabs.insert(lastindex, textarea, text="Tab" + str(lastindex+1))
        self.tabs.select(lastindex)

    def exitTab(self):
        result = self.save_if_modified()
        if result != None: #None => Aborted or Save cancelled, False => Discarded, True = Saved or Not modified
            selectedTab = self.tabs.index("current")
            currentTab = self.tabs.winfo_children()[selectedTab+1]
            
            self.tabs.select(self.tabs.winfo_children()[selectedTab])
            currentTab.destroy()

    def save_if_modified(self, event=None):
        selectedTab = self.tabs.index("current")
        currentTextArea = self.tabs.winfo_children()[selectedTab+1].textarea
        if currentTextArea.edit_modified(): #modified
            response = messagebox.askyesnocancel("Save?", "This document has been modified. Do you want to save changes?") #yes = True, no = False, cancel = None
            if response: #yes/save
                result = self.file_save()
                if result == "saved": #saved
                    return True
                else: #save cancelled
                    return None
            else:
                return response #None = cancel/abort, False = no/discard
        else: #not modified
            return True

    def file_open(self, event=None, filepath=None):
        if filepath == None:
            filepath = filedialog.askopenfilename()
        if filepath != None  and filepath != '':
            with open(filepath, encoding="utf-8") as f:
                fileContents = f.read()# Get all the text from file.           
            # Set current text to a new Tab file contents
            lastindex = self.tabs.index("end")-1

            textarea = Editor(self.tabs)
            self.tabs.insert(lastindex, textarea, text="Tab" + str(lastindex+1))
            self.tabs.select(lastindex)

            textarea.textarea.insert(1.0, fileContents)
            textarea.textarea.edit_modified(False)
            tab_tittle = os.path.basename(filepath)
            self.tabs.tab(lastindex, text = tab_tittle)

    def file_save(self, event=None):
        selectedTab = self.tabs.index("current")
        currentName = self.tabs.tab(selectedTab, "text")
        if 'Tab' in currentName:
            result = self.file_save_as()
        else:
            result = self.file_save_as(filepath='./' + currentName)
        return result

    def file_save_as(self, event=None, filepath=None):
        if filepath == None:
            filepath = filedialog.asksaveasfilename(filetypes=(('Text files', '*.txt'), ('Titus files', '*.ti'), ('All files', '*.*'))) #defaultextension='.txt'
        try:
            with open(filepath, 'wb') as f:
                selectedTab = self.tabs.index("current")
                currentTextArea = self.tabs.winfo_children()[selectedTab+1].textarea
                text = currentTextArea.get(1.0, "end-1c")
                f.write(bytes(text, 'UTF-8'))
                currentTextArea.edit_modified(False)
                tab_tittle = os.path.basename(filepath)
                self.tabs.tab(selectedTab, text = tab_tittle)
                return "saved"
        except FileNotFoundError:
            print('Titus>> File Not Found Error')
            return "cancelled"

    def addTab(self, event):
        selectedTab = self.tabs.index("current")
        lastindex = self.tabs.index("end")-1

        if selectedTab == lastindex :
            textarea = Editor(self.tabs)
            self.tabs.insert(lastindex, textarea, text="Tab" + str(lastindex+1))
            self.tabs.select(lastindex)

    def donothing(self):
        print("clicked")
