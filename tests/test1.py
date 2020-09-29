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
