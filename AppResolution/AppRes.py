import tkinter as tk
from tkinter import ttk
from GetSetRes import *

class CountDownMessageBox(tk.Toplevel): # Toplevel - верхний слой
    def __init__(self, app):
        self.app = app
        super().__init__()

        self.geometry('350x100')
        self.title("Подтверждение")

        self.lbl = tk.Label(self, text="Сохранить текущие параметры отображения?")
        self.lbl.grid(row=0, column=0, columnspan=2)

        self.timer_var = tk.StringVar()
        self.timer = tk.Label(self, textvariable = self.timer_var)
        self.timer.grid(row=1, column=0, columnspan=2)

        self.yes_btn = tk.Button(self, text="Сохранить", command=self.destroy)
        self.yes_btn.grid(row=2, column=0)
        self.no_btn = tk.Button(self, text="Отменить изменения", command=self.cancel)    # , command=self.command_reset(cmd)
        self.no_btn.grid(row=2, column=1)

        self.count_down()

    def cancel(self):
        self.destroy()
        self.app.reset()

    def count_down(self, time_count=10):
        self.timer_var.set(f"Прежние параметры дисплея будут применены через: {time_count} с.")
        if time_count == 0:
            self.destroy()
            self.app.reset()
        time_count -= 1
        self.after(1000, self.count_down, time_count)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.text = tk.StringVar()  # текущее разрешение экрана
        self.message = tk.StringVar()   # сообщение

        self.dict_device = get_device() # словарь вида "DeviceName: device"
        list_device = []    # лист DeviceName
        for i in self.dict_device:
            list_device.append(i)

        self.lblMon = tk.Label(self, text = "Монитор: ")
        self.lblMon.grid(column=0, row=0)

        self.comboMon = ttk.Combobox(self, values=list_device, state="readonly")    # список DeviceName
        self.comboMon.bind("<<ComboboxSelected>>", self.choice_dev)
        self.comboMon.current(0)    # по умолчанию берет первый (основной)
        self.choice_dev("<<ComboboxSelected>>")
        self.comboMon.grid(column=1, row=0)

        self.lblMes = tk.Label(self, textvariable = self.message)  # строка состояния
        self.lblRes = tk.Label(self, textvariable = self.text)  # строка с текущим разрешением
        self.lblMes.grid(column=0, row=3, columnspan=2)
        self.lblRes.grid(column=0, row=1, columnspan=2)

        self.lbl = tk.Label(self, text = "Разрешения монитора: ")
        self.lbl.grid(column=0, row=2)

        self.btn = tk.Button(self, text="Применить", command=self.cmbx_event)
        self.btn.grid(column=2, row=2)

        self.btn_default = tk.Button(self, text="Сброс", command=self.reset)
        self.btn_default.grid(column=3, row=2)

    def choice_dev(self, event):
        cur_mon = self.comboMon.get()
        cur_res = get_cur_resolution(self.dict_device[cur_mon])
        dict_res = get_resolutions(self.dict_device[cur_mon])
        new_dict = self.convert_list(dict_res)
        self.comboRes = ttk.Combobox(self, values=new_dict, state="readonly", width=32)
        for i in range(len(dict_res)):
            if cur_res == dict_res[i]:
                self.comboRes.current(i)
        self.comboRes.grid(column=1, row=2)

    def convert_list(self, dict_res):
        new_dict = []
        for i in dict_res:
            j = list(i)
            one_res = ""
            one_res = str(j[0]) + " на " + str(j[1]) + ", " + str(j[2]) + " Гц"
            if j[3] != 0:
                one_res = one_res + " (чересстрочная)"
            new_dict.append(one_res)
        return new_dict

    def reset(self):    # сброс к разрешению по умолчанию
        cur_mon = self.comboMon.get()
        mes = set_default()
        self.message.set(mes)
        self.change_text(self.dict_device[cur_mon])

    def cmbx_event(self):   # изменение разрешения
        cur_mon = self.comboMon.get()    # получаем выбранный DeviceName из списка
        current_value = self.comboRes.get() # получаем выбранное значение из списка
        cur_res = get_cur_resolution(self.dict_device[cur_mon])  # получаем текущее разрешение и частоту
        val = current_value.split() # разделяем строку на части
        width = val[0]
        height = val[2]
        height = height[:-1]    # убираем запятую в конце числа
        hz = val[3]
        if len(val) > 5:
            flag = 2
        else:
            flag = 0

        check = (int(width), int(height), int(hz), int(flag))
        if check == cur_res:
            self.message.set("Данное разрешение уже установлено.")
        else:
            mes = set_resolution(self.dict_device[cur_mon], int(width), int(height), int(hz), int(flag))
            self.message.set(mes)
            if mes == "Разрешение применено.":
                self.change_text(self.dict_device[cur_mon])
                CountDownMessageBox(self)
    
    def change_text(self, device):
        cur_res = get_cur_resolution(device)  # получаем текущее разрешение и частоту
        self.text.set(f"Текущее разрешение: {cur_res[0]} на {cur_res[1]}, {int(cur_res[2])} Гц")


app = App()   # Создаем новое окно
app.geometry('600x300')
app.title("Разрешение экрана")
app.mainloop()   # Запускаем бесконечный цикл окна. Без этой строки окно не отобразится