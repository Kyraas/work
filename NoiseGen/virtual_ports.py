import sys
import json

from PyQt6.QtCore import QIODevice
from PyQt6.QtSerialPort import QSerialPort
from PyQt6.QtWidgets import (QMainWindow, QApplication,
                            QPushButton, QVBoxLayout, QWidget)

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Тест")

        self.message_dict = {
            "K125": 5,
            "K250": 3,
            "K500": 0,
            "1K": 10,
            "2K": 8,
            "4K": 2,
            "8K": 1,
            "G": 41,
            "A": 19,
            "E": 1
            }

        self.message = json.dumps(self.message_dict)
        container = QWidget()
        layout = QVBoxLayout()
        self.startButton = QPushButton("Старт")
        self.stopButton = QPushButton("Стоп")

        self.setCentralWidget(container)
        container.setLayout(layout)
        layout.addWidget(self.startButton)
        layout.addWidget(self.stopButton)

        self.serial_port = QSerialPort()
        self.serial_port.setPortName("COM2")
        self.serial_port.setBaudRate(9600)
        self.serial_port.setDataBits(QSerialPort.DataBits.Data8)
        self.serial_port.setStopBits(QSerialPort.StopBits.OneStop)

        self.startButton.clicked.connect(self.start)
        self.stopButton.clicked.connect(self.stop)
        self.serial_port.readyRead.connect(self.read)

    def start(self):
        print("Открываем порт на чтение и запись")
        self.serial_port.open(QIODevice.OpenModeFlag.ReadWrite)

    def read(self):
        print("Принимаем сообщение...")
        line = self.serial_port.readAll().data().decode()
        print("Получено сообщение: ", line)

        if line != "PAR?":
            self.message = "OK"
        else:
            self.message = "\t\t" + json.dumps(self.message_dict)
        print("Ответное сообщение: ", self.message)

        if self.serial_port.isOpen():
            print("Отправляем ответ...")
            self.serial_port.write(self.message.encode())
            self.serial_port.waitForBytesWritten()
            print("Сообщение отправлено")
            self.serial_port.close()
            print("Порт закрыт.")

    def stop(self):
        print("Закрываем порт")
        self.serial_port.close()

app = QApplication(sys.argv)
win = App()
win.show()
sys.exit(app.exec())