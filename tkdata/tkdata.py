import json
import tkinter as tk
from tkinter import ttk
from pathlib import Path
import tkinter.filedialog
import tkinter.messagebox


class TkData(tk.Tk):
    def __init__(self, schema=None, **kwargs):
        super().__init__(**kwargs)
        if not schema is None:
            self.init(schema)

    def get_schema(self, schema):
        if isinstance(schema, str):
            with Path(schema).open() as f:
                schema = json.load(f)

        if not isinstance(schema, dict):
            raise AttributeError(
                'schema must be a dict or a json file path containing a dict'
            )

        return schema

    def init(self, schema):
        schema = self.get_schema(schema)
        self.d = {}
        self.s = {}
        self.new_frame(schema, self, self.d, self.s)

    def insert_label(self, frame, value, key):
        label = tk.Label(master=frame, text=value.pop('label', key),
            font=('Helvetica', 9, 'bold'), anchor='w'
        )
        label.pack(fill='both', pady=(10,0), padx=10)
        if 'help' in value:
            label.bind("<Button-1>", lambda e, m=value['help']: self.show_message(m))

    def new_frame(self, schema, frame, data, sch):
        max_cols = 0
        max_rows = 0
        is_grid = False
        for key, value in schema.items():
            type_ = value.pop('type', '')
            if type_ == 'frame' or type_ == 'group':
                is_grid = True
                children = value.pop('children', {})
                pos = value.pop('pos', {})
                new_frame = tk.Frame(master=frame, borderwidth=1,
                    relief='raised')
                new_frame.grid(sticky="nsew", **pos)

                max_cols = max(max_cols,
                    pos.get('column', 0) + pos.get('columnspan', 1))
                max_rows = max(max_rows,
                    pos.get('row', 0) + pos.get('rowspan', 1))

                
                tk.Label(master=new_frame, text=value.pop('label', key),
                    font=('Helvetica', 11, 'bold')
                ).pack(fill='x', pady=4)

                if type_ == 'group':
                    new_frame = tk.Frame(master=new_frame)
                    new_frame.pack(fill='both', expand=True)

                sch[key] = {'__frame__': new_frame}
                data[key] = {}
                self.new_frame(children, new_frame, data[key], sch[key])
                continue

            default = value.pop('default', None)
            data[key] = None
            if type_ == 'str':
                self.insert_label(frame, value, key)

                sch[key] = tk.Entry(master=frame, validate='all',
                    validatecommand=(self.register(
                        lambda v, d=data, k=key: \
                            self.validate_entry(v, d, k)), '%P'
                    )
                )

                if value.get('password', False):
                    sch[key].config(show="*")

                sch[key].pack(fill='x', padx=10)

                if isinstance(default, str):
                    sch[key].insert(0, default)
                    data[key] = default

            elif type_ == 'int':
                self.insert_label(frame, value, key)
                kind = value.pop('kind', 'regular')
                sch[key] = tk.Entry(master=frame, validate='all',
                    validatecommand=(self.register(
                        lambda v, d=data, k=key: \
                            self.validate_entry(v, d, k, int)), '%P'
                    )
                )

                sch[key].pack(fill='x', padx=10)

                if isinstance(default, int):
                    sch[key].insert(0, str(default))
                    data[key] = default

            elif type_ == 'float':
                self.insert_label(frame, value, key)
                sch[key] = tk.Entry(master=frame, validate='all',
                    validatecommand=(self.register(
                        lambda v, d=data, k=key: \
                            self.validate_entry(v, d, k, float)), '%P'
                    )
                )

                sch[key].pack(fill='x', padx=10)

                if isinstance(default, float):
                    sch[key].insert(0, str(default))
                    data[key] = default

            elif type_ == 'bool':
                data[key] = False

                frm = tk.Frame(master=frame)
                frm.pack(fill='x', padx=10)

                tk.Label(master=frm, text=value.pop('label', key),
                    font=('Helvetica', 9, 'bold')
                ).pack(side='left')

                sch[key] = tk.Checkbutton(master=frm, text='',
                    command=lambda d=data, k=key: self.change_bool(d, k)
                )
                sch[key].pack(side='left')

                tk.Label(master=frm, text='').pack(fill='x',
                    side='left', expand=True)

                if isinstance(default, bool):
                    data[key] = default
                    if default: sch[key].select()

            elif type_ == 'choice':
                self.insert_label(frame, value, key)
                values = value.pop('values', [])

                sch[key] = ttk.Combobox(master=frame, values=values)
                sch[key].pack(fill='x', padx=10)
                sch[key].bind("<<ComboboxSelected>>",
                    lambda e, s=sch[key], d=data, k=key: \
                        self.change_choice(s,d,k)
                )
                sch[key].current()
                if isinstance(default, str):
                    sch[key].current(values.index(default))
                    data[key] = default

            elif type_ == 'file' or type_ == 'folder':
                self.insert_label(frame, value, key)
                frm = tk.Frame(master=frame)
                frm.pack(fill='x', padx=10)

                sch[key] = tk.Label(master=frm, relief='sunken',
                    borderwidth=1, anchor='w')
                sch[key].pack(fill='both', side='left', expand=True)

                tk.Button(
                    master=frm,
                    text='...',
                    command=lambda s=sch[key], d=data, k=key, t=type_: \
                        self.select_folder(s, d, k, t),
                    padx=0,
                    pady=0
                ).pack(side=tk.LEFT)

                if isinstance(default, str):
                    sch[key]['text'] = default
                    data[key] = default

            elif type_ == 'button':
                sch[key] = tk.Button(
                    master=frame,
                    text=value.pop('text', key)
                )
                sch[key].pack(fill='x', padx=10)
                del data[key]

        if is_grid:
            frame.columnconfigure(list(range(max_cols)), weight=1)
            frame.rowconfigure(list(range(max_rows)), weight=1)
        else:
            try: tk.Label(master=frame, text=" ").pack()
            except: pass

    def validate_entry(self, str_value, data, key, type_=str):
        if str_value == '':
            data[key] = None
            return True
        try:
            data[key] = type_(str_value)
            return True
        except:
            return False

    def change_bool(self, data, key):
        data[key] = not data[key]

    def change_choice(self, elem, data, key):
        data[key] = elem.get()

    def select_folder(self, elem, data, key, kind):
        if kind == 'folder':
            res = tk.filedialog.askdirectory()
        elif kind == 'file':
            res = tk.filedialog.askopenfilename()

        if res:
            elem['text'] = res
            data[key] = res

    def show_message(self, message):
        window = tk.Toplevel(master=self)
        window.title('Help')
        label = tk.Message(master=window, text=message)
        label.pack(fill='x', padx=10, pady=10)