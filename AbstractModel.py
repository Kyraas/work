# -*- coding: utf-8 -*-
from PyQt6.QtCore import QAbstractTableModel, Qt, QVariant
from orm import Certificate
import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

headers = ['№\nсертификата', 'Дата\nвнесения\nв реестр', 'Срок\nдействия\nсертификата', 'Наименование\nсредства (шифр)', 'Наименования документов,\nтребованиям которых\nсоответствует средство', 'Схема\nсертификации', 'Испытательная\nлаборатория', 'Орган по\nсертификации', 'Заявитель', 'Реквизиты заявителя\n(индекс, адрес, телефон)', 'Информация об\nокончании срока\nтехнической\nподдержки,\nполученная\nот заявителя']

engine = create_engine('sqlite:///parseddata_eng.db')
conn = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()

class MyTableModel(QAbstractTableModel):    # создание модели данных на базе QAbstractTableModel
    def __init__(self, parent):
        super().__init__(parent)
        results = conn.execute(db.select([Certificate])).fetchall()
        self.mylist = results

    def rowCount(self, parent=None):
        return len(self.mylist)

    def columnCount(self, parent=None):
        return len(self.mylist[0])

    def data(self, index, role):
        if not index.isValid():
            return None
        if (role == Qt.ItemDataRole.DisplayRole):
            return self.mylist[index.row()][index.column()]
        else:
            return QVariant()

    def headerData(self, section, orientation, role):
        if role != Qt.ItemDataRole.DisplayRole or orientation != Qt.Orientation.Horizontal:
            return QVariant()
        return headers[section]

    def setData(self, index, value, role = Qt.ItemDataRole.DisplayRole):
        print("SetData", index.row(), index.column(), value)

MyTableModel.setData()