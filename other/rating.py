import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Вводим переменные
        ID = "70174464"
        FIO = "Серебряков Юрий Владимирович"
        y0 = 150
        x0 = 10
        header = tk.BooleanVar(False)

        # Создаем фреймы
        colFrame = tk.Frame(self, borderwidth=5, relief=tk.GROOVE).pack(side=tk.TOP)

        triFrame = tk.LabelFrame(self).pack(side=tk.TOP)

        x1y1Frame = tk.Frame(self, borderwidth=5, relief=tk.GROOVE).pack(side=tk.LEFT)
        x2y2Frame = tk.LabelFrame(self).pack(side=tk.LEFT)
        x3y3Frame = tk.LabelFrame(self).pack(side=tk.LEFT)

        # Класс для создания кнопок
        class RBColor:
            def __init__(self, color, val):
                tk.Radiobutton(
                    colFrame, text=color, command=lambda i=color: paint(i), variable=var, value=val).pack()


        # Класс для создания полей ввода
        class TitEntry:
            def __init__(self, coord, frame):
                tk.Label(frame, text=coord).pack()
                tk.Entry(frame, width=20, bd=3).pack()

        
        # Базовый заголовок
        self.title(FIO)

        # Функция для смены заголовка
        def headerChange(event):
            header.set(not header.get())
            if (header.get() == False): self.title(FIO)
            else: self.title(ID)

        self.bind('<Button-1>', headerChange)

        # Создаем окно
        canv = tk.Canvas(triFrame, width=250, height=250)

        # Рисуем систему координат
        canv.create_line(15,160,15,10, width=2, arrow=tk.LAST, fill="red")
        canv.create_line(10,150,150,150, width=2, arrow=tk.LAST, fill="red")
        canv.create_text(20,170, text="(0; 0)", fill="red", font=("Helvectica", "10"))
        canv.create_text(25, 10, text="y", fill="red", font=("Helvectica", "10"))
        canv.create_text(150, 160, text="x", fill="red", font=("Helvectica", "10"))

        # Берем координаты
        x1 = int(ID[2:4])
        x2 = int(ID[4:6])
        x3 = int(ID[6:8])
        yID = str(int(ID)/3)
        y1 = int(yID[2:4])
        y2 = int(yID[4:6])
        y3 = int(yID[6:8])

        # Рисуем треугольник в зависимости от выбранного цвета
        def paint(color):
            canv.create_polygon([x0+x1,y0-y1], [x0+x2,y0-y2], [x0+x3,y0-y3], fill=color)

        #Рисуем базовый треугольник
        canv.create_polygon([x0+x1,y0-y1], [x0+x2,y0-y2], [x0+x3,y0-y3], fill="blue")

        canv.pack()
 
 
        #Создаем кнопки
        var = tk.IntVar()
        var.set(0)
        RBColor('blue', 0)
        RBColor('red', 1)
        RBColor('green', 2)
        RBColor('yellow', 3)
        RBColor('orange', 4)
        RBColor('pink', 5)



        TitEntry("x1:", x1y1Frame)
        TitEntry("y1:", x1y1Frame)
        TitEntry("x2:", x2y2Frame)
        TitEntry("y2:", x2y2Frame)
        TitEntry("x3:", x3y3Frame)
        TitEntry("y3:", x3y3Frame)


aboba = App()
aboba.mainloop()
