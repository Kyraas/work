# -*- coding: utf-8 -*-
# https://stackoverflow.com/questions/60353152/qtablewidget-resizerowstocontents-very-slow

import sys
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QSortFilterProxyModel, QThread, pyqtSignal, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QButtonGroup, QProgressBar, QMessageBox, QFileDialog, QStyledItemDelegate
from tableview import Ui_MainWindow
from AbstractModel import MyTableModel
from orm import Certificate as tbl, conn
import sqlalchemy as db
from sqlalchemy.sql import func
from siteparser import parse, update_table, count_rows, check_database
from sixmonths import half_year
from lastupdate import get_update_date
from creatingfiles import save_excel_file, save_word_file
from datetime import datetime

class MyDelegate(QStyledItemDelegate):
    def displayText(self, value, locale):
        try:
            value = datetime.strptime(value, "%Y-%m-%d").date()
            value = value.strftime("%d.%m.%Y")  # Изменение формата даты из ГГГГ-ММ-ДД в ДД.ММ.ГГГГ, не препятствуя сортировке
        except ValueError:
            pass
        return value
    def paint(self, painter, option, index):
        option.displayAlignment = QtCore.Qt.AlignmentFlag.AlignCenter   # Выравнивание данных таблицы по центру
        QStyledItemDelegate.paint(self, painter, option, index)


class WorkerThreadLaunch(QThread):
    get_actual_dates = pyqtSignal(str, str)
    def run(self):
        local_update = get_update_date()
        last_update = parse(True)
        self.get_actual_dates.emit(local_update, last_update)


class WorkerThreadUpdate(QThread):
    start_update = pyqtSignal(list)
    cancel_update = pyqtSignal()
    update_progressbar = pyqtSignal(int)
    finish_update = pyqtSignal(list)

    def run(self):
        data = parse()  # получаем результат функции parse
        if data:
            self.start_update.emit(data)
            rows = update_table(data)   # получаем кол-во строк, внесенных в базу
            for row in rows:
                self.update_progressbar.emit(row)
            check_database(data)
            results = conn.execute(db.select([tbl])).fetchall()
            self.finish_update.emit(results)
        else:
            self.cancel_update.emit()
        

class Table(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Инициализация нашего дизайна
        self.setWindowTitle("Таблица сертификатов")
        self.menu.menuAction().setStatusTip("Создание файла")
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
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
        n = self.model.rowCount()
        self.status.showMessage(f'Всего сертификатов: {n}.')
        self.status.setStyleSheet("background-color : #D8D8D8") # серый

        # Получаем даты изменений баз данных (на сайте ФСТЭК и локальная БД)
        init_worker = WorkerThreadLaunch()
        init_worker.get_actual_dates.connect(self.set_update_date)
        init_worker.start()
        init_worker.quit()

        # Делегат
        self.dateDelegate = MyDelegate(self)
        self.tableView.setItemDelegate(self.dateDelegate)

        # Представление
        self.tableView.setModel(self.proxy)
        self.tableView.setSortingEnabled(True)  # Активируем возможность сортировки по заголовкам в представлении

        # Приведение заголовков таблицы к желаемому виду
        self.tableView.hideColumn(0)
        self.tableView.horizontalHeader().resizeSection(1, 80)
        self.tableView.horizontalHeader().resizeSection(2, 70)
        self.tableView.horizontalHeader().resizeSection(3, 100)
        self.tableView.horizontalHeader().resizeSection(4, 300)
        self.tableView.horizontalHeader().resizeSection(5, 200)
        self.tableView.horizontalHeader().resizeSection(6, 150)
        self.tableView.horizontalHeader().resizeSection(7, 150)
        self.tableView.horizontalHeader().resizeSection(8, 210)
        self.tableView.horizontalHeader().resizeSection(9, 300)
        self.tableView.horizontalHeader().resizeSection(10, 300)
        self.tableView.horizontalHeader().resizeSection(11, 103)
        # self.tableView.resizeRowsToContents()   # Высота строк подстраивается под содержимое. Замедляет запуск приложения!!!
        QTimer.singleShot(0, lambda: self.resize_row(0, n, 10))
        
        # Создаем группу фильтров
        self.filters = QButtonGroup(self)
        self.filters.addButton(self.radioButton_red)
        self.filters.addButton(self.radioButton_pink)
        self.filters.addButton(self.radioButton_yellow)
        self.filters.addButton(self.radioButton_gray)
        self.filters.addButton(self.radioButton_white)

        # Соединяем виджеты с функциями
        self.action_Excel.triggered.connect(self.fileSave)
        self.action_Word.triggered.connect(self.fileSave)
        self.refreshButton.clicked.connect(self.start_update_database)
        self.radioButton_red.clicked.connect(self.red)
        self.radioButton_pink.clicked.connect(self.pink)
        self.radioButton_yellow.clicked.connect(self.yellow)
        self.radioButton_gray.clicked.connect(self.gray)
        self.radioButton_white.clicked.connect(self.white)
        self.checkBox_date.stateChanged.connect(self.white)
        self.checkBox_sup.stateChanged.connect(self.white)
        self.resetButton.clicked.connect(self.reset)
        self.searchButton.clicked.connect(self.search)
        self.searchBar.returnPressed.connect(self.search)
        # self.proxy.layoutChanged.connect(self.tableView.resizeRowsToContents)   # при изменении отображения вызываем функцию resizeRowsToContents
        self.proxy.layoutChanged.connect(lambda: self.resize_row(0, n, 10))

    # Замена функции resizeRowsToContents()
    def resize_row(self, row, n, count=1):
        todo = count
        while (row < n) and (todo >= 0):
            self.tableView.resizeRowToContents(row)    
            row += 1
            todo -= 1

        if row < n:
            QTimer.singleShot(0, lambda: self.resize_row(row, n, count))

    # Отображение полученных дат в приложении
    def set_update_date(self, last_date, actual_date):
        self.last_update_date.setText(last_date)
        self.actual_date.setText(actual_date)
    
    # Инициализация и запуск класса WorkerThread
    def start_update_database(self):  # Обновление БД
        self.refreshButton.setEnabled(False)    # во время обновления базы делаем кнопку неактивной
        self.status.setStyleSheet("background-color : pink")
        self.status.showMessage('Получаем данные с сайта ФСТЭК России...')
        self.status.repaint()

        self.worker = WorkerThreadUpdate()
        self.worker.start()
        self.worker.update_progressbar.connect(self.evt_update_progress)
        self.worker.finish_update.connect(self.finish_update_database)
        self.worker.start_update.connect(self.update_database)
        self.worker.cancel_update.connect(self.cancel_update_database)

    # При отсутствии соединения с сайтом ФСТЭК
    def cancel_update_database(self):
        self.status.setStyleSheet("background-color : #FF9090") # бледно-красный
        self.status.showMessage('Нет соединения с сайтом ФСТЭК России.') 
        self.status.repaint()
        self.refreshButton.setEnabled(True)
        self.worker.quit()

    # Начало обновления базы
    def update_database(self, data):
        max = count_rows(data)  # маскимальное кол-во строк
        self.progressbar = QProgressBar(maximum=max)    # задаем максимум progressbar'у
        self.progressbar.setStyleSheet("max-height: 12px; border: 2px solid gray; border-radius: 7px; text-align: center; ")  # задаем стиль
        self.statusBar().addPermanentWidget(self.progressbar)   # добавляем progressbar в statusbar

        self.status.showMessage('Обновление базы...')
        self.status.repaint()
        self.progressbar.setHidden(False)   # отображаем progressbar

    # Анимация progressbar'а
    def evt_update_progress(self, value):
        self.progressbar.setValue(value)

    # Завершение процесса обновления БД
    def finish_update_database(self, results):
        self.status.showMessage('Загрузка таблицы...')
        self.status.repaint()
        self.model.update(results)
        self.reset()    # сбарсываем фильтры, если были использованы во время обновления
        self.refreshButton.setEnabled(True)
        self.progressbar.setHidden(True)    # скрываем progressbar при завершении обновления базы
        n = self.model.rowCount()
        self.status.setStyleSheet("background-color : #ADFF94") # салатовый FF9090
        self.status.showMessage(f'База данных успешно обновлена. Всего сертификатов: {n}.')
        self.last_update_date.setText(get_update_date())    # обновляем дату изменения файла базы данных
        self.worker.quit()

    # При наведении курсора на меню "Файл" строка состояния становилась пустой
    def event(self, e):
        if e.type() == 112: # событие изменения строки состояния (в нижнем левом углу)
            if e.tip() == '':
                e = QtGui.QStatusTipEvent(f'Всего сертификатов: {self.proxy.rowCount()}.')
        return super().event(e)

    # Методы класса
    def fileSave(self):
        err = False
        r = ""
        model = self.proxy  # берём за основу Proxy-модель для экспорта таблицы с учётом применённых фильтров
        if (model.rowCount() == 0): # если строк 0, то отменяем сохранение
            QMessageBox.information(self, "Сохранение файла", f"Нечего сохранять.\nСтрок {model.rowCount()} шт.")
            return
        now = datetime.date(datetime.today())
        date_time = now.strftime("%d.%m.%Y")
        a = self.sender()
        if a.text() == 'Экспортировать в Excel-файл':
            r = "(*.xlsx)"
        else:
            r = "(*.docx)"

        fileName, ok = QFileDialog.getSaveFileName(self, "Сохранить файл", f"./Сертификаты {model.rowCount()} шт. {date_time}", f"All Files{r}")
        if not fileName:    # кнопка "отмена"
            return 

        table = []
        for row in range(model.rowCount()): # цикл по строкам proxy модели
            tbl_row = []
            for column in range(1, model.columnCount()):    # цикл по колонкам, начиная с 1, а не с 0 (0 - колонка rowid)
                tbl_row.append("{}".format(model.index(row, column).data() or ""))  # считываем данные каждой ячейки таблицы, если они имеются
            table.append(tbl_row)

        self.status.setStyleSheet("background-color : #FFFF89")
        if r == "(*.xlsx)":
            self.status.showMessage('Загрузка таблицы в Excel-файл...')
            self.status.repaint()
            err = save_excel_file(self, fileName, table)
        else:
            self.status.showMessage('Загрузка таблицы в Word-файл...')
            self.status.repaint()
            err = save_word_file(self, fileName, table)
        
        if not err:
            QMessageBox.information(self, "Сохранение файла", f"Данные сохранены в файле: \n{fileName}")
            self.status.showMessage('Загрузка завершена.')
        else:
            self.status.showMessage('Ошибка загрузки.')

        self.status.setStyleSheet("background-color : #D8D8D8") # серый
        self.status.repaint()

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

app = QApplication(sys.argv)
win = Table()
win.show()
sys.exit(app.exec())
