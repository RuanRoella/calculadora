import tkinter as tk
import json

from .core import KEYBOARD

class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.set = self.load_json('setup')
        self.setup(self.set['title'], self.set['width'], self.set['height'])

        main_frame = tk.Frame(bg='#ffffff')
        main_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        self.value = tk.StringVar()
        self.value.set(0)

        self.display = tk.Entry(main_frame, textvariable=self.value, readonlybackground="#ffffff", font=('Console', 24, 'bold'), highlightthickness=0, relief=tk.FLAT, justify=tk.RIGHT, state='readonly')
        self.display.pack(side=tk.TOP, padx=5, pady=(10,0), ipady=5)
    
        buttons = tk.Frame(main_frame, bg="#ffffff")
        buttons.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH, padx=5, pady=(0, 10))
 
        self.btns = {}
        for r in range(len(KEYBOARD)):
            buttons.rowconfigure(r+1, weight=1)
            for c in range(len(KEYBOARD[r])):
                buttons.columnconfigure(c, weight=1)

                self.btns[f'btn_{str(KEYBOARD[r][c])}'] = tk.Button(buttons, text=str(KEYBOARD[r][c]), bd=0, highlightthickness=0, bg="#f8f8f2", fg="#000000", font=('Cambria', 10, 'bold'))
                self.btns[f'btn_{str(KEYBOARD[r][c])}'].grid(row=r+1, column=c, padx=(1, 0), pady=(1, 0), sticky=tk.NSEW)

        self.btns['btn_='].config(bg="#47b2f5", fg="#000000")

    @staticmethod
    def load_json(optional: str):
        with open('app/settings.json', 'r', encoding='utf-8') as file:
            json_file = json.load(file)

        return json_file[optional]
    
    def setup(self, title: str, width: int, height: int):
        self.wm_title(title)

        width = width
        height = height

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