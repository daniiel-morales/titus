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
from tkinter import Frame, Label, Menu, Message, Text, Scrollbar
from gui.TextArea import TextArea as Editor

import analysis.bottom_up as left

class App:
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
        filemenu.add_command(label="New", command=self.donothing)
        filemenu.add_command(label="Open", command=self.donothing)
        filemenu.add_command(label="Save", command=self.donothing)
        filemenu.add_command(label="Save as...", command=self.donothing)
        filemenu.add_command(label="Close", command=self.donothing)

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

        runmenu.add_command(label="Sym Table", command=self.donothing)
        runmenu.add_command(label="Error Report", command=self.donothing)
        runmenu.add_command(label="Debugging", command=self.donothing)


        # option menu
        optionmenu = Menu(menubar, tearoff=0)
        optionmenu.add_command(label="Font...", command=self.donothing)
        optionmenu.add_command(label="Bottom-Up Analysis", command=self.donothing)


        # help menu
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help", command=self.donothing)
        helpmenu.add_command(label="About...", command=self.donothing)
        

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

    def execute_current_tab_lef(self):
        selectedTab = self.tabs.index("current")
        currentTextArea = self.tabs.winfo_children()[selectedTab+1].textarea
        index = self.terminal.search(r'\n', "insert", backwards=True, regexp=True)
        input = currentTextArea.get('1.0','end-1c')
        ply_left = left.parse()
        result  = ply_left(left, input)
        if result:
            self.terminal.insert(str(float(index)+1), result)
        

    # parser instance for terminal
    ply_left = left.parse()
    
    def execute_command(self, event):
        # lookup the last line
        index = self.terminal.search(r'\n', "insert", backwards=True, regexp=True)
        input = self.terminal.get(str(index),'end-1c')
        if input == "":
            index ="1.0"
        else:
            index = self.terminal.index("%s+1c" % index)
        input = self.terminal.get(index,'end-1c')
        result  = self.ply_left(input)
        if result:
            self.terminal.insert(str(float(index)+1), "\n")
            self.terminal.insert(str(float(index)+1), result)

    def addTab(self, event):
        selectedTab = self.tabs.index("current")
        lastindex = self.tabs.index("end")-1

        if selectedTab == lastindex :
            textarea = Editor(self.tabs)
            self.tabs.insert(lastindex, textarea, text="Tab" + str(lastindex+1))
            self.tabs.select(lastindex)

    def donothing(self):
        print("clicked")
