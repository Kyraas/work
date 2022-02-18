import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from edid import *

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.text = tk.StringVar()  # изменяемый текст
        self.message = tk.StringVar()

        dict_res = get_resolutions()
        new_dict = self.convert_list(dict_res)
        cur_res = get_cur_resolution()  # получаем текущее разрешение и частоту
        self.change_text()

        self.lblMes = tk.Label(self, textvariable = self.message)  # строка состояния
        self.lblRes = tk.Label(self, textvariable = self.text)  # строка с текущим разрешением
        self.lblMes.grid(column=0, row=0)
        self.lblRes.grid(column=0, row=1)

        self.lbl = tk.Label(self, text = "Разрешения монитора: ")
        self.lbl.grid(column=0, row=2)

        self.comboRes = ttk.Combobox(self, values=new_dict, state="readonly")
        for i in range(len(dict_res)):
            if cur_res == dict_res[i]:
                self.comboRes.current(i)
        self.comboRes.grid(column=1, row=2)

        self.btn = tk.Button(self, text="Применить", command=self.cmbx_event)
        self.btn.grid(column=2, row=2)

        self.btn_default = tk.Button(self, text="Сброс", command=self.reset)
        self.btn_default.grid(column=3, row=2)

    def convert_list(self, dict_res):
        new_dict = []
        for i in dict_res:
            j = list(i)
            one_res = ""
            one_res = str(j[0]) + " на " + str(j[1]) + ", " + str(j[2]) + " Гц"
            new_dict.append(one_res)
        return new_dict

    def reset(self):    # сброс к разрешению по умолчанию
        mes = set_default()
        self.message.set(mes)
        self.change_text()

    def cmbx_event(self):   # изменение разрешения
        current_value = self.comboRes.get() # получаем выбранное значение из списка
        val = current_value.split() # разделяем строку на части
        width = val[0]
        height = val[2]
        height = height[:-1]    # убираем запятую в конце числа
        hz = val[3]
        mes = set_resolution(int(width), int(height), int(hz))
        self.message.set(mes)
        self.change_text()
        self.timer_var = tk.StringVar()
        messagebox.showinfo("Подтверждение", self.timer_var)
        self.count_down()

    def count_down(self, time_count=5):
        self.timer_var.set(f"Прежние параметры дисплея будут применены через: {time_count} с.")
        if time_count == 0:
            # self.destroy()
            return
        time_count -= 1
        self.after(1000, self.count_down, time_count)
        
    def change_text(self):
        cur_res = get_cur_resolution()  # получаем текущее разрешение и частоту
        self.text.set(f"Текущее разрешение: {cur_res[0]} на {cur_res[1]}, {int(cur_res[2])} Гц")



app = App()   # Создаем новое окно
app.geometry('600x300')
app.title("Разрешение экрана")
app.mainloop()   # Запускаем бесконечный цикл окна. Без этой строки окно не отобразится
