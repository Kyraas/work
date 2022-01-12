import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QTextEdit


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.label = QLabel("Кликните внутри этого окна")
        self.setCentralWidget(self.label)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.label.setText("Нажата левая кнопка мыши")
        
        elif e.button() == Qt.MouseButton.MiddleButton:
            self.label.setText("Нажата средняя кнопка мыши")

        elif e.button() == Qt.MouseButton.RightButton:
            self.label.setText("Нажата правая кнопка мыши")

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.label.setText("Левая кнопка мыши отпущена")
        
        elif e.button() == Qt.MouseButton.MiddleButton:
            self.label.setText("Средняя кнопка мыши отпущена")

        elif e.button() == Qt.MouseButton.RightButton:
            self.label.setText("Правая кнопка мыши отпущена")

    def mouseDoubleClickEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.label.setText("Двойной клик левой кнопки мыши")
        
        elif e.button() == Qt.MouseButton.MiddleButton:
            self.label.setText("Двойной клик средней кнопки мыши")

        elif e.button() == Qt.MouseButton.RightButton:
            self.label.setText("Двойной клик правой кнопки мыши")

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()