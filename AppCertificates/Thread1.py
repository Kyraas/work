import sys
#import time
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets    import *
from PyQt6.QtCore       import *
from PyQt6.QtGui        import *
import threading


class CaptchaThread(QtCore.QObject):

    flagFinished = False                                          # +++

    started  = QtCore.pyqtSignal()
    finished = QtCore.pyqtSignal()
    sendText = pyqtSignal(str)

    @QtCore.pyqtSlot()
    def startText(self, text): 
        self.text = text.split(" ")

        def finishedText():    
            self.finished.emit()

        self.osnovaNew() 
        finishedText()

    def osnovaNew(self): 
        while not self.flagFinished:                              # +++
            for a in self.text:
                self.sendText.emit(str(a))
                QtCore.QThread.msleep(400)

                fl = self.flagFinish(self.flagFinished)           # +++
                if fl: break                                      # +++

            self.flagFinished = True                              # +++

    def flagFinish(self, flagFinished):                           # +++ 
        self.flagFinished = flagFinished
        return self.flagFinished


class textDialog(QWidget):
    @QtCore.pyqtSlot()
    def showText(self):
        pass

class BoostRead(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(600, 500)
        # self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint)
        self.thread = None

        self.inputText = QTextEdit(self)
        self.inputText.setGeometry(10, 10, 580, 180)
        self.inputText.setPlaceholderText("Your text")

        self.outputText = QLineEdit(self)
        self.outputText.setGeometry(50, 300, 495, 100)

        self.startBtn = QPushButton(self)
        self.startBtn.setGeometry(10, 200, 280, 50)
        self.startBtn.setText("Start")
        self.startBtn.clicked.connect(self.sendStart)

        self.stopBtn = QPushButton(self)
        self.stopBtn.setGeometry(310, 200, 280, 50)
        self.stopBtn.setText("Stop")

#        self.stopBtn.clicked.connect(self.sendStart)                    # ---
        self.stopBtn.clicked.connect(self.sendStop)                      # +++

    def sendStart(self):
        if not self.thread:
            self.worker      = CaptchaThread()
            self.text_Dialog = textDialog()

            self.worker.started.connect(self.text_Dialog.showText)
            self.worker.sendText.connect(self.processText)
            self.worker.finished.connect(self.closeText)

            thread = threading.Thread(
                target = self.worker.startText, 
                args = [self.inputText.toPlainText()],  
                daemon = True
            ).start()

    def sendStop(self):                                                   # +++
#        pass # Stop thread
        self.worker.flagFinished = True
        self.worker.flagFinish(self.worker.flagFinished)

    def closeText(self):
        try:
            self.text_Dialog.close()
        except AttributeError:
            pass

    def processText(self, text):
        self.outputText.setText(text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = BoostRead()
    ex.show()
    sys.exit(app.exec())