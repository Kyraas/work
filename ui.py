# Образец создания TableView. Заполнение данными работает. Их можно менять
# https://realpython.com/python-pyqt-database/
# как делать нередактируемую таблицу: (через Designer) https://stpuackoverflow.com/questions/1328492/qtableview-not-allow-user-to-edit-cell
# -*- coding: utf-8 -*-
import sys

from PyQt6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableView
from tableview import Ui_MainWindow
# import siteparser

class Table(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.setWindowTitle("Таблица сертификатов")
        # self.resize(1015, 600)
        # Модель
        self.model = QSqlTableModel(self)   # модель, позволяющая менять данные
        self.model.setTable("Сертификаты")  # Соединение модели со существующей таблицей "Сертификаты"
        self.model.select() # Загрузка данных из таблицы и заполнение модели ими 
        # Представление
        self.tableView.setModel(self.model)  # Соединение представления tableView (tableview.py) и модели QSqlTableModel
        # self.tableView.resizeColumnsToContents() # Изменение размеров колонок под длину данных
        # self.setCentralWidget(self.tableView)    # Расположение представления по центру
        # self.pushButton_4.clicked.connect(reflesh)
        # self.pushButton.clicked.connect(query)


def createConnection(): # Соединение с БД
    con = QSqlDatabase.addDatabase("QSQLITE") # Создаем объект БД с указанием типа (в данном случае sqlite)
    con.setDatabaseName("parseddata.db")    # указываем название файла БД
    if not con.open():  # Если True (not False), то выводим ошибку подключения
        QMessageBox.critical(
            None,
            "Таблица сертификатов - Ошибка!",
            "Ошибка базы данных: %s" % con.lastError().databaseText(),
        )
        return False    # В ином случае выводим False, подключение успешно установлено
    return True

# self.pushButton_2.clicked.connect(self.tableView.show)
# def show(model):
#     print("click")
#     model.select() # Загрузка данных из таблицы и заполнение модели ими 

# def query(con):
#     query_id = QSqlQuery()
#     query_id.exec(""" SELECT '№ сертификата' FROM Сертификаты """)
#     print(con.tables())

app = QApplication(sys.argv)
if not createConnection():
    sys.exit(1) # Закрываем приложение при ошибке подключения
win = Table()
win.show()
sys.exit(app.exec())