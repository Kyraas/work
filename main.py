import sys
import json

from PyQt6.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt6.QtCore import QIODevice, QTimer
from PyQt6.QtWidgets import QMainWindow, QApplication
from interface import Ui_MainWindow

# Список размеров байта
databits_list = {
    "8": QSerialPort.DataBits.Data8,
    "7": QSerialPort.DataBits.Data7,
    "6": QSerialPort.DataBits.Data6,
    "5": QSerialPort.DataBits.Data5,
}

stopbits_list = {
    "1": QSerialPort.StopBits.OneStop,
    "1.5": QSerialPort.StopBits.OneAndHalfStop,
    "2": QSerialPort.StopBits.TwoStop,
}


class GenNoise(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Настрока параметром генератора шума")
        self.setFixedSize(1000, 425)

        # Получаем список доступных портов
        for port in QSerialPortInfo.availablePorts():
            self.COMports.addItem(port.portName())

        self.com = self.COMports.currentText()
        self.baudrate = self.baudRate.currentText()
        self.databits = self.dataBits.currentText()
        self.stopbits = self.stopBits.currentText()
        self.timeout = self.timeOut.value()

        self.serial_port = QSerialPort()
        self.serial_port.setPortName(self.com)
        self.serial_port.setBaudRate(int(self.baudrate))
        self.serial_port.setDataBits(databits_list.get(self.databits))
        self.serial_port.setStopBits(stopbits_list.get(self.stopbits))

        self.timer = QTimer()
        self.timer.timeout.connect(self.error_timeout)

        self.serial_port.errorOccurred.connect(self.handle_error)
        self.serial_port.readyRead.connect(self.read)
        self.serial_port.bytesWritten.connect(self.write_finished)

        self.readButton.clicked.connect(self.open_to_read)
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

    # Получение данных COM-порта
    def get_values(self):
        self.com = self.COMports.currentText()
        self.baudrate = self.baudRate.currentText()
        self.databits = self.dataBits.currentText()
        self.stopbits = self.stopBits.currentText()
        self.timeout = self.timeOut.value()

    # Получение пакета с настройками генератора
    def open_to_read(self):
        self.get_values()
        self.serial_port.open(QIODevice.OpenModeFlag.ReadWrite)
        self.serial_port.write(b"PAR?")

    # При получении сигнала отправки данных с порта, считываем их
    def read(self):
        line = None
        self.timer.stop()
        if self.serial_port.isOpen():
            line = self.serial_port.readAll().data().decode().strip()
            if line == "OK" or line == "ER":
                self.statusBar().showMessage(line)
            else:
                self.change_values(json.loads(line))
                self.statusBar().showMessage("")

            self.serial_port.close()
            self.statusBar().repaint()
            self.readButton.setEnabled(True)
            self.writeButton.setEnabled(True)
        else:
            self.statusBar().showMessage("Ошибка. Порт не открыт")
            self.statusBar().repaint()

    # Применяем полученные значения
    def change_values(self, settings):
        values = list(settings.values())
        self.slider125.setValue(values[0])
        self.slider250.setValue(values[1])
        self.slider500.setValue(values[2])
        self.slider1k.setValue(values[3])
        self.slider2k.setValue(values[4])
        self.slider4k.setValue(values[5])
        self.slider8k.setValue(values[6])
        self.ampSignal.setValue(values[7] * 0.25)
        self.attSignal.setValue(values[8] * 0.25)

    # Вывод ошибки по истечении таймера
    def error_timeout(self):
        self.timer.stop()
        if self.serial_port.isOpen():
            self.serial_port.close()
        self.statusBar().showMessage("Ошибка. Таймаут соединения")
        self.statusBar().repaint()
        self.readButton.setEnabled(True)
        self.writeButton.setEnabled(True)

    # Отправить пакет с настройками генератора
    def write(self):
        k125 = self.slider125.value()
        k250 = self.slider250.value()
        k500 = self.slider500.value()
        v1k = self.slider1k.value()
        v2k = self.slider2k.value()
        v4k = self.slider4k.value()
        v8k = self.slider8k.value()
        amp_sig = float(self.ampSignal.value()) / 0.25
        att_sig = float(self.attSignal.value()) / 0.25
        save_flag = int(self.saveCheckBox.isChecked())

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
        self.get_values()
        self.serial_port.open(QIODevice.OpenModeFlag.ReadWrite)
        if self.serial_port.isOpen():
            self.serial_port.write(message.encode())
            self.statusBar().showMessage("Ожидание...")
            self.statusBar().repaint()
            self.readButton.setEnabled(False)
            self.writeButton.setEnabled(False)

    # При получении сигнала завершения записи данных
    # запускаем таймер ожидания ответа
    def write_finished(self):
        self.timer.start(self.timeout * 1000)
        self.statusBar().showMessage("Ожидание...")
        self.statusBar().repaint()
        self.readButton.setEnabled(False)
        self.writeButton.setEnabled(False)

    # Получение ошибки
    def handle_error(self, error):
        if error == QSerialPort.SerialPortError.NoError:
            return
        self.statusBar().showMessage(f"{error} {self.serial_port.errorString()}")
        self.statusBar().repaint()


app = QApplication(sys.argv)
win = GenNoise()
win.show()
sys.exit(app.exec())
