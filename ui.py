import sys  # Для доступа к аргументам командной строки
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

# Подкласс QMainWindow для настройки главного окна приложения
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()  # При создании подкласса из класса Qt, чтобы разрешить Qt настраивать объект, всегда нужно вызывать функцию super __init__.

        self.setWindowTitle("Приложение")

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