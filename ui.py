# Образец создания TableView. Заполнение данными работает. Их можно менять
# https://realpython.com/python-pyqt-database/
# как делать нередактируемую таблицу: (через Designer) https://stpuackoverflow.com/questions/1328492/qtableview-not-allow-user-to-edit-cell
# -*- coding: utf-8 -*-
import sys

from PyQt6.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableView
from tableview import Ui_MainWindow
# import siteparser

class Table(QMainWindow, Ui_MainWindow):
    def __init__(self, con):
        super().__init__(parent=None)
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        # self.con = QSqlDatabase.addDatabase("QSQLITE") # Создаем объект БД с указанием типа (в данном случае sqlite)
        # self.con.setDatabaseName("parseddata.db")    # указываем название файла БД
        self.setWindowTitle("Таблица сертификатов")
        self.resize(1100, 800)
        # Модель
        self.model = QSqlQueryModel(self)   # создаем модель, позволяющую только просматривать данные (нельзя их изменять)
        self.model.setQuery("SELECT * FROM Сертификаты", con)   # Создание SQL-запроса
        # self.model.setQuery("SELECT '№ сертификата' FROM Сертификаты", con)
        # self.model.setTable("Сертификаты")  # Соединение модели со существующей таблицей "Сертификаты"
        # self.model.select() # Загрузка данных из таблицы и заполнение модели ими 
        # Представление
        self.tableView.setModel(self.model)  # Соединение представления модели QSqlTableModel
        # self.tableView.resizeColumnsToContents() # Изменение размеров колонок под длину данных
        # self.setCentralWidget(self.tableView)    # Расположение представления по центру
        self.tableView.resize(1080, 725)
        self.pushButton.clicked.connect(self.query)


    def query(self):
    # model = QSqlQueryModel()
        self.model.setQuery(" SELECT '№ сертификата' FROM Сертификаты ", con)


con = QSqlDatabase.addDatabase("QSQLITE") # Создаем объект БД с указанием типа (в данном случае sqlite)
con.setDatabaseName("parseddata.db")    # указываем название файла БД
if not con.open():  # Если True (not False), то выводим ошибку подключения
    QMessageBox.critical(
        None,
        "Таблица сертификатов - Ошибка!",
        "Ошибка базы данных: %s" % con.lastError().databaseText(),
        )
    sys.exit(1) # Закрываем приложение при ошибке подключения

app = QApplication(sys.argv)
win = Table(con)
win.show()
sys.exit(app.exec())