# Образец создания TableView. Заполнение данными работает. Их можно менять
# https://realpython.com/python-pyqt-database/
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableView

class Table(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Таблица сертификатов")
        self.resize(1015, 600)
        # Модель
        self.model = QSqlTableModel(self)
        self.model.setTable("Сертификаты")  # Соединение модели со существующей таблицей "Сертификаты"
        # self.model.setEditStrategy(QSqlTableModel.OnFieldChange)  # Строка 20 устанавливает стратегию редактирования модели в OnFieldChange. Эта стратегия позволяет модели автоматически обновлять данные в вашей базе данных, если пользователь изменяет какие-либо данные непосредственно в представлении.
        self.model.select() # Загрузка данных из таблицы и заполнение модели ими 
        # Представление
        self.view = QTableView()    # Создание представления для отображения данных, содержащихся в модели
        self.view.setModel(self.model)  # Соединение представление и модели
        self.view.resizeColumnsToContents() # Изменение размеров колонок под длину данных
        self.setCentralWidget(self.view)    # Расположение представления по центру


def createConnection(): # Соединение с БД
    con = QSqlDatabase.addDatabase("QSQLITE") # Создаем объект БД с указанием типа (в данном случае sqlite)
    con.setDatabaseName("parseddata.db")    # указываем название файла БД
    if not con.open():  # Если True (not False), то выводим ошибку подключения
        QMessageBox.critical(
            None,
            "Таблица сертификатов - Ошибка!",
            "Ошибка базы данных: %s" % con.lastError().databaseText(),
        )
        return False    # В ином случае выводим False, подключение успешно установлено
    return True


app = QApplication(sys.argv)
if not createConnection():
    sys.exit(1) # Закрываем приложение при ошибке подключения
win = Table()
win.show()
sys.exit(app.exec())