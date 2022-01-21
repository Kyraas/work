# -*- coding: utf-8 -*-
# QSortFilterSqlQueryModel
import sys

from PyQt6 import QtCore
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from tableview import Ui_MainWindow
# import siteparser

class Table(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        # Соединение с нашей таблицей
        self.setWindowTitle("Таблица сертификатов")
        self.con = QSqlDatabase.addDatabase("QSQLITE") # Создаем объект БД с указанием типа (в данном случае sqlite)
        self.con.setDatabaseName("parseddata.db")    # указываем название файла БД
        self.con.open()

        # Представление
        self.tableView.setSortingEnabled(True)  # Активируем возможность сортировки по заголовкам в представлении

        # Модель
        self.model = QSqlTableModel()   # Модель только для чтения данных, для наборов результатов SQL-запросов
        self.model.setTable("Сертификаты")
        self.model.select()

        # QSortFilterProxyModel обеспечивает поддержку сортировки и фильтрации данных, передаваемых между другой моделью (QSqlQueryModel) и представлением (tableView)
        self.proxy = QtCore.QSortFilterProxyModel()
        self.proxy.setSourceModel(self.model)    # данная модель в качестве набора данных будет использовать QSqlQueryModel
        self.tableView.setModel(self.proxy)  # и также данная модель будет установлена в качестве представления данных

        # Приведение заголовков таблицы к желаемому виду
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
        
        # Соединяем виджеты с функциями
        # self.pushButton.clicked.connect(self.query1)
        # self.checkBox.stateChanged.connect(self.valid)
        self.lineEdit.textChanged.connect(self.proxy.setFilterRegularExpression)

    # def query1(self):
    # def valid(self):
    #     if self.checkBox.isChecked():
    #         self.proxy.eventFilter(" NOT BETWEEN date('Срок действия сертификата') AND date('now') ORDER BY date('Срок действия сертификата') ")
    #         # self.model.select()
    #         self.tableView.resizeRowsToContents()   # Изменение размеров строк под длину данных

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

# =========== Не работает =============
# query = QSqlQuery(self.con)
# query.prepare(""" SELECT * FROM Сертификаты WHERE "Наименование средства (шифр)" LIKE ? """)
# query.addBindValue(text)
# if query.exec():
#     self.model.setQuery(query)
