import sys
import json

from PyQt6.QtCore import QIODevice, QThread, pyqtSignal
from PyQt6.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt6.QtWidgets import QMainWindow, QApplication
from interface import Ui_MainWindow

databits_list = {
    "8": QSerialPort.DataBits.Data8,
    "7": QSerialPort.DataBits.Data7,
    "6": QSerialPort.DataBits.Data6,
    "5": QSerialPort.DataBits.Data5,
}

# Поток для записи\чтения в COM-порт
class ComPort(QThread):
    read_finished = pyqtSignal(str)

    def __init__(self, com, baudrate, databits, com_timeout, message=None):
        super(ComPort, self).__init__()
        self.message = message
        self.com = com
        self.baudrate = baudrate
        self.databits = databits
        self.com_timeout = com_timeout

    def run(self):
        try:
            result = None
            self.serial_port = QSerialPort()
            self.serial_port.setPortName(self.com)
            self.serial_port.setBaudRate(int(self.baudrate))
            self.serial_port.setDataBits(databits_list.get(self.databits))
            print(self.com, self.baudrate, self.databits, self.com_timeout)

            if self.message:
                self.serial_port.open(QIODevice.OpenModeFlag.WriteOnly)
                if self.serial_port.isOpen():
                    self.serial_port.write(self.message.encode())
                    self.serial_port.waitForBytesWritten()
            else:
                self.serial_port.open(QIODevice.OpenModeFlag.ReadOnly)
                if self.serial_port.isOpen():
                    if self.serial_port.waitForReadyRead(5000):
                        result = self.serial_port.readAll()
                    result = "Ошибка. Таймаут соединения"
        except Exception as error:
            result = str(error)
        finally:
            self.read_finished.emit(result)
            if self.serial_port.isOpen():
                self.serial_port.close()
            self.quit()


class Table(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Генератор шума")

        # Получаем список доступных портов
        for port in QSerialPortInfo.availablePorts():
            self.COMports.addItem(port.portName())

        self.readButton.clicked.connect(self.read)
        self.writeButton.clicked.connect(self.write)
        self.ampSignal.valueChanged.connect(self.check_value)
        self.attSignal.valueChanged.connect(self.check_value)

    # Валидация данных
    def check_value(self, value):
        new_value = round(float(value) * 4) / 4
        comboBox = self.sender()
        if value != new_value:
            if self.ampSignal == comboBox:
                self.ampSignal.setValue(new_value)
            if self.attSignal == comboBox:
                self.attSignal.setValue(new_value)

    # Запись в порт
    def write(self):
        k125 = self.slider125.value()
        k250 = self.slider250.value()
        k500 = self.slider500.value()
        v1k = self.slider1k.value()
        v2k = self.slider2k.value()
        v4k = self.slider4k.value()
        v8k = self.slider8k.value()
        amp_sig = self.ampSignal.value()
        att_sig = self.attSignal.value()
        save_flag = int(self.saveCheckBox.isChecked())

        com = self.COMports.currentText()
        baudrate = self.baudRate.currentText()
        databits = self.dataBits.currentText()
        com_timeout = self.timeOut.currentText()

        message_dict = {
            "K125": k125,
            "K250": k250,
            "K500": k500,
            "1K": v1k,
            "2K": v2k,
            "4K": v4k,
            "8K": v8k,
            "G": amp_sig,
            "A": att_sig,
            "E": save_flag
            }

        message = json.dumps(message_dict)
        self.worker = ComPort(com, baudrate, databits, com_timeout, message)
        self.worker.start()
        self.worker.read_finished.connect(self.get_result)

        self.statusBar().showMessage("Ожидание...")
        self.statusBar().repaint()
        self.readButton.setEnabled(False)
        self.writeButton.setEnabled(False)

    # Чтение из порта
    def read(self):

        com = self.COMports.currentText()
        baudrate = self.baudRate.currentText()
        databits = self.dataBits.currentText()
        com_timeout = self.timeOut.currentText()

        self.worker = ComPort(com, baudrate, databits, com_timeout)
        self.worker.start()
        self.worker.read_finished.connect(self.get_result)
        self.worker.finished.connect(self.worker.quit)

        self.statusBar().showMessage("Ожидание...")
        self.statusBar().repaint()
        self.readButton.setEnabled(False)
        self.writeButton.setEnabled(False)

    # Обновление виджетов
    def get_result(self, result):
        self.statusBar().showMessage(result)
        self.statusBar().repaint()
        self.readButton.setEnabled(True)
        self.writeButton.setEnabled(True)


app = QApplication(sys.argv)
win = Table()
win.show()
sys.exit(app.exec())
