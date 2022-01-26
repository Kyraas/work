# -*- coding: utf-8 -*-
# https://stackoverflow.com/questions/17697352/pyqt-implement-a-qabstracttablemodel-for-display-in-qtableview
# https://www.pythonguis.com/tutorials/qtableview-modelviews-numpy-pandas/
from datetime import date, datetime
from PyQt6.QtCore import QAbstractTableModel, Qt, QVariant
import sqlalchemy as db
from orm import Certificate, conn

headers = ['№\nсертификата', 'Дата\nвнесения\nв реестр', 'Срок\nдействия\nсертификата', 'Наименование\nсредства (шифр)', 'Наименования документов,\nтребованиям которых\nсоответствует средство', 'Схема\nсертификации', 'Испытательная\nлаборатория', 'Орган по\nсертификации', 'Заявитель', 'Реквизиты заявителя\n(индекс, адрес, телефон)', 'Информация об\nокончании срока\nтехнической\nподдержки,\nполученная\nот заявителя']

# QAbstractTableModel - это абстрактный базовый класс, означающий, что он не имеет реализаций для методов. Его нельзя использовать напрямую. На его основе необходимо создавать подкласс.

class MyTableModel(QAbstractTableModel):    # создание модели данных на базе QAbstractTableModel
    def __init__(self):
        super(MyTableModel, self).__init__()
        results = conn.execute(db.select([Certificate])).fetchall()
        self.datatable = results
        
    def update(self, dataIn):
        self.datatable = dataIn
        self.layoutChanged.emit()

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):    # Параметр role описывает, какого рода информацию метод должен возвращать при этом вызове.
        if not index.isValid():
            return None
        if role == Qt.ItemDataRole.DisplayRole: # DisplayRole фактически принимает только строковые значения. В иных случаях необходимо форматировать данные в строку
            value = self.datatable[index.row()][index.column()]
            if isinstance(value, date):
                return value.strftime("%Y-%m-%d")

            if isinstance(value, str):
                return value
        else:
            return QVariant()

    def rowCount(self, index):
        return len(self.datatable)

    def columnCount(self, index):  # Принимает первый вложенный список и возвращает длину (только если все строки имеют одинаковую длину)
        return len(self.datatable[0])

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole or orientation != Qt.Orientation.Horizontal:
            return QVariant()
        return headers[section]
