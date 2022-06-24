# -*- coding: utf-8 -*-
# https://stackoverflow.com/questions/17697352/pyqt-implement-a-qabstracttablemodel-for-display-in-qtableview
# https://www.pythonguis.com/tutorials/qtableview-modelviews-numpy-pandas/
# https://doc.qt.io/qtforpython-5/overviews/model-view-programming.html?highlight=layoutabouttobechanged

# QAbstractTableModel - это абстрактный базовый класс,
# означающий, что он не имеет реализаций для методов.
# Его нельзя использовать напрямую.
# На его основе необходимо создавать подкласс.

from datetime import datetime, date

import sqlalchemy as db
from PyQt6.QtGui import QColor
from PyQt6.QtCore import (QAbstractTableModel, Qt,
                            QVariant, QModelIndex)

from orm import Certificate, conn
from datecheck import half_year

headers = [
    '№', '№\nсертификата', 'Дата\nвнесения\nв реестр',
    'Срок\nдействия\nсертификата', 'Наименование\nсредства (шифр)',
    'Наименования документов,\nтребованиям' + \
    'которых\nсоответствует средство',
    'Схема\nсертификации', 'Испытательная\nлаборатория',
    'Орган по\nсертификации', 'Заявитель',
    'Реквизиты заявителя\n(индекс, адрес, телефон)',
    'Информация об\nокончании срока\nтехнической\n' + \
    'поддержки,\nполученная\nот заявителя'
    ]


def convert_date(data):
    return datetime.date(datetime.strptime(data, "%Y-%m-%d"))


# Cоздание модели данных на базе QAbstractTableModel.
class MyTableModel(QAbstractTableModel):

    def __init__(self):
        super(MyTableModel, self).__init__()
        results = conn.execute(db.select([Certificate])).fetchall()
        self.datatable = results
        
    def update(self, dataIn):
        self.layoutAboutToBeChanged.emit()
        self.datatable = dataIn
        self.layoutChanged.emit()

    def rowCount(self, index = QModelIndex()):
        return len(self.datatable)

    # Принимает первый вложенный список и возвращает длину.
    # (только если все строки имеют одинаковую длину)
    def columnCount(self, index = QModelIndex()):
        if len(self.datatable):
            return len(self.datatable[0])
        else:
            return 11

    # Параметр role описывает, какого рода информацию
    # метод должен возвращать при этом вызове.
    def data(self, index, role):
        now_date = datetime.date(datetime.today())
        if not index.isValid():
            return None
        if role == Qt.ItemDataRole.BackgroundRole:
            
            # Колонка с датами окончания сертификата
            date_end = self.datatable[index.row()][3]

            # Колонка с датами окончания поддержки
            sup = self.datatable[index.row()][11]

            # Если и сертификат, и подержка не действительны
            try:
                if (convert_date(sup) < now_date) and \
                    (convert_date(date_end) < now_date):
                    return QColor('#ff7f7f')  # красный
            except ValueError:
                pass

            # Если поддержка не действительна
            try:
                if convert_date(sup) < now_date:
                    return QColor('#ff9fc3')  # розовый
            except ValueError:
                pass

            # Если сертификат не действителен
            try:
                if convert_date(date_end) < now_date:
                    return QColor('#ffecb7')  # желтый

                # Если сертификат истечет через полгода
                elif convert_date(date_end) < half_year():
                    return QColor('#e8eaed')  # светло-серый
            except ValueError:
                pass

        # DisplayRole фактически принимает только строковые значения.
        # В иных случаях необходимо форматировать данные в строку.
        if role == Qt.ItemDataRole.DisplayRole:
            value = self.datatable[index.row()][index.column()]
            if isinstance(value, date):
                return value.strftime("%Y-%m-%d")
            if isinstance(value, str):
                return value
        else:
            return QVariant()

    def headerData(self, section, orientation,
                    role=Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole or \
            orientation != Qt.Orientation.Horizontal:
            return QVariant()
        return headers[section]
