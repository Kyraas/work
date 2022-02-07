# https://github.com/voidrealms/PagedModel
from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QModelIndex
from AbstractModel import MyTableModel

class MySortFilterProxyModel(QtCore.QSortFilterProxyModel):
    ROW_BATCH_COUNT = 20
    def __init__(self):
        super(MySortFilterProxyModel, self).__init__()
        self.rowsLoaded = MySortFilterProxyModel.ROW_BATCH_COUNT

    def rowCount(self, index = QModelIndex()):
        if self.sourceModel().rowCount() <= self.rowsLoaded:  # Если строк меньше ограничения (15 строк), то возвращаем кол-во строк
            return self.sourceModel().rowCount()
        else:
            return self.rowsLoaded  # если больше ограничения, то возвращаем это ограничение (15 строк)

    def canFetchMore(self, index = QModelIndex()):    # Возвращает True, если кол-во строк после запроса больше, чем кол-во загруженных строк
        if self.sourceModel().rowCount() > self.rowsLoaded:
            return True
        else:
            return False

    def fetchMore(self, index = QModelIndex()):   # Если canFetchMore вернул True
        remainder = self.sourceModel().rowCount() - self.rowsLoaded   # Вычитаем из общего кол-ва строк уже загруженные строки, получаем оставшиеся еще не прогруженные строки
        itemsToFetch = min(remainder, MyTableModel.ROW_BATCH_COUNT) # приравнивается к ограничению строк (15 строк) или к кол-ву оставшихся строк (если они меньше ограничения (remainder < 15))
        self.layoutAboutToBeChanged.emit()
        self.beginInsertRows(QModelIndex(), self.rowsLoaded, self.rowsLoaded + itemsToFetch - 1)    # начало загрузки строк
        self.rowsLoaded += itemsToFetch # к уже отображенным в таблице строкам прибавляется еще 15 или меньше строк для отображения
        self.endInsertRows()    # конец загрузки строк
        self.layoutChanged.emit()

    # def filterAcceptRow(self, row, parent):
    #     # index = self.sourceModel().data(self.index).toString()
    #     # print("Отображаем данные...")
    #     # model = self.sourceModel()
    #     # index = model.index(row, 0, parent)
    #     # name = model.data(index, Qt.ItemDataRole.DisplayRole).toString()
        # return True