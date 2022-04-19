import sys, time
from PyQt6.QtWidgets import QDialog, QProgressBar, QStyleFactory, QPushButton, QSlider, QLCDNumber, QHBoxLayout, QVBoxLayout, QApplication, QMessageBox
from PyQt6.QtCore import QThread, pyqtSignal

class DlgMain(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My GUI")

        self.prg = QProgressBar()
        self.prg.setStyle(QStyleFactory.create("Windows"))
        self.prg.setTextVisible(True)

        self.btnStart = QPushButton("Start")
        self.btnStart.clicked.connect(self.evt_btnStart_clicked)

        self.dial = QSlider()
        self.lcd = QLCDNumber()
        self.dial.valueChanged.connect(self.lcd.display)

        self.lytLCD = QHBoxLayout()
        self.lytLCD.addWidget(self.dial)
        self.lytLCD.addWidget(self.lcd)

        self.lytMain = QVBoxLayout()
        self.lytMain.addWidget(self.prg)
        self.lytMain.addWidget(self.btnStart)
        self.lytMain.addLayout(self.lytLCD)
        self.setLayout(self.lytMain)

    def evt_btnStart_clicked(self):
        self.worker = WorkerThread(101)
        self.worker.start()
        self.worker.worker_complete.connect(self.evt_worker_finished)
        self.worker.update_progress.connect(self.evt_update_progress)

    def evt_worker_finished(self, emp):
        QMessageBox.information(self, "Done!", "Worker thread complete\n\n{} {}".format(emp["fn"], emp["ln"]))

    def evt_update_progress(self, val):
        self.prg.setValue(val)


class WorkerThread(QThread):
    update_progress = pyqtSignal(int)
    worker_complete = pyqtSignal(dict)
    def __init__(self, n):
        super(QThread, self).__init__()
        self.n = n

    def run(self):
        for x in range(20, self.n, 20):
            print(x)
            time.sleep(2)
            self.update_progress.emit(x)
        self.worker_complete.emit({"emp_id":1234, "fn":"Mike", "ln":"Miller"})


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlgMain = DlgMain()
    dlgMain.show()
    sys.exit(app.exec())