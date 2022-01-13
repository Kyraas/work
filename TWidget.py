# В данном проекте создается TableWidget с последующим выводом данных из базы данных

import sys

from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidget, QTableWidgetItem
# from table import Ui_MainWindow

class Table(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Таблица сертификатов")
        self.resize(1250, 650)
        # Настройка представления и загрузка данных
        self.view = QTableWidget()
        self.view.setColumnCount(11)    # Создаем заголовки таблицы
        self.view.setHorizontalHeaderLabels(["№ сертификата", "Дата внесения в реестр", "Срок действия сертификата", "Наименование средства (шифр)", "Наименования документов, требованиям которых соответствует средство", "Схема сертификации", "Испытательная лаборатория", "Орган по сертификации", "Заявитель", "Реквизиты заявителя (индекс, адрес, телефон)", "Информация об окончании срока технической поддержки, полученная от заявителя"])

        query = QSqlQuery("SELECT * FROM 'Сертификаты'")    # SQL-запрос
        while query.next(): # запускает while цикл для навигации по записям в результате запроса с помощью .next()
            rows = self.view.rowCount() # позволяет получить кол-во строк в таблице
            self.view.setRowCount(rows + 1) # увеличивает количество строк в таблице с помощью .setRowCount()
            self.view.setItem(rows, 0, QTableWidgetItem(query.value(0)))
            self.view.setItem(rows, 1, QTableWidgetItem(query.value(1)))
            self.view.setItem(rows, 2, QTableWidgetItem(query.value(2)))
            self.view.setItem(rows, 3, QTableWidgetItem(query.value(3)))
            self.view.setItem(rows, 4, QTableWidgetItem(query.value(4)))
            self.view.setItem(rows, 5, QTableWidgetItem(query.value(5)))
            self.view.setItem(rows, 6, QTableWidgetItem(query.value(6)))
            self.view.setItem(rows, 7, QTableWidgetItem(query.value(7)))
            self.view.setItem(rows, 8, QTableWidgetItem(query.value(8)))
            self.view.setItem(rows, 9, QTableWidgetItem(query.value(9)))
            self.view.setItem(rows, 10, QTableWidgetItem(query.value(10)))
        # self.view.resizeColumnsToContents() # Подстраивает размер колонок под длину данных
        self.setCentralWidget(self.view)

        
def createConnection():
    con = QSqlDatabase.addDatabase("QSQLITE")
    con.setDatabaseName("parseddata.db")
    if not con.open():
        QMessageBox.critical(
            None,
            "Таблица сертификатов - Ошибка!",
            "Ошибка базы данных: %s" % con.lastError().databaseText(),
        )
        return False
    return True


app = QApplication(sys.argv)
if not createConnection():
    sys.exit(1)
win = Table()
win.show()
sys.exit(app.exec())