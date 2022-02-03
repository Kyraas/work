# -*- coding: utf-8 -*-
from datetime import *
from PyQt6.QtCore import QAbstractTableModel, Qt, QVariant, QModelIndex
from PyQt6 import QtGui
import sqlalchemy as db
from orm import Certificate, conn
from six_months import half_year

headers = ['№','№\nсертификата', 'Дата\nвнесения\nв реестр', 'Срок\nдействия\nсертификата', 'Наименование\nсредства (шифр)', 'Наименования документов,\nтребованиям которых\nсоответствует средство', 'Схема\nсертификации', 'Испытательная\nлаборатория', 'Орган по\nсертификации', 'Заявитель', 'Реквизиты заявителя\n(индекс, адрес, телефон)', 'Информация об\nокончании срока\nтехнической\nподдержки,\nполученная\nот заявителя']

class TestTableModel(QAbstractTableModel):  
    def __init__(self, parent = None):
        QAbstractTableModel.__init__(self, parent)
        results = conn.execute(db.select([Certificate])).fetchall()
        self.datatable = results
        
    def rowCount(self, index = QModelIndex()):
        return len(self.datatable)

    def columnCount(self, index = QModelIndex()):
        if len(self.datatable):
            return len(self.datatable[0])
        else:
            return 11

    def data(self, index, role):    
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
