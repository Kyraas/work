# -*- coding: utf-8 -*-
# https://konspekteka.ru/test-po-teme-po/
# https://stackoverflow.com/questions/45171328/grab-set-in-tkinter-window
# pyinstaller --noconfirm --onefile --windowed --name "Тестирование"  "C:/Users/ddas/Documents/GitRep/work/Test/main.py"

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from time import ctime
from os import path
from datetime import datetime as dt
import sys
from tkinter import messagebox

from testdatabase import open_database
from createreport import create_new

month = {
    "Jan": "01",
    "Feb": "02",
    "Mar": "03",
    "Apr": "04",
    "May": "05",
    "Jun": "06",
    "Jul": "07",
    "Aug": "08",
    "Sep": "09",
    "Oct": "10",
    "Nov": "11",
    "Dec": "12",
    }

# Таблица
class Table(tk.Frame):
    def __init__(self, parent=None, headings=tuple(), rows=tuple()):
        super().__init__(parent)

        table = ttk.Treeview(self, show="headings", selectmode="browse")
        table["columns"]=headings
        table["displaycolumns"]=headings

        for head in headings:
            table.heading(head, text=head, anchor="center")
            table.column(head, width=120, anchor="center")

        for row in rows:
            table.insert('', tk.END, values=tuple(row))

        scrolltable = tk.Scrollbar(self, command=table.yview)
        table.configure(yscrollcommand=scrolltable.set)
        scrolltable.pack(side="right", fill="y")
        table.pack(expand="yes", fill="both")


# Вход (главное окно)
class Main(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Тестирование")
        resize_window(self, 250, 200)
        self.minsize(height=200, width=100)
        # # app.iconbitmap('icon.ico')

        tk.Label(self, text="Войти как:").pack(pady=(20,0), expand='yes', fill='both')
        
        tk.Button(self, width=15, height=2, text="Студент",
                    command=self.user).pack(padx=50, pady=20, expand='yes', fill='both')
        tk.Button(self, width=15, height=2, text="Преподаватель",
                    command=self.login).pack(padx=50, pady=(0,40), expand='yes', fill='both')
        self.bind('<Return>', self.user)

    def user(self, event=None):
        window = User(self)
        window.grab_set()
        window.focus_force()

    def login(self):
        window = Login(self)
        window.grab_set()
        window.focus_force()


# Вход для студента (промежуточное окно)
class User(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        last_update = tk.StringVar()
        questions_num = tk.StringVar()
        tries_num = tk.StringVar()
        time_limit = tk.StringVar()
        self.student_name = tk.StringVar()
        self.error_name = tk.StringVar()

        self.title("Начать тест")
        resize_window(self, 400, 300)
        self.minsize(height=250, width=250)

        bot_frame = tk.Frame(self)
        start_btn = tk.Button(bot_frame, width=15,
                                text="Начать",
                                command=self.start_test)
        args = open_database()
        name, max_time, tries = open_database(test_info=True)

        tk.Label(self, textvariable=last_update
                    ).pack(pady=(10,0),
                            expand='yes', anchor='center', fill='both')

        if isinstance(args, str):
            last_update.set(args)
            start_btn["state"] = "disable"
        else:
            questions = args[0]
            max = str(len(questions))
            last_update.set(f"Последнее обновление теста: {get_update_date()}")
            questions_num.set(f"Количество вопросов: {max}")
            tries_num.set(f"Количество попыток: {str(tries)}")
            time_limit.set(f"Ограничение по времени: {str(max_time)} мин" )

            info_box = tk.Frame(self)
            info_box.pack(expand='yes', anchor='w', fill='both', padx=30)
            tk.Label(info_box, textvariable=questions_num
                        ).pack(expand='yes', anchor='w', fill='y')
            if tries > 0:
                tk.Label(info_box, textvariable=tries_num
                            ).pack(expand='yes', anchor='w',
                                    fill='y')
                self.bind('<Return>', self.start_test)
            else:
                tk.Label(info_box, fg="red", textvariable=tries_num
                            ).pack(expand='yes', anchor='w',
                                    fill='y')
                start_btn["state"] = "disable"
            tk.Label(info_box, textvariable=time_limit
                        ).pack(expand='yes', anchor='w',
                                fill='y')
            
            if name != "":
                self.student_name.set(name)
                label_name = tk.StringVar()
                label_name.set(f"ФИО студента: {name}")
                tk.Label(info_box, textvariable=label_name
                            ).pack(expand='yes', anchor='w',
                                    fill='y')
            else:
                tk.Label(self, text="Укажите фамилию, имя, отчество:"
                            ).pack(expand='yes', padx=(10,0), pady=(20,0), fill='both')
                tk.Entry(self, width=50, textvariable=self.student_name
                            ).pack(expand='yes', padx=20, fill='both')
                tk.Label(self, textvariable=self.error_name
                            ).pack(expand='yes', fill='both')

        bot_frame.pack(padx=40, pady=(10,30), fill='both')
        start_btn.pack(side='left', expand='yes', fill='both')
        tk.Button(bot_frame, width=15, text="Отмена",
                    command=self.back
                    ).pack(padx=(20, 0), side='left',
                            expand='yes', fill='both')

    def back(self):
        self.parent.deiconify()
        self.destroy()

    def start_test(self, event=None):
        name = self.student_name.get()
        if name == "":
            self.error_name.set("Заполните поле!")
        else:
            name = self.student_name.get()
            open_database(name=name)
            _, _, tries = open_database(test_info=True)
            tries -= 1
            open_database(tries=tries)
            self.error_name.set("")
            self.destroy()
            self.parent.withdraw()
            self = Testing(self.parent)


# Вход для преподавателя (промежуточное окно)
class Login(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.login = tk.StringVar()
        self.password = tk.StringVar()
        self.login_err = tk.StringVar()
        self.password_err = tk.StringVar()

        # Делает родительское окно неактивным, пока активно дочернее
        self.title("Вход")
        resize_window(self, 300, 170)
        self.minsize(height=150, width=300)

        top_frame = tk.Frame(self)
        mid_frame = tk.Frame(self)
        bot_frame = tk.Frame(self)

        top_frame.pack(pady=(20,0), padx=30, expand='yes', fill="both")
        mid_frame.pack(expand='yes', padx=30, fill="both")
        bot_frame.pack(pady=20, padx=30, expand='yes', fill="both")

        tk.Label(top_frame, textvariable=self.login_err
                    ).pack(side="bottom", expand='yes', fill="both")
        tk.Label(mid_frame, textvariable=self.password_err
                    ).pack(side="bottom", expand='yes', fill="both")

        tk.Label(top_frame, text="Логин:"
                    ).pack(side='left', expand='yes', padx=(0,5),
                            fill="both", anchor='e')
        tk.Entry(top_frame, textvariable=self.login
                    ).pack(side='left', expand='yes',
                            anchor='e', fill="both")

        tk.Label(mid_frame, text="Пароль:"
                    ).pack(side='left', expand='yes',
                            fill="both", anchor='e')
        tk.Entry(mid_frame, textvariable=self.password, show="*"
                    ).pack(side='left', expand='yes',
                            anchor='e', fill="both")

        tk.Button(bot_frame, width=15,
                    text="Войти", command=self.start_db
                    ).pack(side='left', expand='yes',
                            padx=(0,15), fill="both")
        tk.Button(bot_frame, width=15,
                    text="Отмена", command=self.destroy
                    ).pack(side='left', expand='yes', fill="both")
        self.bind('<Return>', self.start_db)    # Вход по клавише Enter

    def start_db(self, event=None):
        log = self.login.get()
        passwrd = self.password.get()

        if log == "":
            self.login_err.set("Введите логин")
        else:
            mes = open_database(login=log)
            self.login_err.set(mes)

        if passwrd == "":
            self.password_err.set("Введите пароль")
        else:
            mes = open_database(password=passwrd)
            self.password_err.set(mes)
        
        log_err = self.login_err.get()
        paswrd_err = self.password_err.get()
        if log_err == "" and paswrd_err == "":
            self.parent.withdraw()  # скрываем родительское окно
            self.destroy()
            win = Admin(self.parent)          


# Студент (Тест)
class Testing(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Тестирование")
        resize_window(self, 700, 500)
        self.minsize(height=400, width=400)
        self.focus_force()
        self.protocol("WM_DELETE_WINDOW", self.close_window)

        self.questions, answers =  open_database()
        _, max_time, _ = open_database(test_info=True)
        self.answers_options, self.correct_answers, self.max_score = answers
        self.max_ques = len(self.questions)
        self.num = 0
        self.process = True
        self.student_answers = [[] for _ in range(self.max_ques)]
        self.checked = []
        self.start_test = dt.now()

        self.question = tk.StringVar()
        self.question_limited = tk.StringVar()
        self.time_limited = tk.StringVar()
        self.time_passed = tk.StringVar()
        self.answer_type = tk.StringVar()
        self.selected = tk.IntVar()
        self.warning = tk.StringVar()

        # Строка с количеством (не)пройденных вопросов
        tk.Label(self, font="12",
                textvariable=self.question_limited
                ).pack(anchor='nw', padx=20, expand='true', fill='y')
        
        # Верхний фрейм с таймером
        top_frame = tk.Frame(self)
        top_frame.pack(anchor='nw', expand='true', fill='both')
        tk.Label(top_frame, font="12", textvariable=self.time_limited
                    ).pack(side="left", anchor='nw', padx=20,
                            expand='true', fill='y')
        self.timer_passed = tk.Label(top_frame, font="12",
                                        textvariable=self.time_passed)
        self.timer_passed.pack(side="left", anchor='w',
                                padx=20, expand='true', fill='y')

        # Текст и тип вопроса
        tk.Label(self, wraplength=600, justify="left",
                    font="bold 14", textvariable=self.question
                    ).pack(anchor='w', padx=20,
                            expand='true', fill='y')
        tk.Label(self, textvariable=self.answer_type
                    ).pack(anchor='w', padx=20,
                            pady=(0,10), expand='true', fill='y')
    
        self.answer_frame = tk.Frame(self)
        self.answer_frame.pack(anchor='w', padx=30, expand='true', fill='both')

        # Нижний фрейм с кнопками
        bot_frame = tk.Frame(self)
        bot_frame.pack(padx=(30,200), pady=10, anchor='w', expand='true', fill='both')
        self.btn_back = tk.Button(bot_frame, width=10, text="Назад", command=self.back)
        tk.Button(bot_frame, width=10, text="Далее",
                    command=self.get_answer
                    ).pack(side='right', expand='true', fill='both')
        self.bind('<Return>', self.get_answer)
        tk.Label(self, textvariable=self.warning
                    ).pack(pady=10, expand='true', fill='both')

        self.switch_page()
        self.count_down(max_time)

    # Предыдущая страница
    def back(self):
        if self.num > 0:
            self.num -= 1
            self.switch_page()

    # Получение отмеченных ответов (Enter)
    def get_answer(self, event=None):
        answer = self.selected.get()
        # Один вариант ответа
        if answer != 0:
            self.student_answers[self.num] = answer
            self.num += 1
            self.switch_page()
    
        # Несколько вариантов ответа
        elif self.checked:
            self.student_answers[self.num] = []
            n = len(self.answers_options[self.num])
            empty_answer = True
            for i in range(n):
                checkbtn_answer = self.checked[i].get()
                if checkbtn_answer != 0:
                    empty_answer = False
                    self.student_answers[self.num].append(checkbtn_answer)
            if empty_answer:
                self.warning.set("Вариант ответа не был выбран!")
            else:
                self.num += 1
                self.switch_page()
        else:
            self.warning.set("Вариант ответа не был выбран!")
    
    # Следующая страницв
    def switch_page(self):
        n = self.num
        self.selected.set(0)
        self.checked = []

        # Показ\сокрытие кнопки "Назад"
        if n != 0:
            self.btn_back.pack(side='left', padx=(0, 20), expand='true', fill='both')
        else:
            self.btn_back.pack_forget()

        # Убираем предупреждение, если оно было
        if self.warning.get() != "":
            self.warning.set("")
        
        # Строка с количеством вопросов
        if n < self.max_ques:
            answer = self.student_answers[n]
            self.question_limited.set(f"Вопросов всего: {self.max_ques}. Осталось: {self.max_ques - n - 1}")
            self.question.set(self.questions[n])
            self.add_answer(self.answers_options[n], len(self.answers_options[n]), answer)
            self.update_idletasks()
        else:
            self.end_test()

    # Создание кнопок с вариантами ответов
    def add_answer(self, lst, amount=2, answer=None):
        n = self.num
        old_widgets = self.answer_frame.pack_slaves()
        for widget in old_widgets:
            widget.destroy()
        
        if len(self.correct_answers[n]) == 1:
            if self.answer_type.get != "Выберите один ответ.":
                self.answer_type.set("Выберите один ответ.")
            for i in range(amount):

                # Запоминает выбранные ранее варианты ответа
                if isinstance(answer, int):
                    self.selected.set(answer)

                tk.Radiobutton(self.answer_frame, wraplength=500,
                                justify="left", font="12", text=lst[i],
                                variable=self.selected, value=i+1
                                ).pack(anchor='w', expand='true', fill='y')
        else:
            if self.answer_type.get != "Выберите несколько вариантов ответа.":
                self.answer_type.set("Выберите несколько вариантов ответа.")
            for i in range(amount):
                value = tk.IntVar()

                # Запоминает выбранные ранее варианты ответа
                if answer and isinstance(answer, list):
                    for ans in answer:
                        if i+1 == ans:                           
                            value.set(ans)
                else:
                    value.set(0)

                self.checked.append(value)
                tk.Checkbutton(self.answer_frame, wraplength=500,
                                justify="left", font="12", text=lst[i],
                                variable=self.checked[i], onvalue=i+1,
                                offvalue=0).pack(anchor='w', expand='true', fill='y')

    # Отчет времени
    def count_down(self, time_count=15, passed=0):
        self.time_limited.set(f"Прошло: {passed} мин. Осталось: {time_count} мин.")
        if time_count == 0:
            self.end_test()
        time_count -= 1
        passed += 1
        self.after(60000, self.count_down, time_count, passed)   #60 000 - минута

    # Завершительная страница теста
    def end_test(self):
        self.process = False
        self.points = 0
        points = 0
        self.rows_added = []
        self.all_points = []
        resize_window(self, 700, 700)
        self.close_win = tk.BooleanVar()
        self.name, _, tries = open_database(test_info=True)
        self.start_test_time = self.start_test.strftime("%H:%M:%S")
        self.end_test_time = dt.now().strftime("%H:%M:%S")
        self.duration = dt.strptime(self.end_test_time, "%H:%M:%S") - \
                    dt.strptime(self.start_test_time, "%H:%M:%S")

        # Подсчет баллов
        for i in range(self.max_ques):
            self.rows_added.append([i+1, self.student_answers[i]])
            if len(self.correct_answers[i]) == 1:
                correct = self.correct_answers[i][0]
                if self.student_answers[i] == correct:
                    self.points += 1
                    self.all_points.append(1)
                else:
                    self.all_points.append(0)
            else:
                num_answers = len(self.correct_answers[i])
                one_answer = round(1 / num_answers, 2)
                points = 0
                for ans in self.student_answers[i]:
                    if ans in self.correct_answers[i]:
                        self.points += one_answer
                        points += one_answer
                    elif points > 0:
                        self.points -= one_answer
                        points -= one_answer
                self.all_points.append(round(points, 2))

        # Вычисление оценки
        self.score = round(self.points * 100 / self.max_score, 2)
        if self.score >= 85:
            self.mark = "Отлично (5)"
        elif self.score < 85 and self.score >= 64:
            self.mark = "Хорошо (4)"
        elif self.score < 64 and self.score >= 42:
            self.mark = "Удовлетворительно (3)"
        else:
            self.mark = "Неудовлетворительно (2)"
        
        # Удаление старых виджетов
        old_widgets = self.pack_slaves()
        for widget in old_widgets:
            widget.destroy()

        # Расстановка новых виджетов
        tk.Label(self, font="bold 14",
                text="Тест завершен.\nНабрано баллов: " + \
                    f"{round(self.points, 2)} ({self.score}%)\n" + \
                    f"из {self.max_score} возможных баллов.\n" + \
                    f"Оценка: {self.mark}\n" + \
                    f"Потрачено времени: {self.duration}\n" + \
                    f"Проходил студент: {self.name}"
                    ).pack(pady=20, fill='both')

        # Таблица
        Table(self, headings=('Вопрос №', 'Выбранный ответ'),
                rows=self.rows_added
                ).pack(padx=200, pady=20,
                        expand="yes", fill='both')
        
        # Нижний фрейм
        tk.Checkbutton(self, text="Я подтверждаю, что " + \
                        "ознакомился с результатами теста.",
                        variable=self.close_win
                        ).pack(anchor='center')
        bot_frame = tk.Frame(self)
        bot_frame.pack(expand="yes", pady=20, anchor="center")
        
        # Если попытки кончились, то
        # не отображать кнопку "Пройти тест заново"
        if tries == 0:
            tk.Label(self, text="Попытки закончились! " + \
                        "Повторное прохождение теста более невозможно!"
                        ).pack(pady=(0,30), anchor='center',
                                fill='both')
            self.update_idletasks()
        else:
            tk.Button(bot_frame, height=3, text="Пройти тест заново",
                        command=self.restart
                        ).pack(side='left', fill='both')
        tk.Button(bot_frame, width=15, height=3, text="Выход",
                    command=self.close_window
                    ).pack(padx=10, side='left', fill='both')


    def restart(self):
        if self.close_win.get():
            self.destroy()
            window = User(self.parent)
            window.grab_set()
            window.focus_force()
        else:
            tk.messagebox.showwarning("Внимание",
                    "Подтвердите, что вы ознакомились с результатами.")

    # Событие закрытия приложения
    def close_window(self):
        if self.process and tk.messagebox.askokcancel("Выход",
                            "Вы уверены, что хотите досрочно " + \
                            "завершить тест и закрыть приложение?\n" + \
                            "Попытка будет потрачена."):
            self.end_test()
        elif not self.process:
            if self.close_win.get():
                passwrd = open_database(get_pass=True)
                test_day = dt.strftime(self.start_test, "%d.%m.%Y")

                data = [
                    test_day, self.start_test_time,
                    self.end_test_time, str(self.duration),
                    str(self.points) + " (" + str(self.score) + " %)",
                    self.mark, self.max_ques, self.max_score,
                    get_update_date(), self.all_points
                    ]

                report_message = create_new(self.name, self.rows_added,
                                            self.correct_answers,
                                            passwrd, data)

                if report_message:
                    tk.messagebox.showwarning("Ошибка", report_message)
                else:
                    self.parent.destroy()
            else:
                tk.messagebox.showwarning("Внимание",
                    "Подтвердите, что вы ознакомились с результатами.")
        

# Преподаватель
class Admin(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.status = tk.StringVar()
        self.last_update = tk.StringVar()
        self.student_name = tk.StringVar()
        self.last_update.set("Последнее обновление базы данных: " + \
                        get_update_date())
        
        self.time_limit = tk.IntVar()
        self.tries = tk.IntVar()
        name, time, tries = open_database(test_info=True)
        self.student_name.set(name)
        self.time_limit.set(time)
        self.tries.set(tries)

        resize_window(self, 470, 400)
        self.title("Данные теста")
        self.minsize(height=350, width=400)
        self.protocol("WM_DELETE_WINDOW", self.back)
        self.focus_force()

        tk.Label(self, textvariable=self.last_update
            ).pack(anchor="center", expand='yes',
                    fill='both', pady=(20,10))
        tk.Button(self, width=15, text="Загрузить тест",
                    command=self.update_test
                    ).pack(expand='yes', fill='both', padx=150)

        mid2_frame = tk.Frame(self)
        mid3_frame = tk.Frame(self)
        small_frame = tk.Frame(self)
        bot1_frame = tk.Frame(self)
        bot2_frame = tk.Frame(self)

        mid2_frame.pack(pady=(20,0), anchor="center", 
                        expand='yes', fill='both')
        mid3_frame.pack(anchor="center", expand='yes', fill='both')
        small_frame.pack(padx=(40,0), pady=(5,20), anchor="center", 
                        expand='yes', fill='both')

        tk.Button(self, width=15, text="Применить",
                    command=self.check_value
                    ).pack(expand='yes', fill='both', padx=150)
        tk.Label(self, textvariable=self.status
                    ).pack(anchor="center", expand='yes', fill='both')

        bot1_frame.pack(side="left", anchor="center",
                        pady=30, padx=(50,30), expand='yes', fill='both')
        bot2_frame.pack(side="left", anchor="center",
                        pady=30, padx=(0,50), expand='yes', fill='both')

        tk.Label(mid2_frame, text="Продолжительность теста (мин): "
                    ).pack(side='left', anchor='w',
                            fill='both', padx=(40,0))
        tk.Spinbox(mid2_frame, width=3, from_=5, to=180, increment=5,
                    textvariable=self.time_limit, state='readonly'
                    ).pack(side='left', fill='both')

        tk.Label(mid3_frame, text="Количество попыток: "
                    ).pack(side='left', anchor='w',
                        fill='both', padx=(40,0))
        tk.Spinbox(mid3_frame, width=3, from_=0, to=10,
                    textvariable=self.tries, state='readonly'
                        ).pack(side='left', fill='both')

        tk.Label(small_frame, text="ФИО студента: "
                    ).pack(side='left', anchor='w',
                        fill='both')
        tk.Entry(small_frame, width=40, textvariable=self.student_name
                    ).pack(side='left', anchor='w', fill='both')
        tk.Button(small_frame, text="Очистить", command=self.clear_entry
                    ).pack(side='left', anchor='w',
                    fill='both', padx=(5,30))

        tk.Button(bot1_frame, width=15, text="Сменить логин",
                    command=self.change_login
                    ).pack(expand='yes', pady=(0,20), fill='both')
        tk.Button(bot1_frame, width=15, text="Сменить пароль",
                    command=self.change_password
                    ).pack(expand='yes', fill='both')
        tk.Button(bot2_frame, width=15, text="Критерий оценивания",
                    command=self.evaluation_criterion
                    ).pack(expand='yes', pady=(0,20), fill='both')
        tk.Button(bot2_frame, width=15, text="Назад",
            command=self.back
            ).pack(expand='yes', fill='both')

    def clear_entry(self):
        self.student_name.set("")

    def check_value(self):
        name = self.student_name.get()
        time_limit = self.time_limit.get()
        tries = self.tries.get()
        message = open_database(name=name, time=time_limit, tries=tries)
        self.status.set(message)

    def change_login(self):
        window = NewLogin(self)
        window.grab_set()

    def change_password(self):
        window = NewPassword(self)
        window.grab_set()

    def evaluation_criterion(self):
        window = Criterion(self)
        window.grab_set()

    def update_test(self):
        window = UpdatingTest(self)
        window.grab_set()

    def back(self):
        self.destroy()
        self.parent.deiconify()


# Окно загрузки теста
class UpdatingTest(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        resize_window(self, 400, 250)
        self.title("Обновление теста")
        self.minsize(height=200, width=350)
        self.focus_force()

        self.parent = parent
        self.update_status = parent.last_update
        self.file_path = tk.StringVar()
        self.status = tk.StringVar()

        tk.Label(self, text="Для обновления теста выберите " + \
                    "Excel-файл с новым тестом."
                    ).pack(pady=(10,0), anchor="center",
                            expand='yes', fill='both')
        tk.Label(self, text="Внимание: старые данные будут " + \
                    "удалены из базы данных!"
                    ).pack(anchor="center", expand='yes',
                            fill='both')
        tk.Label(self, text="Данные будут загружены " + \
                "из файла по указанному пути:"
                ).pack(anchor='w', fill='both')
        
        top_frame = tk.Frame(self)
        top_frame.pack(expand="true", fill="y")
        tk.Label(self, textvariable=self.status
                    ).pack(anchor="center", fill='both')

        self.field = tk.Entry(top_frame, width=50,
                                textvariable=self.file_path)
        self.field.pack(side="left", padx=(20,5), pady=(10,0),
                        fill='both', anchor="center")

        tk.Button(top_frame, text="Файл",
                    command=self.open_file
                    ).pack(side="left", fill='both',
                            anchor="center")
        
        bot_frame = tk.Frame(self)
        bot_frame.pack(anchor="center", expand='yes',
                        pady=20, padx=30, fill='both')
        self.upload = tk.Button(bot_frame, width=10,
                                text="Загрузить", state='disable',
                                command=self.update_database)
        self.upload.pack(side="left", padx=(0,20),
                            expand='yes', fill='both')
        tk.Button(bot_frame, width=10, text="Назад",
                    command=self.destroy
                    ).pack(side="left", expand='yes',
                            fill='both')

    def open_file(self):
        self.file = filedialog.askopenfile(
                            filetypes=[("Excel files", "*.xlsx")])
        
        if self.file:
            self.file_path.set(self.file.name)
            self.field.xview_moveto(1)
            self.upload["state"] = "normal"
        
    def update_database(self):
        if path.exists(self.file_path.get()):
            self.status.set("Загрузка...")
            self.update_idletasks()
            message = open_database(self.file.name)
            self.status.set(message)
            self.update_status.set("Последнее обновление базы данных: " \
                                    + get_update_date())
            self.update_idletasks()
        else:
            self.status.set("Ошибка. Указанного файла не существует.")


# Смена логина
class NewLogin(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Смена логина")
        resize_window(self, 250, 250)
        self.minsize(height=150, width=150)
        self.login = tk.StringVar()
        self.status = tk.StringVar()

        tk.Label(self, text="Новый логин:").pack(pady=(15,0), expand='yes', fill='both')
        tk.Entry(self, textvariable=self.login).pack(expand='yes', fill='both', padx=30)
        tk.Label(self, textvariable=self.status).pack(expand='yes', fill='both')
        tk.Button(self, width=15, text="Сохранить",
                    command=self.confirm).pack(expand='yes', fill='both', padx=30)
        tk.Button(self, width=15, text="Закрыть",
                    command=self.destroy).pack(pady=30, expand='yes', fill='both', padx=30)
        self.bind('<Return>', self.confirm) 

    def confirm(self, event=None):
        new_login = self.login.get()
        if new_login == "":
            self.status.set("Введите логин")
        else:
            message = open_database(new_login=new_login)
            self.status.set(message)
        self.update_idletasks()


# Смена пароля
class NewPassword(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Смена пароля")
        resize_window(self, 200, 350)
        self.minsize(height=280, width=100)
        self.old_password = tk.StringVar()
        self.new_password = tk.StringVar()
        self.new_password_check = tk.StringVar()
        self.status = tk.StringVar()

        tk.Label(self, text="Старый пароль:").pack(pady=(15,0), expand='yes', fill='both')
        tk.Entry(self, textvariable=self.old_password, show="*").pack(expand='yes', fill='both', padx=30)
        tk.Label(self, text="Новый пароль:").pack(pady=(20,0), expand='yes', fill='both')
        tk.Entry(self, textvariable=self.new_password, show="*").pack(expand='yes', fill='both', padx=30)
        tk.Label(self, text="Повторите пароль:").pack(pady=(20,0), expand='yes', fill='both')
        tk.Entry(self, textvariable=self.new_password_check,
                    show="*").pack(expand='yes', fill='both', padx=30)
        tk.Label(self, textvariable=self.status).pack(pady=5, expand='yes', fill='both')
        tk.Button(self, width=15, text="Сохранить",
                    command=self.confirm).pack(expand='yes', fill='both', padx=30)
        tk.Button(self, width=15, text="Закрыть",
                    command=self.destroy).pack(pady=30, padx=30, expand='yes', fill='both')
        self.bind('<Return>', self.confirm) 

    def confirm(self, event=None):
        old = self.old_password.get()
        new = self.new_password.get()
        new_check = self.new_password_check.get()
        if old == "" or new == "" or new_check == "":
            self.status.set("Заполните все поля!")
        elif old == new and new == new_check:
            self.status.set("Данный пароль уже установлен!")
        else:
            if new == new_check:
                message = open_database(password=old, new_password=new)
                self.status.set(message)
            else:
                self.status.set("Пароли не совпадают!")
        self.update_idletasks()


# Изменение критерия оценки
class Criterion(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Критерий оценки")
        resize_window(self, 300, 300)
        self.minsize(height=280, width=250)

        self.mark5 = tk.IntVar()
        self.mark4 = tk.IntVar()
        self.mark3 = tk.IntVar()
        self.message = tk.StringVar()

        result = open_database(criterion=True)
        marks = tuple()
        for i in result:
            marks += (i[2],)
        
        self.mark5.set(marks[0])
        self.mark4.set(marks[1])
        self.mark3.set(marks[2])

        frame1 = tk.Frame(self)
        frame2 = tk.Frame(self)
        frame3 = tk.Frame(self)
        frame4 = tk.Frame(self)
        bot_frame = tk.Frame(self)

        tk.Label(self, text="Укажите нижний порог баллов, \n" + \
                "требуемых для достижения указанной оценки:").pack()
        frame1.pack(padx=(60,0), expand='yes', fill='x')
        frame2.pack(padx=(60,0), expand='yes', fill='x')
        frame3.pack(padx=(60,0), expand='yes', fill='x')
        frame4.pack(padx=(60,0), expand='yes', fill='x')
        tk.Label(self, textvariable=self.message).pack()
        bot_frame.pack(pady=10, expand='yes', fill='both')

        tk.Label(frame1, text="5 Отлично >= ").pack(side='left')
        tk.Entry(frame1, width=3,
                    textvariable=self.mark5).pack(side='left')
        tk.Label(frame1, text=" %").pack(side='left')
        tk.Label(frame2, text="4 Хорошо >= ").pack(side='left')
        tk.Entry(frame2, width=3,
                    textvariable=self.mark4).pack(side='left')
        tk.Label(frame2, text=" %").pack(side='left')
        tk.Label(frame3, text="3 Удовлетворительно >= "
                    ).pack(side='left')
        tk.Entry(frame3, width=3,
                    textvariable=self.mark3).pack(side='left')
        tk.Label(frame3, text=" %").pack(side='left')
        tk.Label(frame4, text="2 Неудовлетворительно: < "
                    ).pack(side='left')
        tk.Label(frame4, textvariable=self.mark3).pack(side='left')
        tk.Label(frame4, text=" %").pack(side='left')

        tk.Button(bot_frame, text="Применить",
                    command=self.set_marks
                    ).pack(padx=60, expand='yes',
                            fill='both')
        tk.Button(bot_frame, text="Отмена",
                    command=self.destroy
                    ).pack(padx=60, pady=20, expand='yes',
                            fill='both')

    def set_marks(self):
        try:
            mark5 = self.mark5.get()
            mark4 = self.mark4.get()
            mark3 = self.mark3.get()

            if mark5 > 100 or mark4 > 100 or mark3 > 100:
                self.message.set("Значение не может превышать 100%")
            elif mark5 <= mark4 or mark4 <= mark3:
                self.message.set("Значение не может превышать предыдущее!")
            else:
                self.message.set(open_database(mark=(mark5, mark4, mark3)))
        except:
            self.message.set("Значение должно быть целочисленным!")


# Расположение окна в центре экрана
def resize_window(window, width, height):
    w = (window.winfo_screenwidth() - width) // 2
    h = (window.winfo_screenheight() - height) // 2
    window.geometry(f'{width}x{height}+{w}+{h}')


# Получение даты изменения файла БД
def get_update_date():

    # Получаем абсолютный путь
    # database_path = resource_path("data_files/Database.db")
    database_path = path.abspath("Database.db")
    try:
        # Получаем дату последнего обновления файла Database.db
        c_time = path.getmtime(database_path)

        # Конвертируем секунды в дату
        date = ctime(c_time)

        # Конвертируем в список
        textdate = str(date).split()
        m = month.get(textdate[1])
        s = textdate[3]
        new_date = textdate[2] + \
            "." + m + "." + textdate[4] + " г. " + s[:-3]
    except OSError:
        print(f"По указанному пути: {database_path} \
                файл не существует, либо был перемещён.")
        new_date = "База данных не найдена."
    finally:
        return new_date


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = path.abspath(".")

    return path.join(base_path, relative_path)


if __name__ == "__main__":
    result = get_update_date()
    if result != "База данных не найдена.":
        app = Main()
        app.mainloop()
    else:
        messagebox.showerror("Ошибка", result)
