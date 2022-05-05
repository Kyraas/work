import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Вводим переменные
        id = "70174464"
        student = "Серебряков Юрий Владимирович"
        y0 = 150
        x0 = 10
    
        header = tk.BooleanVar(False)

        # Создаем фреймы
        TopFrame = tk.Frame(self)
        GraphFrame = tk.Frame(TopFrame)
        ButtonFrame = tk.LabelFrame(TopFrame)
        CoordsFrame = tk.Frame(self)
        TopFrame.pack(side="top")
        GraphFrame.pack(side="left")
        ButtonFrame.pack(side="right")
        CoordsFrame.pack(side="left")



        # Класс для создания полей ввода
        class TitEntry:
            def __init__(self, coord):
                tk.Label(CoordsFrame, text=coord).pack()
                tk.Entry(CoordsFrame, width=10, bd=3).pack()
        
        # Базовый заголовок
        self.title(student)

        # Функция для смены заголовка
        def headerChange(event):
            header.set(not header.get())
            if (header.get() == False): self.title(student)
            else: self.title(id)

        self.bind('<Button-1>', headerChange)

        # Создаем окно
        canv = tk.Canvas(GraphFrame, width=250, height=250)

        # Рисуем систему координат
        canv.create_line(15,160,15,10, width=2, arrow=tk.LAST, fill="red")
        canv.create_line(10,150,150,150, width=2, arrow=tk.LAST, fill="red")
        canv.create_text(20,170, text="(0; 0)", fill="red", font=("Helvectica", "10"))
        canv.create_text(25, 10, text="y", fill="red", font=("Helvectica", "10"))
        canv.create_text(150, 160, text="x", fill="red", font=("Helvectica", "10"))

        # Берем координаты
        # x1 = int(id[2:4])
        # x2 = int(id[4:6])
        # x3 = int(id[6:8])
        # yID = str(int(id)/3)
        # y1 = int(yID[2:4])
        # y2 = int(yID[4:6])
        # y3 = int(yID[6:8])
        x1 = int(id[2:4])
        x2 = int(id[4:6])
        x3 = int(id[6:8])
        yID = str(int(id)/3)
        y1 = int(yID[2:4])
        y2 = int(yID[4:6])
        y3 = int(yID[6:8])

        var = tk.StringVar()
        var.set("size-") 

        #Рисуем базовый треугольник
        rectangle = canv.create_polygon([x0+x1,y0-y1], [x0+x2,y0-y2], [x0+x3,y0-y3], fill="blue") 
        canv.pack()

        # Класс для создания кнопок
        class RBColor:
            def __init__(self, color):
                tk.Radiobutton(ButtonFrame, text=color, variable=var, value=color, command=paint).pack(anchor='w')

        # Рисуем треугольник в зависимости от выбранного цвета
        def paint():
            if var.get() == "size+":
                canv.coords(rectangle, x0+x1*1.5, y0-y1*1.5, x0+x2*1.5, y0-y2*1.5, x0+x3*1.5, y0-y3*1.5)
            else:
                canv.coords(rectangle, x0+x1, y0-y1, x0+x2, y0-y2, x0+x3, y0-y3)
        # Создаем кнопки
        RBColor('size+')
        RBColor('size-')


        # Создаем поля ввода
        TitEntry("x1:")
        TitEntry("y1:")
        TitEntry("x2:")
        TitEntry("y2:")
        TitEntry("x3:")
        TitEntry("y3:")


aboba = App()
aboba.mainloop()