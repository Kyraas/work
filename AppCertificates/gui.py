# -*- coding: utf-8 -*-
# https://stackoverflow.com/questions/64184256/qtableview-placeholder-text-before-table-appears
# https://stackoverflow.com/questions/17604243/pyside-get-list-of-all-visible-rows-in-a-table
# https://stackoverflow.com/questions/53353450/how-to-highlight-a-words-in-qtablewidget-from-a-searchlist
# https://stackoverflow.com/questions/60353152/qtablewidget-resizerowstocontents-very-slow

import sys
from os import path
from datetime import datetime
from ctypes import windll

import sqlalchemy as db
from sqlalchemy.sql import func
from PyQt6.QtCore import (QSortFilterProxyModel, QThread, pyqtSignal,
                            QRect, QPoint, Qt, QTimer, pyqtSlot)
from PyQt6.QtGui import (QAbstractTextDocumentLayout, QTextOption,
                            QTextDocument, QPalette, QIcon, QTextCursor,
                            QTextCharFormat, QColor, QStatusTipEvent)
from PyQt6.QtWidgets import (QApplication, QMainWindow, QButtonGroup,
                            QProgressBar, QMessageBox, QFileDialog,
                            QStyledItemDelegate, QStyleOptionViewItem,
                            QStyle)

from myWindow import Ui_MainWindow
from AbstractModel import MyTableModel
from orm import Certificate as tbl, conn
from siteparser import parse, update_table, count_rows, check_database
from datecheck import get_update_date, half_year
from creatingfiles import save_excel_file, save_word_file

# Для отображения значка на панели.
myappid = "'ООО ЦБИ'. ДДАС. Бондаренко М.А."
windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = path.abspath(".")

    return path.join(base_path, relative_path)

# Поток, получающий последние даты обновления БД.
# (ФСТЭК и локального файла)
class WorkerThreadLaunch(QThread):
    get_actual_dates = pyqtSignal(str, str)
    def run(self):
        local_update = get_update_date()
        last_update = parse(True)
        if last_update == False:
            last_update = "Актуальность базы ФСТЭК: нет данных"
        self.get_actual_dates.emit(local_update, last_update)
        self.quit()


# Поток, обновляющий БД и progressbar.
class WorkerThreadUpdate(QThread):
    start_update = pyqtSignal(list)
    cancel_update = pyqtSignal()
    update_progressbar = pyqtSignal(int)
    finish_update = pyqtSignal(list)

    def run(self):
        # Получаем результат функции parse.
        data = parse()
        if data:
            self.start_update.emit(data)

            # Получаем кол-во строк, внесенных в базу.
            rows = update_table(data)
            for row in rows:
                self.update_progressbar.emit(row)
            check_database(data)
            results = conn.execute(db.select([tbl])).fetchall()
            self.finish_update.emit(results)
        else:
            self.cancel_update.emit()
        self.quit()


# Подсвечивает искомый текст, изменение цвета выделенных строк.
class HighlightDelegate(QStyledItemDelegate):
    def __init__(self, column_width, parent=None):
        super(HighlightDelegate, self).__init__(parent)
        self.column_width = column_width
        self._filters = []

    def paint(self, painter, option, index):
        painter.save()
        options = QStyleOptionViewItem(option)
        textOption = QTextOption()
        textOption.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.initStyleOption(options, index)

        # Создаем объект для каждой ячейки таблицы.
        self.doc = QTextDocument(options.text)
        self.doc.setDefaultTextOption(textOption)

        # Меняем ширину текста в каждом QTextDocument()
        for col, width in enumerate(self.column_width, start=1):
            if index.column() == col:
                self.doc.setTextWidth(width)

        self.apply_highlight()
        options.text = ""   # очищаем переменную
        style = QApplication.style() if options.widget is None \
            else options.widget.style()
        style.drawControl(QStyle.ControlElement.CE_ItemViewItem,
                            options, painter)

        # Цвет при выделении строки
        ctx = QAbstractTextDocumentLayout.PaintContext()
        if option.state & QStyle.StateFlag.State_Selected:
            ctx.palette.setColor(
                QPalette.ColorRole.Text,
                option.palette.color(
                    QPalette.ColorGroup.Active,
                    QPalette.ColorRole.HighlightedText))
        else:
            ctx.palette.setColor(
                QPalette.ColorRole.Text,
                option.palette.color(
                    QPalette.ColorGroup.Active,
                    QPalette.ColorRole.Text))

        textRect = style.subElementRect(
            QStyle.SubElement.SE_ItemViewItemText, options)

        if index.column() != 0:
            textRect.adjust(0, -4, 0, 0)

        # Корректное распределение текста по ячейкам таблицы.
        painter.translate(textRect.topLeft())
        painter.setClipRect(textRect.translated(-textRect.topLeft()))
        self.doc.documentLayout().draw(painter, ctx)
        painter.restore()

    # Подсветка искомого текста
    def apply_highlight(self):
        cursor = QTextCursor(self.doc)
        cursor.beginEditBlock()
        fmt = QTextCharFormat()
        fmt.setForeground(QColor("red"))
        fmt.setBackground(QColor("yellow"))
        for f in self.filters():
            highlightCursor = QTextCursor(self.doc)
            while not highlightCursor.isNull() and not highlightCursor.atEnd():
                highlightCursor = self.doc.find(f, highlightCursor)
                if not highlightCursor.isNull():
                    highlightCursor.mergeCharFormat(fmt)
        cursor.endEditBlock()

    # Изменение формата даты из ГГГГ-ММ-ДД в ДД.ММ.ГГГГ, не препятствуя сортировке
    def displayText(self, value, locale):
        try:
            value = datetime.strptime(value, "%Y-%m-%d").date()
            value = value.strftime("%d.%m.%Y")
        except ValueError:
            pass
        return value

    @pyqtSlot(list)
    def setFilters(self, filters):
        if self._filters == filters: return
        self._filters = filters

    def filters(self):
        return self._filters


class Table(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # Инициализация нашего дизайна
        self.setupUi(self)
        self.setWindowTitle("Таблица сертификатов")
        self.showMaximized()
        self.menu.menuAction().setStatusTip("Создание файла")
        icon_path = resource_path("icon.ico")
        self.setWindowIcon(QIcon(icon_path))
        self.status = self.statusBar()

        column_width = [
            80, 70, 110, 300, 200, 150,
            150, 210, 300, 300, 103
            ]

        # Модель
        self.model = MyTableModel()

        # Прокси модель (поиск и сортировка по возрастанию\убыванию)
        self.proxy = QSortFilterProxyModel()
        self.proxy.setSourceModel(self.model)
        self.proxy.setDynamicSortFilter(True)

        # Поиск по всей таблице (все колонки)
        self.proxy.setFilterKeyColumn(-1)
        self.proxy.setFilterCaseSensitivity(
            Qt.CaseSensitivity.CaseInsensitive)

        # Считаем строки при запуске программы
        if self.model.rowCount() == 0:
            self.status.showMessage(
                f"База данных пуста. Обновите базу данных," +
                "чтобы загрузить данные.")

            self.status.setStyleSheet(
                "background-color : #FF9090") # бледно-красный
        else:
            self.status.showMessage(
                f'Всего сертификатов: {self.model.rowCount()}.')

            self.status.setStyleSheet(
                "background-color : #D8D8D8") # серый

        # Получаем даты изменений баз данных.
        # (на сайте ФСТЭК и локальная БД)
        init_worker = WorkerThreadLaunch()
        init_worker.get_actual_dates.connect(self.set_update_date)
        init_worker.start()

        # Делегат
        self._delegate = HighlightDelegate(column_width)
        self.tableView.setItemDelegate(self._delegate)

        # Представление
        self.tableView.setModel(self.proxy)

        # Активируем возможность сортировки
        # по заголовкам в представлении.
        self.tableView.setSortingEnabled(True)

        # Приведение заголовков и первых видимых
        # строк таблицы к желаемому виду.
        self.tableView.hideColumn(0)
        for col, width in enumerate(column_width, start=1):
            self.tableView.horizontalHeader().resizeSection(
                col, width)

        # Выполнение функции с задержкой
        QTimer.singleShot(100, self.resize_visible_rows)
        
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
        self.proxy.layoutChanged.connect(self.resize_visible_rows)
        self.tableView.verticalScrollBar().valueChanged.connect(
            self.resize_visible_rows)
        self.searchBar.textChanged.connect(self.search)

    @pyqtSlot(str)
    def on_textChanged(self, text):
        self._delegate.setFilters(list(set(text.split())))
        self.tableView.viewport().update()

    # При наведении курсора на меню "Файл"
    # строка состояния становилась пустой.
    def event(self, e):
        # Событие изменения строки состояния. (в нижнем левом углу)
        if e.type() == 112:
            if e.tip() == '':
                e = QStatusTipEvent(
                    f'Всего сертификатов: {self.proxy.rowCount()}.')
        return super().event(e)

    # Изменение высоты только видимых строк
    def resize_visible_rows(self):
        viewport_rect = QRect(QPoint(0, 0),
                                self.tableView.viewport().size())

        for row in range(0, self.proxy.rowCount() + 1):
            # Выбираем любую видимую колонку. (костыль!)
            rect = self.tableView.visualRect(self.proxy.index(row, 7))
            if viewport_rect.intersects(rect):  # если видимые строки
                for _ in range(0, 20):
                    self.tableView.resizeRowToContents(row)
                    row += 1
                break

    # Отображение полученных дат в приложении
    def set_update_date(self, last_date, actual_date):
        self.last_update_date.setText(last_date)
        self.actual_date.setText(actual_date)
    
    # Инициализация и запуск класса WorkerThread
    def start_update_database(self):
        # Во время обновления базы делаем кнопку неактивной.
        self.refreshButton.setEnabled(False)
        self.status.setStyleSheet("background-color : pink")
        self.status.showMessage(
                        'Получаем данные с сайта ФСТЭК России...')
        self.status.repaint()

        self.worker = WorkerThreadUpdate()
        self.worker.start()
        self.worker.update_progressbar.connect(self.evt_update_progress)
        self.worker.finish_update.connect(self.finish_update_database)
        self.worker.start_update.connect(self.update_database)
        self.worker.cancel_update.connect(self.cancel_update_database)

    # При отсутствии соединения с сайтом ФСТЭК
    def cancel_update_database(self):
        # бледно-красный
        self.status.setStyleSheet("background-color : #FF9090")
        self.status.showMessage("Нет соединения с сайтом ФСТЭК " +
                                "России. Проверьте интернет-" +
                                "соединение или повторите " +
                                "попытку позже.") 
        self.status.repaint()
        self.refreshButton.setEnabled(True)
        self.worker.quit()

    # Начало обновления базы
    def update_database(self, data):
        # маскимальное кол-во строк
        max = count_rows(data)

        # Задаем максимум progressbar'у.
        self.progressbar = QProgressBar(maximum=max)

        # Задаём стиль
        self.progressbar.setStyleSheet(
            "max-height: 12px;\
            border: 2px solid gray;\
            border-radius: 7px;\
            text-align: center;"
            )

        # Добавляем progressbar в statusbar.
        self.statusBar().addPermanentWidget(self.progressbar)

        self.status.showMessage('Обновление базы...')
        self.status.repaint()

        # Отображаем progressbar
        self.progressbar.setHidden(False)

    # Анимация progressbar'а
    def evt_update_progress(self, value):
        self.progressbar.setValue(value)

    # Завершение процесса обновления БД
    def finish_update_database(self, results):
        self.status.showMessage('Загрузка таблицы...')
        self.status.repaint()
        self.model.update(results)

        # Сбарсываем фильтры, если были
        # использованы во время обновления.
        self.reset()
        self.searchBar.clear()
        self.refreshButton.setEnabled(True)

        # Скрываем progressbar при завершении обновления базы.
        self.progressbar.setHidden(True)
        n = self.model.rowCount()
        self.status.setStyleSheet("background-color : #ADFF94")
        self.status.showMessage("База данных успешно обновлена. " +
                                f"Всего сертификатов: {n}.")

        # Обновляем дату изменения файла базы данных.
        self.last_update_date.setText(get_update_date())
        self.worker.quit()

    # Сохранение таблицы в файл
    def fileSave(self):
        # Берём за основу Proxy-модель для экспорта
        # таблицы с учётом применённых фильтров
        model = self.proxy
        err = False
        r = ""
        table = []
        now = datetime.date(datetime.today())
        date_time = now.strftime("%d.%m.%Y")
        a = self.sender()

        # Если строк 0, то отменяем сохранение.
        if (model.rowCount() == 0): 
            QMessageBox.information(self, "Сохранение файла",
                                    "Нечего сохранять.\n" +
                                    f"Строк {model.rowCount()} шт.")
            return

        if a.text() == 'Экспортировать в Excel-файл':
            r = "(*.xlsx)"
        else:
            r = "(*.docx)"

        fileName, ok = QFileDialog.getSaveFileName(
                                self, "Сохранить файл",
                                f"./Сертификаты {model.rowCount()}" +
                                f"шт. {date_time}", f"All Files{r}")

        if not fileName:    # кнопка "отмена"
            return 

        # Цикл по строкам proxy модели
        for row in range(model.rowCount()):
            tbl_row = []

            # Цикл по колонкам, начиная с 1, а не с 0
            # (0 - колонка rowid)
            for column in range(1, model.columnCount()):

                # Считываем данные каждой ячейки таблицы,
                # если они имеются.
                tbl_row.append("{}".format(
                                model.index(row, column).data() or ""))
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
            QMessageBox.information(
                            self, "Сохранение файла",
                            f"Данные сохранены в файле: \n{fileName}")

            self.status.showMessage('Загрузка завершена.')
        else:
            self.status.showMessage('Ошибка загрузки.')

        self.status.setStyleSheet("background-color : #D8D8D8") # серый
        self.status.repaint()

    # Поиск по таблице
    def search(self, text):
        self.status.setStyleSheet("background-color : #FFFF89")
        self.status.showMessage('Поиск...')
        self.status.repaint()
        self.proxy.setFilterRegularExpression(text)
        self.on_textChanged(text)

        self.proxy.layoutChanged.emit()
        n = self.proxy.rowCount()
        if n != 0:
            # Серый цвет
            self.status.setStyleSheet("background-color : #D8D8D8")
            self.status.showMessage(f'Сертификатов: {n}.')
        else:
            self.status.setStyleSheet("background-color : #D8D8D8")
            self.status.showMessage('По данному запросу не найдено.')
        self.status.repaint()

    # Фильтры:
    # 1. Сертификат и поддержка не действительны
    def red(self):
        red_filter = (tbl.support <= func.current_date()) & \
                        (tbl.date_end <= func.current_date()) & \
                        (tbl.support != '')
        if self.radioButton_red.isChecked():
            self.myquery(red_filter)
            self.reset_checkBoxes()

    # 2. Поддержка не действительна
    def pink(self):
        pink_filter = (tbl.support <= func.current_date()) & \
                        (tbl.date_end > func.current_date()) & \
                        (tbl.support != '')
        if self.radioButton_pink.isChecked():
            self.myquery(pink_filter)
            self.reset_checkBoxes()

    # 3. Сертификат не действителен
    def yellow(self):
        yellow_filter = (tbl.date_end <= func.current_date()) & \
                        (tbl.date_end != '#Н/Д')
        if self.radioButton_yellow.isChecked():
            self.myquery(yellow_filter)
            self.reset_checkBoxes()
            
    # 4. Сертификат истечёт менее, чем через полгода
    # (почему-то пропадает последний столбец)
    def gray(self):
        gray_filter = (tbl.date_end <= half_year()) & \
                        (tbl.date_end > func.current_date())
        if self.radioButton_gray.isChecked():
            self.myquery(gray_filter)
            self.reset_checkBoxes()

    # 5. Сертификат и поддержка действительны
    def white(self):
        white_filter = (tbl.support > func.current_date()) & \
                        (tbl.date_end > func.current_date())
        if self.radioButton_white.isChecked():
            self.checkBox_date.setEnabled(True)
            self.checkBox_sup.setEnabled(True)
            if self.checkBox_date.isChecked():
                white_filter = white_filter + (tbl.date_end == '#Н/Д')
            if self.checkBox_sup.isChecked():
                white_filter = white_filter + (
                                (tbl.date_end > func.current_date()) & \
                                (tbl.support == ''))
            self.myquery(white_filter)

    # Сброс флагов
    def reset_checkBoxes(self):
        # Если хотя бы один флаг включён
        if self.checkBox_date.isEnabled:
            if self.checkBox_date.isChecked:
                # Убираем флаги, если они стоят
                self.checkBox_date.setChecked(False)
            if self.checkBox_sup.isChecked:
                self.checkBox_sup.setChecked(False)
            self.checkBox_date.setEnabled(False)
            self.checkBox_sup.setEnabled(False)

    # Сброс фильтров
    def reset(self):
        self.reset_checkBoxes()

        # Делаем переключатели уникальными
        # и отдельно выключаем каждый.
        self.filters.setExclusive(False)
        self.radioButton_red.setChecked(False)
        self.radioButton_pink.setChecked(False)
        self.radioButton_yellow.setChecked(False)
        self.radioButton_gray.setChecked(False)
        self.radioButton_white.setChecked(False)
        self.filters.setExclusive(True)
        self.proxy.sort(-1)
        self.myquery()

    # SQL-запрос к SQLite базе данных
    def myquery(self, *args):
        self.status.setStyleSheet("background-color : #FFFF89")
        self.status.showMessage('Загрузка...')
        self.status.repaint()
        instanse = conn.execute(
            db.select([tbl]).filter(*args)).fetchall()

        self.model.update(instanse)
        n = self.proxy.rowCount()
        if n != 0:
            self.status.setStyleSheet("background-color : #D8D8D8")
            self.status.showMessage(f'Сертификатов: {n}.')
        else:
            self.status.setStyleSheet("background-color : #FFFFFF")
            self.status.showMessage('По данному запросу не найдено.')
        self.status.repaint()

    # Событие закрытия приложения
    def closeEvent(self, event):

        # Закрываем соединение с БД перед закрытием.
        if conn:
            conn.close()
        self.status.setStyleSheet("background-color : #FFFF89")
        self.status.showMessage('Закрываем...')
        self.status.repaint()


app = QApplication(sys.argv)
win = Table()
win.show()
sys.exit(app.exec())
