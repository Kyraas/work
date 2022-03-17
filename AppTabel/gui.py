# https://stackoverflow.com/questions/53721337/how-to-get-python-console-logs-on-my-tkinter-window-instead-of-a-cmd-window-whil

import tkinter as tk
from tkinter import N, END, ttk
from Laboriousness import main
import sys

class PrintLogger(): # create file like object
    ui = None
    # console = None
    def __init__(self, textbox): # pass reference to text widget
        self.textbox = textbox # keep ref

    def write(self, text):
        self.textbox.insert(tk.END, text) # write text to textbox
        self.ui.update_idletasks()
        self.ui.console.yview(END)
            # could also scroll to end of textbox here to make sure always visible

    def flush(self): # needed for file like object
        pass

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.console = tk.Text()
        self.console.grid(column=0, row=0)

        # create instance of file like object
        pl = PrintLogger(self.console)
        pl.ui = self
        # pl.console = self.console
        # replace sys.stdout with our object
        sys.stdout = pl

        self.start_btn = tk.Button(self, text="Начать", command=self.start)
        self.start_btn.grid(column=1, row=0, sticky=N)

    def start(self):
        main()

app = App()   # Создаем новое окно
# app.geometry('500x300')
app.title("Заполнение табелей")
app.mainloop()   # Запускаем бесконечный цикл окна. Без этой строки окно не отобразится
