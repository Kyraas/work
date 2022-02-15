# -*- coding: utf-8 -*-
# https://github.com/FokinAleksandr/PyQT-CRUD-App/blob/f0933cbbb2c6b85b9bce83ecc0be4490a6b8c210/app/tablewidgets/employees.py#L111
# https://stackoverflow.com/questions/60353152/qtablewidget-resizerowstocontents-very-slow

import sys
from datetime import *
from tkinter.ttk import Progressbar
from PyQt6.QtWidgets import QApplication, QMainWindow, QButtonGroup, QProgressBar
from PyQt6 import QtCore
from PyQt6.QtCore import QSortFilterProxyModel
from tableview import Ui_MainWindow
from AbstractModel import MyTableModel
from orm import Certificate as tbl, conn
import sqlalchemy as db
from sqlalchemy.sql import func
from siteparser import parse, update_table, count_rows, commit_db
from six_months import half_year
from last_update import get_update_date

class Table(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Инициализация нашего дизайна
        self.setWindowTitle("Таблица сертификатов")
        self.status = self.statusBar()

        # Модель
        self.model = MyTableModel()

        # Прокси модель (поиск и сортировка по возрастанию\убыванию)
        self.proxy = QSortFilterProxyModel()
        self.proxy.setSourceModel(self.model)
        self.proxy.setDynamicSortFilter(False)
        self.proxy.setFilterKeyColumn(-1)   # Поиск по всей таблице (все колонки)
        self.proxy.setFilterCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)

        # Считаем строки при запуске программы
        n = self.proxy.rowCount()                    
        self.status.showMessage(f'Всего сертификатов: {n}.')
        self.status.setStyleSheet("background-color : #D8D8D8") # серый

        # Проверяем дату последнего изменения файла базы данных
        self.last_update_date.setText(get_update_date())

        # Инициализируем progressbar
        data = parse()  # парсим сайт
        if data != False:
            max = count_rows(data)  # маскимальное кол-во строк
            self.progressbar = QProgressBar(maximum=max)    # задаем максимум progressbar'у
            self.statusBar().addPermanentWidget(self.progressbar)   # добавляем progressbar в statusbar
            self.progressbar.setStyleSheet("max-height: 12px")  # задаем стиль
            self.progressbar.setHidden(False)   # пока что скрываем progressbar
        else:
            self.status.setStyleSheet("background-color : #FF9090") # бледно-красный
            self.status.showMessage('Нет соединения с сайтом ФСТЭК России.') 
            self.status.repaint()
            self.refreshButton.setEnabled(False)

        # Представление
        self.tableView.setModel(self.proxy)
        self.tableView.setSortingEnabled(True)  # Активируем возможность сортировки по заголовкам в представлении

        # Приведение заголовков таблицы к желаемому виду
        self.tableView.setColumnHidden(0, True) # Скрываем rowid
        self.tableView.horizontalHeader().resizeSection(1, 80)
        self.tableView.horizontalHeader().resizeSection(2, 70)
        self.tableView.horizontalHeader().resizeSection(3, 80)
        self.tableView.horizontalHeader().resizeSection(4, 300)
        self.tableView.horizontalHeader().resizeSection(5, 200)
        self.tableView.horizontalHeader().resizeSection(6, 150)
        self.tableView.horizontalHeader().resizeSection(7, 150)
        self.tableView.horizontalHeader().resizeSection(8, 210)
        self.tableView.horizontalHeader().resizeSection(9, 300)
        self.tableView.horizontalHeader().resizeSection(10, 300)
        self.tableView.horizontalHeader().resizeSection(11, 103)
        self.tableView.resizeRowsToContents()   # Высота строк подстраивается под содержимое. Замедляет запуск приложения!!!
        
        # Создаем группу фильтров
        self.filters = QButtonGroup(self)
        self.filters.addButton(self.radioButton_red)
        self.filters.addButton(self.radioButton_pink)
        self.filters.addButton(self.radioButton_yellow)
        self.filters.addButton(self.radioButton_gray)
        self.filters.addButton(self.radioButton_white)

        # Соединяем виджеты с функциями
        self.refreshButton.clicked.connect(self.refresh)
        self.radioButton_red.clicked.connect(self.red)
        self.radioButton_pink.clicked.connect(self.pink)
        self.radioButton_yellow.clicked.connect(self.yellow)
        self.radioButton_gray.clicked.connect(self.gray)
        self.radioButton_white.clicked.connect(self.white)
        self.checkBox_date.stateChanged.connect(self.white)
        self.checkBox_sup.stateChanged.connect(self.white)
        self.resetButton.clicked.connect(self.reset)
        self.searchButton.clicked.connect(self.search)
        self.proxy.layoutChanged.connect(self.tableView.resizeRowsToContents)   # при изменении отображения вызываем функцию resizeRowsToContents

    # Методы класса
    def search(self):
        self.status.setStyleSheet("background-color : #FFFF89")
        self.status.showMessage('Поиск...')
        self.status.repaint()
        self.proxy.layoutAboutToBeChanged.emit()
        self.proxy.setFilterRegularExpression(self.searchBar.text())
        if self.searchBar.text() == '':
            self.status.setStyleSheet("background-color : #FFFF89")
            self.status.showMessage('Загрузка...')
            self.status.repaint()
            self.proxy.sort(-1, QtCore.Qt.SortOrder.AscendingOrder) # при пустой строке поиска возвращаем строки к исходному виду
        self.proxy.layoutChanged.emit()
        n = self.proxy.rowCount()
        if n != 0:
            self.status.setStyleSheet("background-color : #D8D8D8") # серый
            self.status.showMessage(f'Сертификатов: {n}.')
        else:
            self.status.setStyleSheet("background-color : #D8D8D8")
            self.status.showMessage('По данному запросу не найдено.')
        self.status.repaint()

    def refresh(self):  # Обновление БД
        self.refreshButton.setEnabled(False)    # во время обновления базы делаем кнопку неактивной
        self.status.setStyleSheet("background-color : pink")
        self.status.showMessage('Получаем данные с сайта ФСТЭК России...')
        self.status.repaint()
        data = parse()  # получаем результат функции parse
        if data != False:

            # Начало обновления базы
            self.status.showMessage('Обновление базы...')
            self.status.repaint()
            self.progressbar.setHidden(False)   # отображаем progressbar
            rows = update_table(data)   # получаем кол-во строк, внесенных в базу
            for row in rows:
                self.progressbar.setValue(row)
            self.status.showMessage('Загрузка таблицы...')
            self.status.repaint()
            results = conn.execute(db.select([tbl])).fetchall()
            self.model.update(results)

            # Завершение обновления базы
            self.progressbar.setHidden(True)    # скрываем progressbar при завершении обновления базы
            final = commit_db() # получаем сообщение об успешном обновлении
            n = self.proxy.rowCount()
            self.status.setStyleSheet("background-color : #ADFF94") # салатовый FF9090
            self.status.showMessage(f'{final} Всего сертификатов: {n}.')
            self.refreshButton.setEnabled(True) # делаем кнопку снова активной
            self.last_update_date.setText(get_update_date())    # обновляем дату изменения файла базы данных
        else:
            self.status.setStyleSheet("background-color : #FF9090") # бледно-красный
            self.status.showMessage('Нет соединения с сайтом ФСТЭК России.') 
            self.status.repaint()

    def red(self):  # Сертификат и поддержка не действительны
        red_filter = (tbl.support <= func.current_date()) & (tbl.date_end <= func.current_date()) & (tbl.support != '')
        if self.radioButton_red.isChecked():
            self.myquery(red_filter)
            if self.checkBox_date.isEnabled:
                if self.checkBox_date.isChecked:
                    self.checkBox_date.setChecked(False)
                if self.checkBox_sup.isChecked:
                    self.checkBox_sup.setChecked(False)
                self.checkBox_date.setEnabled(False)
                self.checkBox_sup.setEnabled(False)

    def pink(self): # Поддержка не действительна
        pink_filter = (tbl.support <= func.current_date()) & (tbl.date_end > func.current_date()) & (tbl.support != '')
        if self.radioButton_pink.isChecked():
            self.myquery(pink_filter)
            if self.checkBox_date.isEnabled:
                if self.checkBox_date.isChecked:
                    self.checkBox_date.setChecked(False)
                if self.checkBox_sup.isChecked:
                    self.checkBox_sup.setChecked(False)
                self.checkBox_date.setEnabled(False)
                self.checkBox_sup.setEnabled(False)

    def yellow(self):   # Сертификат не действителен
        yellow_filter = (tbl.date_end <= func.current_date()) & (tbl.date_end != '#Н/Д')
        if self.radioButton_yellow.isChecked():
            self.myquery(yellow_filter)
            if self.checkBox_date.isEnabled:
                if self.checkBox_date.isChecked:
                    self.checkBox_date.setChecked(False)
                if self.checkBox_sup.isChecked:
                    self.checkBox_sup.setChecked(False)
                self.checkBox_date.setEnabled(False)
                self.checkBox_sup.setEnabled(False)
            
    def gray(self): # Сертификат истечёт менее, чем через полгода
        gray_filter = (tbl.date_end <= half_year()) & (tbl.date_end > func.current_date())
        if self.radioButton_gray.isChecked():
            self.myquery(gray_filter)
            if self.checkBox_date.isEnabled:
                if self.checkBox_date.isChecked:
                    self.checkBox_date.setChecked(False)
                if self.checkBox_sup.isChecked:
                    self.checkBox_sup.setChecked(False)
                self.checkBox_date.setEnabled(False)
                self.checkBox_sup.setEnabled(False)

    def white(self):    # Сертификат и поддержка действительны
        white_filter = (tbl.support > func.current_date()) & (tbl.date_end > func.current_date())
        if self.radioButton_white.isChecked():
            self.checkBox_date.setEnabled(True)
            self.checkBox_sup.setEnabled(True)
            if self.checkBox_date.isChecked():
                white_filter = white_filter + (tbl.date_end == '#Н/Д')
            if self.checkBox_sup.isChecked():
                white_filter = white_filter + ((tbl.date_end > func.current_date()) & (tbl.support == ''))
            self.myquery(white_filter)

    def reset(self):    # Сброс фильтров
        self.checkBox_date.setChecked(False)
        self.checkBox_sup.setChecked(False)
        self.checkBox_date.setEnabled(False)
        self.checkBox_sup.setEnabled(False)
        self.filters.setExclusive(False)
        self.radioButton_red.setChecked(False)
        self.radioButton_pink.setChecked(False)
        self.radioButton_yellow.setChecked(False)
        self.radioButton_gray.setChecked(False)
        self.radioButton_white.setChecked(False)
        self.filters.setExclusive(True)
        self.myquery()

    def myquery(self, *args):
        self.status.setStyleSheet("background-color : #FFFF89")
        self.status.showMessage('Загрузка...')
        self.status.repaint()
        instanse = conn.execute(db.select([tbl]).filter(*args)).fetchall()
        self.model.update(instanse)
        n = self.proxy.rowCount()
        if n != 0:
            self.status.setStyleSheet("background-color : #D8D8D8")
            self.status.showMessage(f'Сертификатов: {n}.')
        else:
            self.status.setStyleSheet("background-color : #FFFFFF")
            self.status.showMessage('По данному запросу не найдено.')
        self.status.repaint()

    def closeEvent(self, event):    # если приложение закрывают
        if conn:
            conn.close()    # закрываем соединение с БД перед закрытием
        self.status.setStyleSheet("background-color : #FFFF89")
        self.status.showMessage('Закрываем...')
        self.status.repaint()
        event.accept()

    
app = QApplication(sys.argv)
win = Table()
win.show()
sys.exit(app.exec())
