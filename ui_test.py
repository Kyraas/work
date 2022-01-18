# -*- coding: utf-8 -*-
# QSortFilterSqlQueryModel
import sys

from PyQt6.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableView
from tableview import Ui_MainWindow
# import siteparserpyqt

class Table(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.setWindowTitle("Таблица сертификатов")
        self.con = QSqlDatabase.addDatabase("QSQLITE") # Создаем объект БД с указанием типа (в данном случае sqlite)
        self.con.setDatabaseName("parseddata.db")    # указываем название файла БД
        self.con.open()
        # self.resize(1015, 600)
        # Модель
        self.model = QSqlQueryModel(self)   # модель, позволяющая менять данные
        self.model.setQuery("SELECT * FROM Сертификаты", self.con)   # Создание SQL-запроса
        # Представление
        self.tableView.setModel(self.model)  # Соединение представления tableView (tableview.py) и модели QSqlTableModel
        # self.tableView.resizeColumnsToContents() # Изменение размеров колонок под длину данных
        # self.setCentralWidget(self.tableView)    # Расположение представления по центру
        self.pushButton.clicked.connect(self.query1)
        self.pushButton_2.clicked.connect(self.testsort)
        self.lineEdit.textChanged.connect(self.search)

    def query1(self):
        self.model.setQuery("SELECT * FROM Сертификаты", self.con) 

    def testsort(self):
        self.model.setQuery("""SELECT * FROM Сертификаты ORDER BY "Дата внесения в реестр" """, self.con) 

    def search(self):
        text = self.lineEdit.text()
        # =========== Не работает =============
        # query = QSqlQuery(self.con)
        # query.prepare(""" SELECT * FROM Сертификаты WHERE "Наименование средства (шифр)" LIKE ? """)
        # query.addBindValue(text)
        # if query.exec():
        #     self.model.setQuery(query)
        self.model.setQuery(""" SELECT * FROM Сертификаты WHERE ("№ сертификата" LIKE "%{}%" OR "Дата внесения в реестр" LIKE "%{}%" OR "Срок действия сертификата" LIKE "%{}%" OR "Наименование средства (шифр)" LIKE "%{}%" OR "Наименования документов, требованиям которых соответствует средство" LIKE "%{}%" OR "Схема сертификации" LIKE "%{}%" OR "Испытательная лаборатория" LIKE "%{}%" OR "Орган по сертификации" LIKE "%{}%" OR "Заявитель" LIKE "%{}%" OR "Реквизиты заявителя (индекс, адрес, телефон)" LIKE "%{}%" OR "Информация об окончании срока технической поддержки, полученная от заявителя" LIKE "%{}%" ) """.format(text, text, text, text, text, text, text, text, text, text, text))



app = QApplication(sys.argv)
win = Table()
if not win.con.open():  # Если True (not False), то выводим ошибку подключения
        QMessageBox.critical(
            None,
            "Таблица сертификатов - Ошибка!",
            "Ошибка базы данных: %s" % win.con.lastError().databaseText(),
        )
win.show()
sys.exit(app.exec())

# 
# SELECT * FROM "Сертификаты" WHERE ("№ сертификата" LIKE '%h%' ESCAPE '\' OR "Дата внесения в реестр" LIKE '%h%' ESCAPE '\' OR
# "Срок действия сертификата" LIKE '%h%' ESCAPE '\' OR
# "Наименование средства (шифр)" LIKE '%h%' ESCAPE '\' OR
# "Наименования документов, требованиям которых соответствует средство" LIKE '%h%' ESCAPE '\' OR
# "Схема сертификации" LIKE '%h%' ESCAPE '\' OR "Испытательная лаборатория" LIKE '%h%' ESCAPE '\' OR
# "Орган по сертификации" LIKE '%h%' ESCAPE '\' OR "Заявитель" LIKE '%h%' ESCAPE '\' OR
# "Реквизиты заявителя (индекс, адрес, телефон)" LIKE '%h%' ESCAPE '\' OR
# "Информация об окончании срока технической поддержки, полученная от заявителя" LIKE '%h%' ESCAPE '\')