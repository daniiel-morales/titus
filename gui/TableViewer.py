# pylint: disable=import-error
from tkinter import Toplevel, Label
from syntax_tree.leaf import leaf
def showTable(table):
    # use black background so it "peeks through" to 
    # form grid lines
    window = Toplevel()
    window._widgets = []

    # setting headers
    row = 0
    current_row = []
    ins_tuple = ["IDENTIFIER", "TYPE", "SIZE", "VALUE", "SCOPE", "REFERENCE"]
    for column in range(6):
        label = Label(window, text="%s" % ins_tuple[column], 
                            borderwidth=0, width=10, bg = "black", fg = "white")
        label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
        current_row.append(label)
    window._widgets.append(current_row)
    row += 1

    # setting content
    for key in table.printTable():
        #current_row = []
        ins = table.get(key)
        typ = ["INT", "FLOAT", "STRING", "STRUCT"]
        is_label = ins.getType()
        is_pointer = ins.getValue()
        is_struct = ins.getSize()
        ref = ins.getRef()
        if type(is_label) == str:
            typ = "FUNCTION"
            ref = "LABEL"
        elif type(is_pointer) == leaf:
            typ = "POINTER"
            is_pointer = is_pointer.getValue()
        else:
            typ = typ[is_label-1]
            if typ == "STRUCT":
                is_struct = len(is_pointer)
        ins_tuple = [ins.getID(), typ, is_struct, is_pointer, ins.getScope(), ref]
        for column in range(6):
            label = Label(window, text="%s" % ins_tuple[column], 
                                borderwidth=0, width=10, bg = "black", fg = "lightgrey")
            label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
            current_row.append(label)
        window._widgets.append(current_row)
        row += 1

    for column in range(6):
        window.grid_columnconfigure(column, weight=1)

    window.resizable(width=True, height=False)

def __set(window, row, column, value):
    widget = window._widgets[row][column]
    widget.configure(text=value)