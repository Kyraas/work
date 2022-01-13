# В данном проекте подключается готовый ui (TableWidget) и выводится. Заполнение таблицы данными из базы данных не работает

import sys

from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidget, QTableWidgetItem
from table import Ui_MainWindow

class Table(QMainWindow):
    def __init__(self):
        super().__init__()
        self._data = data
        data = QSqlQuery("SELECT * FROM 'Сертификаты'")
        self.setWindowTitle("Таблица сертификатов")
        self.view = Ui_MainWindow()
        self.view.setupUi(self)
        # self.view.setColumnCount(11)    # Создаем заголовки таблицы

        # query = QSqlQuery("SELECT * FROM 'Сертификаты'")    # SQL-запрос

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

def createConnection():
    con = QSqlDatabase.addDatabase("QSQLITE")
    con.setDatabaseName("parseddata.db")
    if not con.open():
        QMessageBox.critical(
            None,
            "Таблица сертификатов - Ошибка!",
            "Ошибка базы данных: %s" % con.lastError().databaseText(),
        )
        return False
    return True

app = QApplication(sys.argv)
if not createConnection():
    sys.exit(1)
win = Table()
win.show()
sys.exit(app.exec())