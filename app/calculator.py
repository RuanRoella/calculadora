import tkinter as tk

from .core import KEYBOARD
from .core import Settings
from .core import Calculator

class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.calculate = Calculator()
        self.set = Settings()
        self.setup(self.set.main.title, self.set.main.width, self.set.main.height)

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


    def button_command(self, e):

        button = e.widget.cget('text')

        if button in [str(i) for i in range(10)]:
            self.display_numeric(int(button))
        elif button == "\u232B":
            self.set_backspace()
        elif button in ["\u00F7", 'x', '-', '+']:
            self.set_operators(button)
        elif button in ["CE", "C"]:
            self.clean_data(button)
        elif button in ["¹/\u02E3", "\u02E3²", "²\u221A\u02E3"]:
            result = self.calculate.get_x_element(self.display.get(), button)
            self.display.delete(0, tk.END)
            self.display.insert(0, result['display'])
            self.prev_var.set(result['preview'])
        elif button == "%":
            result = self.calculate.get_porcent(self.prev_var.get())
            self.display.delete(0, tk.END)
            self.display.insert(0, result['display'])
            self.prev_var.set(result['preview'])
        elif button == ",":
            ...
        elif button == "←":
            ...
        else:
            result = self.calculate.eval(self.prev_var.get())
            self.display.delete(0, tk.END)
            self.display.insert(0, result)
            self.prev_var.set("%s%s" % (self.prev_var.get(), '='))
        
            
    def display_numeric(self, value: int):
        if len(self.display.get()) >= 13:
            return

        if self.display.get() == "0":
            self.display.delete(0)
            self.display.insert(0, str(value))
        else:
            self.display.insert(tk.END, str(value))

        express = "%s%s" % (self.prev_var.get(), self.display.get()[-1])
        if value == 0 and len(self.display.get()) <= 1:
            self.display.insert(tk.END, ',')
            express = "%s%s" % (self.prev_var.get(), self.display.get())
        
        self.prev_var.set(express)

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
        
        if self.display.get() == "0" or self.prev_var.get()[-1] == operator:
            return
        
        if self.prev_var.get()[-1] == "=":
            self.prev_var.set("%s%s" % (self.display.get(), operator))

        self.display.delete(0, tk.END)
        self.display.insert(tk.END, 0)

        if self.prev_var.get()[-1] in ["\u00F7", 'x', '-', '+']:
            new_express = self.prev_var.get()[:-1]
            self.prev_var.set(new_express)
        
        express = "%s%s" % (self.prev_var.get(), operator)
        self.prev_var.set(express)
    
    def clean_data(self, btn):

        if btn == "CE":
            index = self.prev_var.get().find(self.display.get())
            if index != -1:
                self.prev_var.set(self.prev_var.get()[:index])
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, 0)
        else:
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, 0)
            self.prev_var.set("")

    def setup(self, title: str, width: int, height: int):
        self.wm_title(title)

        width = int(width)
        height = int(height)

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