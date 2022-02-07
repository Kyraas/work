from PyQt6 import QtCore
# from PyQt6.QtCore import Qt, QModelIndex

class Filter(QtCore.QSortFilterProxyModel):
    started = QtCore.pyqtSignal()
    finished = QtCore.pyqtSignal()
    def __init__(self):
        super(Filter, self).__init__()
        self.total_added = 0
        self.total_passed = 0
        self.total_processed = 0
        self.total_pages = 0
        self.regxpattern = ""
        self.pagedata = True
        self.pagesize = 100


    def pageData(self):
        return self.pagedata

    def setPageData(self, value):
        self.pagedata = value

    def pageSize(self):
        return self.pagesize

    def setPageSize(self, value):
        self.pagesize = value

    def pageCount(self):
        if not self.pagedata:
            return -1
        return self.total_pages

    # def filterPaged(self, pattern = ""):
    #     print("pattern: ", pattern)
    #     self.regxpattern = pattern
    #     print("regxpattern: ",self.regxpattern)
    #     self.search()

    def currentPage(self):
        return self.currentpage

    def setCurrentPage(self, value = 0):
        self.currentpage = value
        self.search()

    def back(self):
        self.currentpage -= 1
        if self.currentpage < 0:
            self.currentpage = 0
        self.search()

    def next(self):
        self.currentpage += 1
        if self.currentpage > self.total_pages:
            self.currentpage = self.total_pages
        self.search()

    def search(self):
        self.total_added = 0
        self.total_passed = 0
        self.total_processed = 0
        self.total_pages = 0
        self.min = self.currentpage * self.pagesize
        self.max = self.min + self.pagesize
        # self.layoutAboutToBeChanged.emit()
        # self.emit(self.started)
        self.started.emit()
        # self.setFilterRegularExpression(self.regxpattern)

    def process(self, allowed, countonly, reason):
        self.total_processed += 1
        if allowed == True and countonly == False:
            self.total_added += 1
        if countonly:
            self.total_passed += 1
            # знак деления, возможно подключение библиотеки math
            self.total_pages = self.total_passed / self.pagesize

        print("Allowed: ", allowed, reason)

        # посмотрим, закончили ли мы
        print(self.total_processed, "of", self.sourceModel().rowCount())
        
        if self.total_processed >= self.sourceModel().rowCount():
            # self.layoutChanged.emit()
            self.finished.emit()

        return allowed

    def filterAcceptRow(self, source_row, source_parent):
        # Получаем индекс элемента
        # index = self.sourceModel().data(self.index).toString().contains(self.filterRegularExpression())
        index = self.sourceModel().data(self.index).toString()

        # print("Count: ", self.rowCount(), "Added: ", self.total_added, "Processed: ", self.total_processed, "Data: ", self.sourceModel().data(index).toString())

        # Убедитесь, что он соответствует нашему фильтру
        # if not self.sourceModel().data(index).toString().contains(self.filterRegularExpression()):
        if not self.sourceModel().data(index).toString():
            return self.process(False, False, "Failed filter")

        # Разрешаем всё, если нет подкачки данных
        if not self.pagedata:
            return self.process(True, True, "Not paging")

        # Тут начинается процесс подкачки данных

        # Запрещаем лишние строки, выходящие за рамки
        if self.total_added >= self.pagesize:
            return self.process(False, True, "Not in page range")

        # Если мы здесь, значит, он прошел фильтр, и мы все еще можем добавить его на страницу

        # Убедимся, что она находится на текущей странице
        if self.total_passed >= self.min and self.total_passed < self.max:
            return self.process(True, True, "In page range")

        return self.process(False, True, "Default")