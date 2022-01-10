from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(543, 303)

        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(20, 270, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.loadData)

        self.tableView = QtWidgets.QTableView(Dialog)
        self.tableView.setGeometry(QtCore.QRect(10, 10, 521, 251))
        self.tableView.setSortingEnabled(True)
        self.tableView.setObjectName("tableView")

        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(340, 270, 191, 20))
        self.lineEdit.setObjectName("lineEdit")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Загрузить"))
        self.lineEdit.setPlaceholderText(_translate("Dialog", "Поиск по имени или ID"))

    def loadData(self):
        headers = ["Имя", "Очки", "Дата регистрации", "ID"]
        model = QtGui.QStandardItemModel()
        model.setHorizontalHeaderLabels(headers)

        items = [
            ('Oleg', 22.98, 1587900157, 188530139),
            ('Max', 223.05, 1587900543, 17578),
            ('Vladimir324235576576294592', -99.12, 1587900003, 1),
            ('Anton', -11.32, 1587900322, 5675677),
            ('Глеб', 17.21, 1587900932, 2277786),
            ('Nataliya', 989.16, 1587900113, 7887678),
            ('Виталий', -233.04, 1587900199, 124214)
        ]


        for row_number, row_data in enumerate(items):
            tableitem = []
            model.insertRow(row_number)
            for value in row_data:
                item = QtGui.QStandardItem(str(value))
                tableitem.append(item)
            model.insertRow(row_number, tableitem)

        self.tableView.setModel(model)




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())