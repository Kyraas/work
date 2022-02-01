# -*- coding: utf-8 -*-
# https://github.com/FokinAleksandr/PyQT-CRUD-App/blob/f0933cbbb2c6b85b9bce83ecc0be4490a6b8c210/app/tablewidgets/employees.py#L111
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import QtCore
from tableview import Ui_MainWindow
from AbstractModel import MyTableModel
from orm import Certificate as tbl, conn
import sqlalchemy as db
from sqlalchemy.sql import func
from siteparser import parse, update_table
from six_months import half_year

class Table(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.setWindowTitle("Таблица сертификатов")
        self.status = self.statusBar()
        self.status.showMessage('Установлено соединение с SQL.')

        # Модель
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
        self.refreshButton.clicked.connect(self.refresh)
        self.checkBox_red.stateChanged.connect(self.red)
        self.checkBox_pink.stateChanged.connect(self.pink)
        self.checkBox_yellow.stateChanged.connect(self.yellow)
        self.checkBox_gray.stateChanged.connect(self.gray)
        self.checkBox_white.stateChanged.connect(self.white)
        self.searchBar.textChanged.connect(self.search)

    def refresh(self):
        self.refreshButton.setEnabled(False)
        self.status.showMessage('Получаем данные с сайта ФСТЭК России...')
        self.status.repaint()
        data = parse()  # получаем результат функции parse
        if data != False:
            self.status.showMessage('Обновляем базу данных...')
            self.status.repaint()
            text = update_table(data)
            self.status.showMessage(text)
            self.refreshButton.setEnabled(True)
        else:
            self.status.showMessage('Нет соединения с сайтом ФСТЭК России.')
            self.status.repaint()

    def red(self):
        red_filter = (tbl.support <= func.current_date()) & (tbl.date_end <= func.current_date()) & (tbl.support != '')
        if self.checkBox_red.isChecked():
            self.myquery(red_filter)
        else:
            self.myquery()

    def pink(self):
        pink_filter = (tbl.support <= func.current_date()) & (tbl.date_end > func.current_date()) & (tbl.support != '')
        if self.checkBox_pink.isChecked():
            self.myquery(pink_filter)
        else:
            self.myquery()

    def yellow(self):
        yellow_filter = (tbl.date_end <= func.current_date()) & (tbl.support > func.current_date())
        if self.checkBox_yellow.isChecked():
            self.myquery(yellow_filter)
        else:
            self.myquery()

    def gray(self):
        gray_filter = (tbl.date_end <= half_year()) & (tbl.date_end > func.current_date())
        if self.checkBox_gray.isChecked():
            self.myquery(gray_filter)
        else:
            self.myquery()
    
    def white(self):
        white_filter = (tbl.support > func.current_date()) & (tbl.date_end > func.current_date())
        if self.checkBox_white.isChecked():
            self.myquery(white_filter)
        else:
            self.myquery()

        
    def search(self, text):
        search_filter = tbl.name.like('%{}%'.format(text)) | tbl.docs.like('%{}%'.format(text)) | tbl.scheme.like('%{}%'.format(text)) | tbl.lab.like('%{}%'.format(text)) | tbl.certification.like('%{}%'.format(text)) | tbl.applicant.like('%{}%'.format(text)) | tbl.requisites.like('%{}%'.format(text)) | tbl.id.like('%{}%'.format(text)) | tbl.date_start.like('%{}%'.format(text)) | tbl.date_end.like('%{}%'.format(text)) | tbl.support.like('%{}%'.format(text))
        
        if self.checkBox_pink.isChecked():
            search_filter = search_filter & (tbl.support < func.current_date())
        # if self.checkBox2.isChecked():
            # search_filter = search_filter & 
            # ...
        self.myquery(search_filter)

    def myquery(self, *args):
        instanse = conn.execute(db.select([tbl]).filter(*args)).fetchall()
        self.model.update(instanse)
        self.tableView.resizeRowsToContents()

    def closeEvent(self, event):
        if conn:
            conn.close()    # закрываем соединение с бд
            print("Соединение с SQLite закрыто.")
        event.accept()

    
app = QApplication(sys.argv)
win = Table()
win.show()
sys.exit(app.exec())
