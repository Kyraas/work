from PyQt5 import QtWidgets, QtGui
from table import Ui_MainWindow  # импорт нашего сгенерированного файла
import sys
import parser
 
 
class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        headers = ["Имя", "Очки", "Дата регистрации", "ID"]
        model = QtGui.QStandardItemModel()
        model.setHorizontalHeaderLabels(headers)

        for row_number, row_data in enumerate(parser.data):
            tableitem = []
            model.insertRow(row_number)
            for value in row_data:
                item = QtGui.QStandardItem(str(value))
                tableitem.append(item)
            model.insertRow(row_number, tableitem)

        self.tableView.setModel(model)
 
app = QtWidgets.QApplication([])
application = mywindow()
application.show()
 
sys.exit(app.exec())