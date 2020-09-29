import tkinter as tk

from tkdata import TkData

schema = {
    "group_1": {"type": "group", "pos": {"row": 0, "column": 0, "columnspan": 2}, "children": {
        "group_1.1": {"type": "frame", "pos": {"row": 0, "column": 0}, "children": {
            "str_field_with_label": { "type": "str", "label": "String Field" },
            "str_field_no_label": { "type": "str" }
        }},
        "group_1.2": {"type": "frame", "pos": {"row": 0, "column": 1}, "children": {
            "int_field": { "type": "int" },
            "float_field": { "type": "float" }
        }}
    }},
    "group_2": {"type": "frame", "pos": {"row": 1, "column": 0}, "children": {
        "bool_field": { "type": "bool" },
        "choice_field": { 
            "type": "choice",
            "values": ["option 1", "option 2", "option 3"]
        }
    }},
    "group_3": {"type": "frame", "pos": {"row": 1, "column": 1}, "children": {
        "file_field": { "type": "file" },
        "folder_field": { "type": "folder" },
        "button": { "type": "button", "text": "Print dict" }
    }}
}

gui = TkData(schema)

def show_message(event):
    window = tk.Toplevel(master=gui)
    message = tk.Message(master=window, text=str(gui.d))
    message.pack(fill='x', padx=10, pady=10)

gui.s['group_3']['button'].bind('<Button-1>', show_message)
gui.mainloop()