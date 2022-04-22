import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTextCursor
from PyQt6.QtWidgets import QLineEdit, QPushButton, QDialog, QHBoxLayout, QLabel, QDialogButtonBox, QVBoxLayout, QGridLayout, QLayout, QMessageBox, QMainWindow, QApplication

class Ui_nms_pad(QMainWindow):
    def __init__(self):
        super(Ui_nms_pad, self).__init__()
        self.text = "word"
        self.Find_word()

    def Find_word(self):
        self.findDialog = QDialog(self)

        label = QLabel("Find Word:")
        self.lineEdit = QLineEdit()
        self.lineEdit.setText("word")
        label.setBuddy(self.lineEdit)

        self.findButton = QPushButton("Find Next")
        self.findButton.setDefault(True)
        self.findButton.clicked.connect(self.searchText)

        buttonBox = QDialogButtonBox(Qt.Orientation.Vertical)
        buttonBox.addButton(self.findButton, QDialogButtonBox.ButtonRole.ActionRole)

        topLeftLayout = QHBoxLayout()
        topLeftLayout.addWidget(label)
        topLeftLayout.addWidget(self.lineEdit)

        leftLayout = QVBoxLayout()
        leftLayout.addLayout(topLeftLayout)

        mainLayout = QGridLayout()
        mainLayout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        mainLayout.addLayout(leftLayout, 0, 0)
        mainLayout.addWidget(buttonBox, 0, 1)
        mainLayout.setRowStretch(2, 1)
        self.findDialog.setLayout(mainLayout)

        self.findDialog.setWindowTitle("Find")
        self.findDialog.show()

    def searchText(self):
        cursor = self.text.textCursor()
        findIndex = cursor.anchor()
        text = self.lineEdit.text()
        content = self.text.toPlainText()
        length = len(text)

        self.lastSearchText = text
        index = content.find(text, findIndex)

        if -1 == index:
            errorDialog = QMessageBox(self)
            errorDialog.addButton("Cancel", QMessageBox.ButtonRole.ActionRole)

            errorDialog.setWindowTitle("Find")
            errorDialog.setText("Not Found\"%s\"." % text)
            errorDialog.setIcon(QMessageBox.critical)
            errorDialog.exec()
        else:
            start = index

            cursor = self.text.textCursor()
            cursor.clearSelection()
            cursor.movePosition(QTextCursor.MoveOperation.Start, QTextCursor.MoveMode.MoveAnchor)
            cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.MoveAnchor, start + length)
            cursor.movePosition(QTextCursor.MoveOperation.Left, QTextCursor.MoveMode.KeepAnchor, length)
            cursor.selectedText()
            self.text.setTextCursor(cursor)

app = QApplication(sys.argv)
win = Ui_nms_pad()
win.show()
sys.exit(app.exec())