# -*- coding: utf-8 -*-
# https://evileg.com/en/forum/topic/706/
import sys

from PyQt6.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableView
from tableview import Ui_MainWindow
import sqlite3
# import siteparserpyqt

class Table(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.setWindowTitle("Таблица сертификатов")
        self.con = sqlite3.connect("parseddata.db") # соединение с бд
        self.cur = self.con.cursor() # создание курсора
        # self.resize(1015, 600)
        # Модель
        self.model = QSqlQueryModel(self)   # модель, позволяющая менять данные
        self.cur.execute("SELECT * FROM Сертификаты")
        # Представление
        self.tableView.setModel(self.model)  # Соединение представления tableView (tableview.py) и модели QSqlTableModel
        # self.tableView.resizeColumnsToContents() # Изменение размеров колонок под длину данных
        # self.setCentralWidget(self.tableView)    # Расположение представления по центру
        # self.pushButton.clicked.connect(self.query1)
        # self.pushButton_2.clicked.connect(self.query2)
        # self.textEdit.textChanged.connect(self.search)
        # self.text = self.textEdit.toPlainText()

    # def query1(self):
    #     self.cur.execute(""" SELECT "№ сертификата" FROM Сертификаты """, self.con)


    # def query2(self):
    #     self.model.setQuery(""" SELECT * FROM Сертификаты """, self.con)


    # def search(self):
    #     text = self.textEdit.toPlainText()
    #     # self.model.setQuery(" SELECT * FROM Сертификаты WHERE * LIKE :text", self.con, text)


app = QApplication(sys.argv)
win = Table()
if not win.con:  # Если True (not False), то выводим ошибку подключения
        QMessageBox.critical(
            None,
            "Таблица сертификатов - Ошибка!",
            "Ошибка базы данных: %s" % win.con.lastError().databaseText(),
        )
win.show()
sys.exit(app.exec())