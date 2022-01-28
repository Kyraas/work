# -*- coding: utf-8 -*-
# QSortFilterSqlQueryModel
from ctypes import resize
from email.header import Header
import sys

from PyQt6.QtCore import Qt
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableView
from tableview import Ui_MainWindow
# import siteparser

class Table(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.setWindowTitle("Таблица сертификатов")
        self.con = QSqlDatabase.addDatabase("QSQLITE") # Создаем объект БД с указанием типа (в данном случае sqlite)
        self.con.setDatabaseName("parseddata.db")    # указываем название файла БД
        self.con.open()
        self.tableView.setSortingEnabled(True)  # Активируем возможность сортировки по заголовкам в представлении
        # Модель
        self.model = QSqlQueryModel()   # Модель только для чтения данных, для наборов результатов SQL-запросов
        self.model.setQuery("SELECT * FROM Сертификаты", self.con)   # Создание SQL-запроса
        # QSortFilterProxyModel обеспечивает поддержку сортировки и фильтрации данных, передаваемых между другой моделью (QSqlQueryModel) и представлением (tableView)
        proxy = QtCore.QSortFilterProxyModel()
        proxy.setSourceModel(self.model)    # данная модель в качестве набора данных будет использовать QSqlQueryModel
        self.tableView.setModel(proxy)  # и также данная модель будет установлена в качестве представления данных
        self.model.setHeaderData(0, QtCore.Qt.Orientation.Horizontal, '№\nсертификата')
        self.model.setHeaderData(1, QtCore.Qt.Orientation.Horizontal, 'Дата\nвнесения\nв реестр')
        self.model.setHeaderData(2, QtCore.Qt.Orientation.Horizontal, 'Срок\nдействия\nсертификата')
        self.tableView.horizontalHeader().resizeSection(3, 300)
        self.model.setHeaderData(4, QtCore.Qt.Orientation.Horizontal, 'Наименования документов,\nтребованиям которых\nсоответствует средство')
        self.tableView.horizontalHeader().resizeSection(4, 200)
        self.tableView.horizontalHeader().resizeSection(5, 150)
        self.model.setHeaderData(6, QtCore.Qt.Orientation.Horizontal, 'Испытательная\nлаборатория')
        self.tableView.horizontalHeader().resizeSection(6, 150)
        self.model.setHeaderData(7, QtCore.Qt.Orientation.Horizontal, 'Орган по\nсертификации')
        self.tableView.horizontalHeader().resizeSection(7, 210)
        self.tableView.horizontalHeader().resizeSection(8, 300)
        self.model.setHeaderData(9, QtCore.Qt.Orientation.Horizontal, 'Реквизиты заявителя\n(индекс, адрес, телефон)')
        self.tableView.horizontalHeader().resizeSection(9, 300)
        self.model.setHeaderData(10, QtCore.Qt.Orientation.Horizontal, 'Информация об\nокончании срока\nтехнической\nподдержки,\nполученная\nот заявителя')
        self.tableView.resizeRowsToContents()   # Изменение размеров строк под длину данных
        
        self.pushButton.clicked.connect(self.query1)
        # self.pushButton_2.clicked.connect(self.testsort)
        self.lineEdit.textChanged.connect(self.search)
        self.checkBox.stateChanged.connect(self.valid)

    def query1(self):
        self.model.setQuery("SELECT * FROM Сертификаты", self.con)
        self.tableView.resizeRowsToContents()

    def valid(self):
        if self.checkBox.isChecked():
            # qvalid = """AND "Срок действия сертификата" NOT BETWEEN date("Срок действия сертификата") AND date('now') ORDER BY date("Срок действия сертификата")  """
            self.model.setQuery("""SELECT * FROM Сертификаты WHERE "Срок действия сертификата" NOT BETWEEN date("Срок действия сертификата") AND date('now') ORDER BY date("Срок действия сертификата")  """, self.con)
            self.tableView.resizeRowsToContents()
        else:
            qvalid = ""
            self.query1()
            self.tableView.resizeRowsToContents()
        return qvalid

    def search(self):
        text = self.lineEdit.text()
        # =========== Не работает =============
        # query = QSqlQuery(self.con)
        # query.prepare(""" SELECT * FROM Сертификаты WHERE "Наименование средства (шифр)" LIKE ? """)
        # query.addBindValue(text)
        # if query.exec():
        #     self.model.setQuery(query)
        qsearch = """ SELECT * FROM Сертификаты WHERE ("№ сертификата" LIKE "%{}%" OR "Дата внесения в реестр" LIKE "%{}%" OR "Срок действия сертификата" LIKE "%{}%" OR "Наименование средства (шифр)" LIKE "%{}%" OR "Наименования документов, требованиям которых соответствует средство" LIKE "%{}%" OR "Схема сертификации" LIKE "%{}%" OR "Испытательная лаборатория" LIKE "%{}%" OR "Орган по сертификации" LIKE "%{}%" OR "Заявитель" LIKE "%{}%" OR "Реквизиты заявителя (индекс, адрес, телефон)" LIKE "%{}%" OR "Информация об окончании срока технической поддержки, полученная от заявителя" LIKE "%{}%" ) """ + self.valid()
        self.model.setQuery(qsearch.format(text, text, text, text, text, text, text, text, text, text, text))
        self.tableView.resizeRowsToContents()



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