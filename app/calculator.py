import tkinter as tk
import re
from .core import KEYBOARD
from .core import Settings
from .core import Calculator

class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.calculate = Calculator()
        self.set = Settings()
        self.setup()
        self.key_up = []

        main_frame = tk.Frame(bg=self.set.main.background)
        main_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        self.prev_var = tk.StringVar()
        self.preview = tk.Entry(main_frame, textvariable=self.prev_var, cnf=self.set.preview)
        self.preview.pack(side=tk.TOP, fill=tk.X, padx=2, pady=(2, 0), ipady=2)

        self.display = tk.Entry(main_frame, cnf=self.set.display)
        self.display.insert(0,0)
        self.display.pack(side=tk.TOP, padx=2, pady=0, ipady=2)

        buttons = tk.Frame(main_frame, bg=self.set.main.background)
        buttons.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH, padx=2, pady=(0, 2))

        self.btns = {}
        for r in range(len(KEYBOARD)):
            buttons.rowconfigure(r+1, weight=1)
            for c in range(len(KEYBOARD[r])):
                buttons.columnconfigure(c, weight=1)

                self.btns[f'btn_{str(KEYBOARD[r][c])}'] = tk.Button(buttons, text=str(KEYBOARD[r][c]), cnf=self.set.button)
                self.btns[f'btn_{str(KEYBOARD[r][c])}'].bind('<ButtonPress>', self.button_command)
                self.btns[f'btn_{str(KEYBOARD[r][c])}'].grid(row=r+1, column=c, padx=(1, 0), pady=(1, 0), sticky=tk.NSEW)

        self.btns['btn_='].config(cnf=self.set.button_equal)
        # Undefined Button
        self.btns['btn_←'].configure(state='disabled', background="#dddddd")


    def button_command(self, e):

        button = e.widget.cget('text')

        self.key_up.append(button)

        last_key = self.key_up[-1]
        
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
            self.display.delete(0, tk.END)
            self.display.insert(0, result)
            self.prev_var.set("%s%s =" % (self.prev_var.get(), self.display.get()))


    def display_numeric(self, value: int):

        if len(self.display.get()) > 14:
            return

        if self.display.get() == "0":
            self.display.delete(0)
       
        if len(self.key_up) > 1:
            
            if self.key_up[-2] in ["\u00F7", 'x', '-', '+']:
                self.display.delete(0, tk.END)
        
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

        value = self.display.get()

        _split_value = value.split(',')
        if _split_value[-1] in ['', "0"]:
            self.display.delete(0, tk.END)
            self.display.insert(0, _split_value[0])
            value = _split_value[0]

        self.prev_var.set("%s %s " % (value, operator))
    
    def set_float_point(self):
        
        if self.display.get().find(',') > 0:
            return

        # Last value of the display
        value = self.display.get()[-1]

        point = ","

        if value == ",":
            return
        elif value in ["\u00F7", 'x', '-', '+']:
            self.display.delete(0, tk.END)
            point = "0,"
        elif len(self.key_up) > 1:
            if self.key_up[-2] in ["\u00F7", 'x', '-', '+']:
                self.display.delete(0, tk.END)
                point = "0,"

        self.display.insert(tk.END, point)
        
    def clean_data(self, btn):
        
        if btn == "CE":
            self.display.delete(0, tk.END)
            self.display.insert(0, 0)
        else:
            self.display.delete(0, tk.END)
            self.prev_var.set("")
            self.display.insert(0, 0)

    def setup(self):
        
        self.wm_iconbitmap(default=r'assets\calculator.ico')
        
        self.wm_title('Calculadora')

        width = 300
        height = 400

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