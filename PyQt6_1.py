from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton


import sys  # Для доступа к аргументам командной строки
from random import choice


window_titles = [
    'Мое приложение',
    'Мое приложение',
    'Все еще мое приложение',
    'Все еще мое приложение',
    'Что за?..',
    'Что за?..',
    'Это удивительно',
    'Это удивительно',
    'Что-то пошло не так'
]


# Подкласс QMainWindow для настройки главного окна приложения
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()  # При создании подкласса из класса Qt, чтобы разрешить Qt настраивать объект, всегда нужно вызывать функцию super __init__.

        self.n_times_clicked = 0

        self.setWindowTitle("Мое приложение")

        self.button = QPushButton("Нажми")
        self.button.clicked.connect(self.the_button_was_clicked)  # соединяем кнопку с функцией

        self.windowTitleChanged.connect(self.the_window_title_changed)  #  подключаем пользовательский метод the_window_title_changed слота к сигналу окна .windowTitleChanged

        # устанавливаем виджет по центру
        self.setCentralWidget(self.button)


    def the_button_was_clicked(self):
        print("Клик")
        new_window_title = choice(window_titles)
        print("Установка заголовка: %s" % new_window_title)
        self.setWindowTitle(new_window_title)


    def the_window_title_changed(self, window_title):
        print("Заголовок окна изменен: %s" % window_title)

        if window_title == 'Что-то пошло не так':
            self.button.setDisabled(True)

# Приложению нужен только один экземпляр QApplication
# Передаем sys.argv, чтобы разрешить аргументы командной строки приложения
# Если не нужно использовать аргументы командной строки, QApplication([]) тоже работает
app = QApplication(sys.argv)

# создание виджет Qt - окно.
window = MainWindow()
window.show()   # По умолчанию окно скрыто, поэтому нужно прописать show()

# Запуск цикла событий.
app.exec()
# Учебник https://habr.com/ru/company/skillfactory/blog/599599/