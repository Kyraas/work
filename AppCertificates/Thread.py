# -*- coding: utf-8 -*-
import sys
from PyQt6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QLabel, QWidget
from PyQt6.QtCore import QThread, pyqtSignal, Qt

class MyThread(QThread):
    mysignal = pyqtSignal(str)
    def  __init__(self, parent=None):
        QThread.__init__(self, parent)
    def run(self):
        for i in range(1, 21):
            self.sleep(3)	# "Засыпаем" на 3 секунды
            # Передача данных из потока через сигнал
            self.mysignal.emit("i = %s" % i)

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel("Нажмите кнопку для запуска потока")
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.button = QPushButton("Запустить процесс")
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.label)
        self.vbox.addWidget(self.button)
        self.setLayout(self.vbox)
        self.mythread = MyThread()    # Создаем экземпляр класса
        self.button.clicked.connect(self.on_clicked)
        self.mythread.started.connect(self.on_started)
        self.mythread.finished.connect(self.on_finished)
        self.mythread.mysignal.connect(self.on_change, Qt.ConnectionType.QueuedConnection)
    def on_clicked(self):
        self.button.setDisabled(True) # Делаем кнопку неактивной
        self.mythread.start()         # Запускаем поток
    def on_started(self):	# Вызывается при запуске потока
        self.label.setText("Вызван метод on_started ()")
    def on_finished(self):      # Вызывается при завершении потока
        self.label.setText("Вызван метод on_finished()")
        self.button.setDisabled(False) # Делаем кнопку активной
    def on_change(self, s):
        self.label.setText(s)
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MyWindow()
    window.setWindowTitle("Использование класса QThread")
    window.resize(300, 70)
    window.show()
    sys.exit(app.exec())
