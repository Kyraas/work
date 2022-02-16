import sys, time
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class statusdemo(QMainWindow):
    def __init__(self, parent = None):
        super(statusdemo, self).__init__(parent)

        self.msgs = ["Checkpoint 001", "Checkpoint 002", "Checkpoint 003", "Checkpoint 000"] # +
        self.n = len(self.msgs)                                                                 # +
        self.i = 0                                                                              # +

        qpb = QPushButton("Debug")
        qpb.clicked.connect(self.debug)
        self.setCentralWidget(qpb)

        self.statusBar = QStatusBar()
        self.setWindowTitle("QStatusBar Debug")
        self.setStatusBar(self.statusBar)

        self.timer = QTimer(self)                                                               # +
        self.timer.setInterval(500)                             
        self.timer.timeout.connect(self.show_message)

    def show_message(self):
        self.statusBar.showMessage(self.msgs[self.i])
        self.i += 1
        if self.i == len(self.msgs): 
            # self.timer.stop()
            self.i = 0

    def debug(self):
        self.timer.start()


def main():
    app = QApplication(sys.argv)
    ex = statusdemo()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()