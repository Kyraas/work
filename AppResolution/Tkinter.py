import tkinter as tk
from tkinter import ttk
from edid import *

def myFunc(e):
    x = int(e[0])
    return x

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        get_res = get_resolutions() # получаем кортежи поддерживаемых разрешений из EDID монитора
        get_res.sort(reverse=True)  # сортируем кортежи
        dict_res = []
        for i in list(get_res): # преобразуем кортежи в список
            s = ""
            s += str(i[0]) + ' на ' +  str(i[1]) + ', ' + str(i[2]) + ' Гц'
            dict_res.append(s)

        self.text = tk.StringVar()  # изменяемый текст
        cur_res = get_cur_resolution()  # получаем текущее разрешение и частоту
        self.text.set(f"Текущее разрешение: {cur_res[0]} на {cur_res[1]}, {float(cur_res[2])} Гц")

        self.lblRes = tk.Label(self, textvariable = self.text)  # строка с текущим разрешением
        self.lblRes.grid(column=0, row=0)

        self.lbl = tk.Label(self, text = "Разрешения монитора: ")
        self.lbl.grid(column=0, row=1)

        self.comboRes = ttk.Combobox(self, values=dict_res, state="readonly")
        # res = get_resolutions()
        # for i in res:
        #     if res_freq in res:
        #         print(res_freq)
        self.comboRes.current(0)
        self.comboRes.grid(column=1, row=1)

        self.btn = tk.Button(self, text="Применить", command=self.cmbx_event)
        self.btn.grid(column=2, row=1)

        self.btn_default = tk.Button(self, text="Сброс", command=self.reset)
        self.btn_default.grid(column=3, row=1)

    def reset(self):    # сброс к разрешению по умолчанию
        mes = set_default()
        cur_res = get_cur_resolution()
        self.text.set(f"{mes}\nТекущее разрешение: {cur_res[0]} на {cur_res[1]}, {float(cur_res[2])} Гц")

    def cmbx_event(self):   # изменение разрешения
        current_value = self.comboRes.get() # получаем выбранное значение из списка
        val = current_value.split() # разделяем строку на части
        width = val[0]
        height = val[2]
        height = height[:-1]    # убираем запятую в конце числа
        hz = val[3]
        mes = set_resolution(int(width), int(height), float(hz))
        cur_res = get_cur_resolution()
        self.text.set(f"{mes}\nТекущее разрешение: {cur_res[0]} на {cur_res[1]}, {float(cur_res[2])} Гц")

app = App()   # Создаем новое окно
app.geometry('600x300')
app.title("Разрешение экрана")
app.mainloop()   # Запускаем бесконечный цикл окна. Без этой строки окно не отобразится