# tkdata

Create Tkinter forms easily. This library allows you to create a Tkinter GUI easily from a dict containing the structure of the window. This library lets you only create a limited set of widgets, namely: 

1. An entry to get a string.
1. An entry to get an integer.
1. An entry to get a float.
1. A checkbox to get a boolean.
1. A combobox to get a string from a set of choices.
1. A widget to select a file (and get a string of its path).
1. A widget to select a folder (and get a string of its path).

You can group these widgets, and even group multiple groups of widgets. You can specify the position of these groups in a grid inside the window too.

## Installation

```pip install tkdata```

## How to use it

Here is an example on how to use it:

```
from tkdata import TkData

# Schema of the program
schema = {
    "str_field": {
        "type": "str",
        "default": "Default value for str_field",
        "help": "Explanation about what string_field variable means",
        "label": "String Field"
    },
    "int_field": {
        "type": "int",
        "default": 1,
        "help": "Explanation about what int_field variable means",
        "label": "Integer Field"
    },
    "float_field": {
        "type": "float",
        "default": 1.0,
        "help": "Explanation about what float_field variable means",
        "label": "Float Field"
    },
    "bool_field": {
        "type": "bool",
        "default": True,
        "help": "Explanation about what bool_field variable means",
        "label": "Boolean Field"
    },
    "choice_field": {
        "type": "choice",
        "values": ["option 1", "option 2", "option 3"],
        "default": "option 1",
        "help": "Explanation about what choice_field variable means",
        "label": "Choice Field"
    },
    "file_field": {
        "type": "file",
        "default": "/path/to/file.extension",
        "help": "Explanation about what file_field variable means",
        "label": "File Field"
    },
    "folder_field": {
        "type": "folder",
        "default": "/path/to/folder/",
        "help": "Explanation about what folder_field variable means",
        "label": "Folder Field"
    },
    "button": {
        "type": "button",
        "text": "text inside the button"
    }
}

# Create TkData instance with the schema dict. If This can not be done after TkData
# intantiation, you can use gui.init(schema) function after it.
gui = TkData(schema)

# Get the data from the tkdata interface
args = gui.d

# Assign a function to a button named "button" specified in the schema.
# In this example, when the button is clicked all the data dict is printed 
gui.s['button'].bind('<Button-1>', lambda e: print(args))

# Start the loop of tkinter
gui.mainloop()

```
This code will show a Tkinter GUI with widgets to modify each element specified in the schema (except the button widget).

In the following example we show how to group widgets and set the location of each group.
```
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
```

In this example group_2 and group_3 are of type **frame**, a type to group widgets; and group_1 is of type **group**, a type to group multiple **frame**s. To position frames and groups you have to use same options for placing widgets inside a grid on Tkinter, and place these options in a dict inside the schema of the frame or group with the attribute **pos**. This is shown in the last example.

## To do
1. Add more widgets.
2. Add a way to make validation on the fields.