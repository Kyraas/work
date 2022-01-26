# -*- coding: utf-8 -*-
# https://github.com/FokinAleksandr/PyQT-CRUD-App/blob/f0933cbbb2c6b85b9bce83ecc0be4490a6b8c210/app/tablewidgets/employees.py#L111
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import QtCore
from tableview import Ui_MainWindow
from AbstractModel import MyTableModel
import sqlalchemy as db
from orm import Certificate, conn
from sqlalchemy.sql import func
# import siteparser

class Table(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.setWindowTitle("Таблица сертификатов")

        # Модель
        # results = conn.execute(db.select([Certificate])).fetchall()
        self.model = MyTableModel()

        # Представление
        self.tableView.setSortingEnabled(True)  # Активируем возможность сортировки по заголовкам в представлении

        # QSortFilterProxyModel обеспечивает поддержку сортировки и фильтрации данных, передаваемых между другой моделью (QSqlQueryModel) и представлением (tableView)
        self.proxy = QtCore.QSortFilterProxyModel()
        self.proxy.setDynamicSortFilter(True)
        self.proxy.setSourceModel(self.model)
        self.tableView.setModel(self.proxy)  # и также данная модель будет установлена в качестве представления данных

        # Приведение заголовков таблицы к желаемому виду
        self.tableView.horizontalHeader().resizeSection(3, 300)
        self.tableView.horizontalHeader().resizeSection(4, 200)
        self.tableView.horizontalHeader().resizeSection(5, 150)
        self.tableView.horizontalHeader().resizeSection(6, 150)
        self.tableView.horizontalHeader().resizeSection(7, 210)
        self.tableView.horizontalHeader().resizeSection(8, 300)
        self.tableView.horizontalHeader().resizeSection(9, 300)
        self.tableView.horizontalHeader().resizeSection(10, 103)
        self.tableView.resizeRowsToContents()   # Изменение размеров строк под длину данных
        
        # Соединяем виджеты с функциями
        # self.pushButton.clicked.connect(self.refresh)
        self.checkBox.stateChanged.connect(self.query)
        self.lineEdit.textChanged.connect(self.search)

    # def refresh(self):
        # results = conn.execute(db.select([Certificate])).fetchall()
        # text = 'Гром'
        # self.model.update(results)

    def query(self):
        if self.checkBox.isChecked():
            results = conn.execute(db.select([Certificate]).filter(Certificate.date_end >= func.current_date()).order_by(Certificate.date_end)).fetchall()
            self.model.update(results)
        else:
            results = conn.execute(db.select([Certificate])).fetchall()
            self.model.update(results)

    def search(self, text):
        print(text)
        results = conn.execute(db.select([Certificate]).filter(Certificate.name.like('%{}%'.format(text)))).fetchall()
        self.model.update(results)
    
app = QApplication(sys.argv)
win = Table()
win.show()
sys.exit(app.exec())
