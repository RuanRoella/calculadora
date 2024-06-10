import tkinter as tk
import os

from .core import *
from .core import keyboard


class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.calculate = Calculator()
        self.set = JsonParser()
        self.theme = self._themes(self.set.current_theme)
        self.setup()
        self.key_up = []

        main_frame = tk.Frame(bg=self.theme.background)
        main_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        self.prev_var = tk.StringVar()
        self.preview = tk.Entry(main_frame, textvariable=self.prev_var, cnf=self.theme.preview)
        self.preview.pack(side=tk.TOP, fill=tk.X, padx=2, pady=(2, 0), ipady=2)
#       

        self.display = tk.Entry(main_frame, cnf=self.theme.display)
        self.display.insert(0,0)
        self.display.pack(side=tk.TOP, padx=2, pady=0, ipady=2)

        buttons = tk.Frame(main_frame, bg=self.set.setup.background)
        buttons.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH, padx=2, pady=(0, 2))

        self.btns = {}
        for r in range(len(keyboard.DEFAULT)):
            buttons.rowconfigure(r+1, weight=1)
            for c in range(len(keyboard.DEFAULT[r])):
                buttons.columnconfigure(c, weight=1)

                self.btns[f'btn_{str(keyboard.DEFAULT[r][c])}'] = tk.Button(buttons, text=str(keyboard.DEFAULT[r][c]), cnf=self.theme.buttons)
                self.btns[f'btn_{str(keyboard.DEFAULT[r][c])}'].bind('<ButtonPress>', self.button_command)
                self.btns[f'btn_{str(keyboard.DEFAULT[r][c])}'].grid(row=r+1, column=c, padx=(1, 0), pady=(1, 0), sticky=tk.NSEW)

        self.btns['btn_='].config(cnf=self.theme.equal_button)
        # Undefined Button
        self.btns['btn_'].configure(cnf=self.theme.disabled_button)


    def button_command(self, e):
        
        if e.widget.cget('state') == "disabled":
            return

        button = e.widget.cget('text')
        
        last_key = button

        if last_key in ["\u00F7", 'x', '-', '+']:
            self.set_operators(last_key)
        elif last_key in [str(i) for i in range(10)]:
            self.display_numeric(last_key)
        elif last_key == ",":
            self.set_float_point()
        elif last_key in ['CE', 'C']:
            self.clean_data(last_key)
        elif last_key == "\u232B":
            self.set_backspace()
        elif last_key in ["¹/\u02E3", "\u02E3²", "²\u221A\u02E3"]:
            result = self.calculate.get_x_element(self.display.get(), last_key)
            self.display.delete(0, tk.END)
            self.display.insert(0, result['display'])
            self.prev_var.set(result['preview'])
        elif last_key == "%":
            result = self.calculate.get_porcent(self.display.get(), self.prev_var.get())
            self.display.delete(0, tk.END)
            self.display.insert(0, result['display'])
            self.prev_var.set(result['preview'])
        elif last_key == "=":
            result = self.calculate.eval(self.display.get(), self.prev_var.get())
            if result:
                self.display.delete(0, tk.END)
                self.display.insert(0, result['display'])
                self.prev_var.set("%s%s =" % (self.prev_var.get(), result['preview']))


    def display_numeric(self, value: str):
        
        if len(self.display.get()) > 13:
            return
        
        if self.display.get() == "0":
            self.display.delete(0)

        if len(self.key_up) > 0:
            if (self.key_up[-1] in ["\u00F7", 'x', '-', '+'] and
                self.display.get() != "0,"):
                self.display.delete(0, tk.END)
        
        self.key_up.append(value)
        self.display.insert(tk.END, value)

    def set_backspace(self):

        if self.display.get() == "0":
            return
        
        if len(self.display.get()) <= 1:
            self.display.delete(0, tk.END)
            self.prev_var.set("")

            self.display.insert(tk.END, 0)
        else:
            self.display.delete(len(self.display.get())-1, tk.END)
            self.prev_var.set(self.display.get())

    def set_operators(self, operator: str):
        
        if self.display.get() == "0":
            return

        self.key_up.append(operator)
        
        value = format_number(self.display.get())
        
        _format_value = str(value).replace('.', ',')

        self.display.delete(0, tk.END)
        self.display.insert(0, _format_value)
        self.prev_var.set("%s %s " % (_format_value, operator))

    def set_float_point(self):
        
        if (self.display.get().find(',') > 0 and
            self.key_up[-1] not in ["\u00F7", 'x', '-', '+']
        ):
            return
        elif float(self.display.get()) > 0:
            point = ","
        else:
            self.display.delete(0, tk.END)
            point = "0,"

        self.display.insert(tk.END, point)
        
    def clean_data(self, btn):
        
        self.key_up.clear()

        if btn == "CE":
            self.display.delete(0, tk.END)
            self.display.insert(0, 0)
        else:
            self.display.delete(0, tk.END)
            self.prev_var.set("")
            self.display.insert(0, 0)

    def _themes(self, name: str):

        themes = self.set.themes
        for theme in themes:
            if theme.name == name:
                return theme

    def setup(self):
        
        self.wm_iconbitmap(default=self.set.setup.icon)
        
        self.wm_title(self.set.setup.title)

        width = self.set.setup.width
        height = self.set.setup.height

        w_screen = self.winfo_screenwidth()
        h_screen = self.winfo_screenheight()

        posX = int((w_screen / 2) - (width / 2))
        posY = int((h_screen / 2) - (height / 2))

        self.wm_resizable(False, False)

        self.geometry(f"{width}x{height}+{posX}+{posY}")

    def start(self):
        self.mainloop()
    
    def close(self):
        self.quit()