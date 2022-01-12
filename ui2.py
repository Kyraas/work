import sys
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableView

class Table(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Таблица сертификатов")
        self.resize(415, 200)
        # Set up the model
        self.model = QSqlTableModel(self)
        self.model.setTable("Table")
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.setHeaderData(0, Qt.Horizontal, "№ сертификата")
        self.model.setHeaderData(1, Qt.Horizontal, "Дата внесения в реестр")
        self.model.setHeaderData(2, Qt.Horizontal, "Срок действия сертификата")
        self.model.setHeaderData(3, Qt.Horizontal, "Наименование средства (шифр)")
        self.model.setHeaderData(4, Qt.Horizontal, "Наименования документов, требованиям которых соответствует средство")
        self.model.setHeaderData(5, Qt.Horizontal, "Схема сертификации")
        self.model.setHeaderData(6, Qt.Horizontal, "Испытательная лаборатория")
        self.model.setHeaderData(7, Qt.Horizontal, "Орган по сертификации")
        self.model.setHeaderData(8, Qt.Horizontal, "Заявитель")
        self.model.setHeaderData(9, Qt.Horizontal, "Реквизиты заявителя (индекс, адрес, телефон)")
        self.model.setHeaderData(10, Qt.Horizontal, "Информация об окончании срока технической поддержки, полученная от заявителя")
        self.model.select()
        # Set up the view
        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.resizeColumnsToContents()
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
sys.exit(app.exec_())