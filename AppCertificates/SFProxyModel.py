from PyQt6.QtCore import QSortFilterProxyModel, QModelIndex, pyqtSignal

class MyProxyModel(QSortFilterProxyModel):
    ROW_BATCH_COUNT = 20    # ограничение первоначального отображения и размер пакета для последующих обновлений представления
    resize_rows = pyqtSignal(int)

    def __init__(self, parent=None):
        super(MyProxyModel, self).__init__(parent)
        self.rowsLoaded = MyProxyModel.ROW_BATCH_COUNT  # инициализируется с помощью ROW_BATCH_COUNT и увеличивается, когда действия пользователя влекут за собой отображение большего количества строк в таблице.
        self.rows = 0


    def rowCount(self, index = QModelIndex()):
        if self.sourceModel().rowCount() <= self.rowsLoaded:  # Если строк меньше ограничения (15 строк), то возвращаем кол-во строк
            self.rows = self.sourceModel().rowCount()
        else:
            self.rows = self.rowsLoaded  # если больше ограничения, то возвращаем это ограничение (15 строк)
        return self.sourceModel().rowCount()

    def canFetchMore(self, index = QModelIndex()):    # Возвращает True, если кол-во строк после запроса больше, чем кол-во загруженных строк
        if self.sourceModel().rowCount() < self.rowsLoaded:
            print("True")
            return True
        else:
            print("False")
            return False

    def fetchMore(self, index = QModelIndex()):   # Если canFetchMore вернул True

        remainder = self.sourceModel().rowCount() - self.rowsLoaded   # Вычитаем из общего кол-ва строк уже загруженные строки, получаем оставшиеся еще не прогруженные строки
        print(remainder)
        # self.resize_rows.emit(remainder)
        itemsToFetch = min(remainder, MyProxyModel.ROW_BATCH_COUNT) # приравнивается к ограничению строк (15 строк) или к кол-ву оставшихся строк (если они меньше ограничения (remainder < 15))
        print(itemsToFetch)
        self.rowsLoaded += itemsToFetch # к уже отображенным в таблице строкам прибавляется еще 15 или меньше строк для отображения
        print(self.rowsLoaded)
        # self.resize_rows.emit(self.rowsLoaded)

    # def sort(self, col, order):
    #     model = self.sourceModel()
    #     self.layoutAboutToBeChanged.emit()
    #     model = sorted(model, key=operator.itemgetter(col), reverse=(order != Qt.SortOrder.AscendingOrder))
    #     self.layoutChanged.emit()

    # def filterAcceptsRow(self, row_num, parent):
    #     """
    #     Reimplemented from base class to allow the use
    #     of custom filtering.
    #     """
    #     model = self.sourceModel()
    #     # The source model should have a method called row()
    #     # which returns the table row as a python list.
    #     tests = [func(model.row(row_num), self.filterString)
    #              for func in self.filterFunctions.values()]
    #     return not False in tests
    