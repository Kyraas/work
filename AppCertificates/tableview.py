# Form implementation generated from reading ui file 'tableview.ui'
#
# Created by: PyQt6 UI code generator 6.1.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1062, 879)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setMinimumSize(QtCore.QSize(370, 190))
        self.groupBox.setObjectName("groupBox")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 358, 166))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_filters = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_filters.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_filters.setObjectName("verticalLayout_filters")
        self.formLayout_red = QtWidgets.QFormLayout()
        self.formLayout_red.setObjectName("formLayout_red")
        self.label_red = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_red.setMinimumSize(QtCore.QSize(20, 20))
        self.label_red.setMaximumSize(QtCore.QSize(20, 20))
        self.label_red.setAutoFillBackground(False)
        self.label_red.setStyleSheet("background-color: rgb(255, 127, 127);\n"
"border-style: solid;\n"
"border-width: 1px;\n"
"border-color: rgb(0, 0, 0);")
        self.label_red.setText("")
        self.label_red.setObjectName("label_red")
        self.formLayout_red.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_red)
        self.radioButton_red = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.radioButton_red.setAutoExclusive(True)
        self.radioButton_red.setObjectName("radioButton_red")
        self.formLayout_red.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.radioButton_red)
        self.verticalLayout_filters.addLayout(self.formLayout_red)
        self.formLayout_pink = QtWidgets.QFormLayout()
        self.formLayout_pink.setObjectName("formLayout_pink")
        self.label_pink = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_pink.setMinimumSize(QtCore.QSize(20, 20))
        self.label_pink.setMaximumSize(QtCore.QSize(20, 20))
        self.label_pink.setAutoFillBackground(False)
        self.label_pink.setStyleSheet("background-color: rgb(255, 159, 195);\n"
"border-style: solid;\n"
"border-width: 1px;\n"
"border-color: rgb(0, 0, 0);")
        self.label_pink.setText("")
        self.label_pink.setObjectName("label_pink")
        self.formLayout_pink.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_pink)
        self.radioButton_pink = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.radioButton_pink.setAutoExclusive(True)
        self.radioButton_pink.setObjectName("radioButton_pink")
        self.formLayout_pink.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.radioButton_pink)
        self.verticalLayout_filters.addLayout(self.formLayout_pink)
        self.formLayout_yellow = QtWidgets.QFormLayout()
        self.formLayout_yellow.setObjectName("formLayout_yellow")
        self.label_yellow = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_yellow.setMinimumSize(QtCore.QSize(20, 20))
        self.label_yellow.setMaximumSize(QtCore.QSize(20, 20))
        self.label_yellow.setAutoFillBackground(False)
        self.label_yellow.setStyleSheet("background-color: rgb(255, 236, 183);\n"
"border-style: solid;\n"
"border-width: 1px;\n"
"border-color: rgb(0, 0, 0);")
        self.label_yellow.setText("")
        self.label_yellow.setObjectName("label_yellow")
        self.formLayout_yellow.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_yellow)
        self.radioButton_yellow = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.radioButton_yellow.setAutoExclusive(True)
        self.radioButton_yellow.setObjectName("radioButton_yellow")
        self.formLayout_yellow.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.radioButton_yellow)
        self.verticalLayout_filters.addLayout(self.formLayout_yellow)
        self.formLayout_gray = QtWidgets.QFormLayout()
        self.formLayout_gray.setObjectName("formLayout_gray")
        self.label_gray = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_gray.setMinimumSize(QtCore.QSize(20, 20))
        self.label_gray.setMaximumSize(QtCore.QSize(20, 20))
        self.label_gray.setAutoFillBackground(False)
        self.label_gray.setStyleSheet("background-color: rgb(232, 234, 237);\n"
"border-style: solid;\n"
"border-width: 1px;\n"
"border-color: rgb(0, 0, 0);")
        self.label_gray.setText("")
        self.label_gray.setObjectName("label_gray")
        self.formLayout_gray.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_gray)
        self.radioButton_gray = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.radioButton_gray.setAutoExclusive(True)
        self.radioButton_gray.setObjectName("radioButton_gray")
        self.formLayout_gray.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.radioButton_gray)
        self.verticalLayout_filters.addLayout(self.formLayout_gray)
        self.formLayout_white = QtWidgets.QFormLayout()
        self.formLayout_white.setObjectName("formLayout_white")
        self.label_white = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_white.setMinimumSize(QtCore.QSize(20, 20))
        self.label_white.setMaximumSize(QtCore.QSize(20, 20))
        self.label_white.setAutoFillBackground(False)
        self.label_white.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-style: solid;\n"
"border-width: 1px;\n"
"border-color: rgb(0, 0, 0);")
        self.label_white.setText("")
        self.label_white.setObjectName("label_white")
        self.formLayout_white.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_white)
        self.radioButton_white = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.radioButton_white.setAutoExclusive(True)
        self.radioButton_white.setObjectName("radioButton_white")
        self.formLayout_white.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.radioButton_white)
        self.verticalLayout_filters.addLayout(self.formLayout_white)
        self.resetButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.resetButton.setToolTip("")
        self.resetButton.setObjectName("resetButton")
        self.verticalLayout_filters.addWidget(self.resetButton)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setMinimumSize(QtCore.QSize(55, 30))
        self.label.setLineWidth(5)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.searchBar = QtWidgets.QLineEdit(self.centralwidget)
        self.searchBar.setMinimumSize(QtCore.QSize(0, 30))
        self.searchBar.setText("")
        self.searchBar.setClearButtonEnabled(True)
        self.searchBar.setObjectName("searchBar")
        self.horizontalLayout.addWidget(self.searchBar)
        self.searchButton = QtWidgets.QPushButton(self.centralwidget)
        self.searchButton.setMinimumSize(QtCore.QSize(100, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.searchButton.setFont(font)
        self.searchButton.setObjectName("searchButton")
        self.horizontalLayout.addWidget(self.searchButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.checkBox_date = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_date.setEnabled(False)
        self.checkBox_date.setMinimumSize(QtCore.QSize(426, 15))
        self.checkBox_date.setMaximumSize(QtCore.QSize(16777215, 15))
        self.checkBox_date.setObjectName("checkBox_date")
        self.gridLayout_2.addWidget(self.checkBox_date, 0, 0, 1, 1)
        self.checkBox_sup = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_sup.setEnabled(False)
        self.checkBox_sup.setMinimumSize(QtCore.QSize(454, 15))
        self.checkBox_sup.setMaximumSize(QtCore.QSize(16777215, 15))
        self.checkBox_sup.setObjectName("checkBox_sup")
        self.gridLayout_2.addWidget(self.checkBox_sup, 1, 0, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout_2)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.refreshButton = QtWidgets.QPushButton(self.centralwidget)
        self.refreshButton.setMinimumSize(QtCore.QSize(200, 50))
        self.refreshButton.setMaximumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.refreshButton.setFont(font)
        self.refreshButton.setObjectName("refreshButton")
        self.gridLayout_3.addWidget(self.refreshButton, 0, 0, 1, 1)
        self.last_update_date = QtWidgets.QLabel(self.centralwidget)
        self.last_update_date.setMinimumSize(QtCore.QSize(0, 0))
        self.last_update_date.setMaximumSize(QtCore.QSize(16777215, 20))
        self.last_update_date.setObjectName("last_update_date")
        self.gridLayout_3.addWidget(self.last_update_date, 1, 0, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout_3)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setMinimumSize(QtCore.QSize(0, 0))
        self.tableView.setLineWidth(3)
        self.tableView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableView.setObjectName("tableView")
        self.gridLayout.addWidget(self.tableView, 1, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1062, 22))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionWord = QtGui.QAction(MainWindow)
        self.actionWord.setObjectName("actionWord")
        self.action_Excel = QtGui.QAction(MainWindow)
        self.action_Excel.setObjectName("action_Excel")
        self.action_Word = QtGui.QAction(MainWindow)
        self.action_Word.setObjectName("action_Word")
        self.menu.addAction(self.action_Excel)
        self.menu.addAction(self.action_Word)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Обозначения цветов и фильтры:"))
        self.radioButton_red.setText(_translate("MainWindow", "Сертифкат и техническая поддержка не действительны"))
        self.radioButton_pink.setText(_translate("MainWindow", "Техническая поддержка не действительна"))
        self.radioButton_yellow.setText(_translate("MainWindow", "Сертифкат не действителен"))
        self.radioButton_gray.setText(_translate("MainWindow", "Срок сертификата истечёт меньше, чем через полгода"))
        self.radioButton_white.setText(_translate("MainWindow", "Сертифкат и техническая поддержка действительны"))
        self.resetButton.setText(_translate("MainWindow", "Сброс фильтра"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"right\"><span style=\" font-size:11pt;\">Поиск: </span></p></body></html>"))
        self.searchBar.setToolTip(_translate("MainWindow", "<html><head/><body><p>Поле для ввода искомой информации</p></body></html>"))
        self.searchBar.setPlaceholderText(_translate("MainWindow", "Введите текст..."))
        self.searchButton.setText(_translate("MainWindow", "Поиск"))
        self.checkBox_date.setToolTip(_translate("MainWindow", "Флаги, применительные только к действительным сертификатам"))
        self.checkBox_date.setText(_translate("MainWindow", "Показать сертификаты, где информация о сроке сертификата не указана"))
        self.checkBox_sup.setToolTip(_translate("MainWindow", "Флаги, применительные только к действительным сертификатам"))
        self.checkBox_sup.setText(_translate("MainWindow", "Показать сертификаты, где информация о технической поддержке не указана"))
        self.refreshButton.setToolTip(_translate("MainWindow", "Требуется интернет-соединение"))
        self.refreshButton.setText(_translate("MainWindow", "Обновить базу данных"))
        self.last_update_date.setToolTip(_translate("MainWindow", "Последнее обновление таблицы"))
        self.last_update_date.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">Актуальность базы:</span></p></body></html>"))
        self.menu.setStatusTip(_translate("MainWindow", "Создание файлов"))
        self.menu.setTitle(_translate("MainWindow", "Файл"))
        self.actionWord.setText(_translate("MainWindow", "Word"))
        self.action_Excel.setText(_translate("MainWindow", "Экспортировать в Excel-файл"))
        self.action_Excel.setStatusTip(_translate("MainWindow", "Сохранение видимой таблицы в Excel-файл"))
        self.action_Word.setText(_translate("MainWindow", "Экспортировать в Word-файл"))
        self.action_Word.setStatusTip(_translate("MainWindow", "Сохранение видимой таблицы в Word-файл"))
