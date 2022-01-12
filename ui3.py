import sys

from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidget, QTableWidgetItem
from table import Ui_MainWindow
# from table import Ui_MainWindow

class Table(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Таблица сертификатов")
        self.view = Ui_MainWindow()
        self.view.setupUi(self)
        self.view.setColumnCount(11)    # Создаем заголовки таблицы

app = QApplication(sys.argv)
win = Table()
win.show()
sys.exit(app.exec())