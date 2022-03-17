import tkinter as tk
from tkinter import END, N, ttk

text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus sagittis diam eget turpis laoreet, vitae faucibus dolor ullamcorper. Proin vel congue velit. Phasellus neque diam, ultricies in varius sit amet, ullamcorper ut velit."

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.console = tk.Text()
        self.console.grid(column=0, row=0)

        self.start_btn = tk.Button(self, text="Начать", command=self.start)
        self.start_btn.grid(column=1, row=0, sticky=N)

    def start(self):
        for i in range(10):
            new_text = str(i) + " " + text + "\n"
            self.after(1000, self.console.insert(END, new_text))
            # self.console.insert(1.0, text)
            self.console.yview(END)
            self.update_idletasks()

app = App()   # Создаем новое окно
app.title("Заполнение табелей")
app.mainloop()   # Запускаем бесконечный цикл окна. Без этой строки окно не отобразится
