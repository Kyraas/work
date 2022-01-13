# Пример создания TableView. Данные нельзя менять, только просматривать

import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox
from tableview import Ui_MainWindow


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

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


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.table = QtWidgets.QTableView()

        data = QSqlQuery("SELECT * FROM 'Сертификаты'")    # SQL-запрос

        self.model = TableModel(data)
        self.table.setModel(self.model)

        self.setCentralWidget(self.table)

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


app=QtWidgets.QApplication(sys.argv)
if not createConnection():
    sys.exit(1)
window=MainWindow()
window.show()
sys.exit(app.exec())