from operator import contains
from PyQt6 import QtCore

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


    def pageData(self): # не вызывается (?)
        print("1) pagedata: ", self.pagedata)
        return self.pagedata

    def setPageData(self, value):
        print("2) значение: ", value)
        self.pagedata = value
        print("2) pagedata: ", self.pagedata)

    def pageSize(self):
        print("3) pagesize: ", self.pagesize)
        return self.pagesize

    def setPageSize(self, value):
        print("4) value: ", value)
        self.pagesize = value
        print("4) pagesize: ", self.pagesize)

    def pageCount(self):
        print("5) pagedata: ", self.pagedata)
        print("5) total_pages: ", self.total_pages)
        if not self.pagedata:
            return -1
        return self.total_pages

    def filterPaged(self, pattern = ""):
        self.regxpattern = pattern
        self.search()

    def currentPage(self):
        print("6) currentpage: ", self.currentpage)
        return self.currentpage

    def setCurrentPage(self, value = 0):
        print("7) value: ", value)
        self.currentpage = value
        print("7) currentpage: ", self.currentpage)
        self.search()

    def back(self):
        print("назад")
        self.currentpage -= 1
        if self.currentpage < 0:
            self.currentpage = 0
        self.search()

    def next(self):
        print("вперёд")
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
        self.started.emit()
        self.setFilterRegularExpression(self.regxpattern)

    def process(self, allowed, countonly, reason):  # Не вызывается (?)
        print("process")
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
            self.finished.emit()

        return allowed

    def filterAcceptRow(self, source_row, source_parent):   # не вызывается (!)
        print("filterAcceptRow")
        # Получаем индекс элемента
        # index = self.sourceModel().data(self.index).toString().contains(self.filterRegularExpression())
        index = self.sourceModel().data(self.index)
        print(index)
        # index = QtCore.Qt.strtoString(index)
        index = contains(self.filterRegularExpression())
        print(index)

        # print("Count: ", self.rowCount(), "Added: ", self.total_added, "Processed: ", self.total_processed, "Data: ", self.sourceModel().data(index).toString())

        # Убедитесь, что он соответствует нашему фильтру
        if not self.sourceModel().data(index).toString().contains(self.filterRegularExpression()):
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