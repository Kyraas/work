# -*- coding: utf-8 -*-
# https://stackoverflow.com/questions/17697352/pyqt-implement-a-qabstracttablemodel-for-display-in-qtableview
# https://www.pythonguis.com/tutorials/qtableview-modelviews-numpy-pandas/
# https://doc.qt.io/qtforpython-5/overviews/model-view-programming.html?highlight=layoutabouttobechanged
import operator
from datetime import *
from PyQt6.QtCore import QAbstractTableModel, Qt, QVariant, QModelIndex
from PyQt6 import QtGui
import sqlalchemy as db
from orm import Certificate, conn
from six_months import half_year

headers = ['№','№\nсертификата', 'Дата\nвнесения\nв реестр', 'Срок\nдействия\nсертификата', 'Наименование\nсредства (шифр)', 'Наименования документов,\nтребованиям которых\nсоответствует средство', 'Схема\nсертификации', 'Испытательная\nлаборатория', 'Орган по\nсертификации', 'Заявитель', 'Реквизиты заявителя\n(индекс, адрес, телефон)', 'Информация об\nокончании срока\nтехнической\nподдержки,\nполученная\nот заявителя']

# QAbstractTableModel - это абстрактный базовый класс, означающий, что он не имеет реализаций для методов. Его нельзя использовать напрямую. На его основе необходимо создавать подкласс.

# self.tableView.resizeRowsToContents()

class MyTableModel(QAbstractTableModel):    # создание модели данных на базе QAbstractTableModel
    ROW_BATCH_COUNT = 15    # ограничение первоначального отображения и размер пакета для последующих обновлений представления

    def __init__(self):
        super(MyTableModel, self).__init__()
        results = conn.execute(db.select([Certificate])).fetchall()
        self.datatable = results
        self.rowsLoaded = MyTableModel.ROW_BATCH_COUNT  # инициализируется с помощью ROW_BATCH_COUNT и увеличивается, когда действия пользователя влекут за собой отображение большего количества строк в таблице.
        
    def update(self, dataIn):
        self.datatable = dataIn
        self.layoutChanged.emit()

    def row(self, index = QModelIndex()):
        return len(self.datatable)

    def rowCount(self, index = QModelIndex()):
        if len(self.datatable) <= self.rowsLoaded:  # Если строк меньше ограничения (15 строк), то возвращаем кол-во строк
            return len(self.datatable)
        else:
            return self.rowsLoaded  # если больше ограничения, то возвращаем это ограничение (15 строк)

    def canFetchMore(self, index = QModelIndex()):    # Возвращает True, если кол-во строк после запроса больше, чем кол-во загруженных строк
        if len(self.datatable) > self.rowsLoaded:
            return True
        else:
            return False

    def fetchMore(self, index = QModelIndex()):   # Если canFetchMore вернул True
        remainder = len(self.datatable) - self.rowsLoaded   # Вычитаем из общего кол-ва строк уже загруженные строки, получаем оставшиеся еще не прогруженные строки
        itemsToFetch = min(remainder, MyTableModel.ROW_BATCH_COUNT) # приравнивается к ограничению строк (15 строк) или к кол-ву оставшихся строк (если они меньше ограничения (remainder < 15))
        self.beginInsertRows(QModelIndex(), self.rowsLoaded, self.rowsLoaded + itemsToFetch - 1)    # начало загрузки строк
        self.rowsLoaded += itemsToFetch # к уже отображенным в таблице строкам прибавляется еще 15 или меньше строк для отображения
        self.endInsertRows()    # конец загрузки строк

    def columnCount(self, index = QModelIndex()):  # Принимает первый вложенный список и возвращает длину (только если все строки имеют одинаковую длину)
        if len(self.datatable):
            return len(self.datatable[0])
        else:
            return 11

    def data(self, index, role):    # Параметр role описывает, какого рода информацию метод должен возвращать при этом вызове.
        now_date = datetime.date(datetime.today())
        if not index.isValid():
            return None
        if role == Qt.ItemDataRole.BackgroundRole:
            date_end = self.datatable[index.row()][3]  # колонка с датами окончания сертификата
            sup = self.datatable[index.row()][11]   # колонка с датами окончания поддержки

            if len(sup) == 10: 
                if (datetime.date(datetime.strptime(sup, "%Y-%m-%d")) < now_date) and (datetime.date(datetime.strptime(date_end, "%Y-%m-%d")) < now_date):    # Если и сертификат, и подержка не действительны
                    return QtGui.QColor('#ff7f7f')  # красный
                if datetime.date(datetime.strptime(sup, "%Y-%m-%d")) < now_date:    # Если поддержка не действительна
                    return QtGui.QColor('#ff9fc3')  # розовый

            if len(date_end) == 10:
                if datetime.date(datetime.strptime(date_end, "%Y-%m-%d")) < now_date:    # Если сертификат не действителен
                    return QtGui.QColor('#ffecb7')  # желтый
                elif datetime.date(datetime.strptime(date_end, "%Y-%m-%d")) < half_year(): # Если сертификат истечет через полгода
                    return QtGui.QColor('#e8eaed')  # светло-серый

        if role == Qt.ItemDataRole.DisplayRole: # DisplayRole фактически принимает только строковые значения. В иных случаях необходимо форматировать данные в строку
            value = self.datatable[index.row()][index.column()]
            if isinstance(value, date):
                return value.strftime("%Y-%m-%d")
            if isinstance(value, str):
                return value
        else:
            return QVariant()

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole or orientation != Qt.Orientation.Horizontal:
            return QVariant()
        return headers[section]

    def sort(self, col, order):
        self.layoutAboutToBeChanged.emit()
        self.datatable = sorted(self.datatable, key=operator.itemgetter(col), reverse=(order != Qt.SortOrder.AscendingOrder))
        self.layoutChanged.emit()

    # def filter(self, filter, index, role = Qt.ItemDataRole.DisplayRole):
    #     now_date = datetime.date(datetime.today())
    #     value = self.datatable[index.row()][index.column()]
    #     date_end = self.datatable[index.row()][3]  # колонка с датами окончания сертификата
    #     sup = self.datatable[index.row()][11]   # колонка с датами окончания поддержки

    #     if role == Qt.ItemDataRole.DisplayRole:
    #         if len(sup) == 10: 
    #             if filter == 1:
    #                 if (datetime.date(datetime.strptime(sup, "%Y-%m-%d")) < now_date) and (datetime.date(datetime.strptime(date_end, "%Y-%m-%d")) < now_date):    # Если и сертификат, и подержка не действительны
    #                     return value  # красный
    #             if filter == 2:
    #                 if datetime.date(datetime.strptime(sup, "%Y-%m-%d")) < now_date:    # Если поддержка не действительна
    #                     return value  # розовый
    #         if len(date_end) == 10:
    #             if filter == 3:
    #                 if datetime.date(datetime.strptime(date_end, "%Y-%m-%d")) < now_date:    # Если сертификат не действителен
    #                     return value  # желтый
    #             if filter == 4:
    #                 if datetime.date(datetime.strptime(date_end, "%Y-%m-%d")) < half_year(): # Если сертификат истечет через полгода
    #                     return value  # светло-серый
    #     else:
    #         return QVariant()
