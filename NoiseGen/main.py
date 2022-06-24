import sys
import json

from PyQt6.QtCore import QIODevice, QTimer
from PyQt6.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt6.QtSerialPort import QSerialPort, QSerialPortInfo
from interface import Ui_MainWindow

# Список размеров байта
databits_list = {
    "8": QSerialPort.DataBits.Data8,
    "7": QSerialPort.DataBits.Data7,
    "6": QSerialPort.DataBits.Data6,
    "5": QSerialPort.DataBits.Data5,
}

# Список стоп-битов
stopbits_list = {
    "1": QSerialPort.StopBits.OneStop,
    "1.5": QSerialPort.StopBits.OneAndHalfStop,
    "2": QSerialPort.StopBits.TwoStop,
}

# Словарь параметров
message_dict = {
    "K125": 0,
    "K250": 0,
    "K500": 0,
    "1K": 0,
    "2K": 0,
    "4K": 0,
    "8K": 0,
    "G": 0,
    "A": 0,
    "E": 0,
}

class GenNoise(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(900, 420)

        # Получаем список доступных портов
        for port in QSerialPortInfo.availablePorts():
            self.COMports.addItem(port.portName())

        # Инициализация объектов
        self.serial_port = QSerialPort()
        self.timer = QTimer()
        self.stopButton.setEnabled(False)

        # Сигналы
        self.timer.timeout.connect(self.error_timeout)
        self.serial_port.errorOccurred.connect(self.handle_error)
        self.serial_port.readyRead.connect(self.read)
        self.serial_port.bytesWritten.connect(self.write_finished)

        # Сигналы виджетов
        self.readButton.clicked.connect(self.open_to_read)
        self.writeButton.clicked.connect(self.write)
        self.openButton.clicked.connect(self.open_file)
        self.stopButton.clicked.connect(self.stop_timer)
        self.resetButton.clicked.connect(self.reset)
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

        self.serial_port.setPortName(self.com)
        self.serial_port.setBaudRate(int(self.baudrate))
        self.serial_port.setDataBits(databits_list.get(self.databits))
        self.serial_port.setStopBits(stopbits_list.get(self.stopbits))

    # Получение пакета с настройками генератора
    def open_to_read(self):
        self.get_values()
        self.serial_port.open(QIODevice.OpenModeFlag.ReadWrite)
        self.serial_port.write(b"PAR?")

    # Сделать кнопки (не)доступными
    def enable_buttons(self, value=True):
        self.readButton.setEnabled(value)
        self.writeButton.setEnabled(value)
        self.stopButton.setEnabled(not value)
        self.resetButton.setEnabled(value)
        self.openButton.setEnabled(value)

    # При получении сигнала отправки данных с порта, считываем их
    def read(self):
        line = None
        self.timer.stop()
        if self.serial_port.isOpen():
            line = self.serial_port.readAll().data().decode().strip()
            if line == "OK" or line == "ER":
                self.statusBar().showMessage(line)
            else:
                try:
                    self.change_values(json.loads(line))
                    self.statusBar().showMessage("")
                except json.decoder.JSONDecodeError as error:
                    self.statusBar().showMessage(f"Ошибка декодирования из JSON: {error}")

            self.serial_port.close()
            self.statusBar().repaint()
            self.enable_buttons()
        else:
            self.statusBar().showMessage("Ошибка. Порт не открыт")
            self.statusBar().repaint()

    # Применяем полученные значения
    def change_values(self, settings):
        try:
            self.slider125.setValue(settings["K125"])
            self.slider250.setValue(settings["K250"])
            self.slider500.setValue(settings["K500"])
            self.slider1k.setValue(settings["1K"])
            self.slider2k.setValue(settings["2K"])
            self.slider4k.setValue(settings["4K"])
            self.slider8k.setValue(settings["8K"])
            self.ampSignal.setValue(settings["G"] * 0.25)
            self.attSignal.setValue(settings["A"] * 0.25)
            if settings["E"] == 1 or settings["E"] == '1':
                self.saveCheckBox.setChecked(True)
        except KeyError as error:
            self.statusBar().showMessage(f"Неверные параметры. Ожидался: {error}")

    # Остановка таймера
    def stop_timer(self):
        self.timer.stop()
        if self.serial_port.isOpen():
            self.serial_port.close()
        self.statusBar().showMessage("")
        self.statusBar().repaint()
        self.enable_buttons()

    # Вывод ошибки по истечении таймера
    def error_timeout(self):
        self.stop_timer()
        self.statusBar().showMessage("Ошибка. Таймаут соединения")

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
            "G": int(amp_sig),
            "A": int(att_sig),
            "E": save_flag
            }

        message = json.dumps(message_dict)
        self.get_values()
        self.serial_port.open(QIODevice.OpenModeFlag.ReadWrite)
        if self.serial_port.isOpen():
            self.serial_port.write(message.encode())
            self.statusBar().showMessage("Ожидание...")
            self.statusBar().repaint()
            self.enable_buttons(False)

    # При получении сигнала завершения записи данных
    # запускаем таймер ожидания ответа
    def write_finished(self):
        self.timer.start(self.timeout * 1000)
        self.statusBar().showMessage("Ожидание...")
        self.statusBar().repaint()
        self.enable_buttons(False)

    # Открыть файл с парамтерами
    def open_file(self):
        data = ""
        filename, fileformat = QFileDialog.getOpenFileName(self, "Открыть файл параметров")
        if filename:
            with open(filename, 'r') as f:
                for line in f:
                    data += line.strip()
            print(data)
            try:
                settings = json.loads(data)
                self.change_values(settings)
            except json.decoder.JSONDecodeError as error:
                self.statusBar().showMessage(f"Ошибка декодирования из JSON: {error}")
        else:
            return
        
    # Сброс настроек по умолчанию
    def reset(self):
        self.change_values({x:0 for x in message_dict})
        self.COMports.setCurrentIndex(0)
        self.baudRate.setCurrentIndex(3)
        self.dataBits.setCurrentIndex(3)
        self.stopBits.setCurrentIndex(0)
        self.timeOut.setValue(5)
        self.saveCheckBox.setChecked(False)

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
