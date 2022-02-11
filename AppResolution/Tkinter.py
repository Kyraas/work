# import tkinter as tk
import tkinter as tk
from tkinter import ttk
from edid import *

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.text = tk.StringVar()
        cur_res = get_cur_resolution()
        self.text.set(f"Текущее разрешение: {cur_res}")

        self.lblRes = tk.Label(self, textvariable = self.text)
        self.lblRes.grid(column=0, row=0)

        self.lbl = tk.Label(self, text = "Разрешения монитора: ")
        self.lbl.grid(column=0, row=1)

        self.comboRes = ttk.Combobox(self, values = get_resolutions(), state="readonly")
        self.comboRes.current(0)
        self.comboRes.grid(column=1, row=1)

        self.btn = tk.Button(self, text="Применить", command=self.cmbx_event)
        self.btn.grid(column=2, row=1)

        self.btn_default = tk.Button(self, text="Сброс", command=self.reset)
        self.btn_default.grid(column=3, row=1)

    def reset(self):
        set_default()
        cur_res = get_cur_resolution()
        self.text.set(f"Текущее разрешение: {cur_res}")

    def cmbx_event(self):
        current_value = self.comboRes.get()
        val = current_value.split()
        width = val[0]
        height = val[1]
        print(width, height)
        # hz = val[2]
        set_resolution(int(width), int(height))
        cur_res = get_cur_resolution()
        self.text.set(f"Текущее разрешение: {cur_res}")

app = App()   # Создаем новое окно
app.geometry('600x300')
app.title("Разрешение экрана")
app.mainloop()   # Запускаем бесконечный цикл окна. Без этой строки окно не отобразится