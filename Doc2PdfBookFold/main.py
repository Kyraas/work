# https://habr.com/ru/sandbox/174800/

import os
import sys
from ctypes import windll

from PyQt6.QtCore import QThread, pyqtSlot
from PyQt6.QtWidgets import (QMainWindow, QProgressBar, QApplication,
                            QFileDialog, QMessageBox)

from docx2pdfgui import Ui_MainWindow
from worker import Worker


class App(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.status = self.statusBar()
        self.progressBar = None
        self.worker, self.thread_worker = None, None

        self.startBtn.clicked.connect(self.start)
        self.fileDialogBtn.clicked.connect(self.open_dialog)

    # Обновление прогрессбара
    @pyqtSlot(int)
    def evt_update_progress(self, value):
        self.progressBar.setValue(value)

    # Изменение текста статусбара
    @pyqtSlot(str)
    def change_text(self, text):
        self.status.showMessage(text)
        self.status.repaint()

    # Завершение процесса потока
    @pyqtSlot()
    def finish_process(self):
        self.thread_worker.quit()
        self.worker.deleteLater()
        self.disable_buttons(False)

        # Скрываем прогрессбар
        self.progressBar.setHidden(True)
        self.change_text("Готово.")

    # Инициализация прогрессбара
    def init_progress(self, value):
        self.progressBar = QProgressBar(maximum=value)

        # Добавляем прогрессбар в статусбар
        self.status.addPermanentWidget(self.progressBar)

        # Делаем прогрессбар видимым
        self.progressBar.setHidden(False)

    # (Де)активация кнопок
    def disable_buttons(self, flag):
        self.startBtn.setDisabled(flag)
        self.fileDialogBtn.setDisabled(flag)

    # Диалог выбора папки с файлами для печати
    def open_dialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, "")
        if folder_path:
            self.pathLine.setText(folder_path)

    # Инициализация и запуск потока
    def start_thread(self, outdir, files_to_print):
        self.thread_worker = QThread()
        self.worker = Worker(outdir, files_to_print)
        self.worker.moveToThread(self.thread_worker)

        # Соединяем сигналы и слоты
        self.thread_worker.started.connect(self.worker.run)
        self.worker.change_status.connect(self.change_text)
        self.worker.update_progressbar.connect(self.evt_update_progress)
        self.worker.finished.connect(self.finish_process)
        self.thread_worker.finished.connect(self.thread_worker.deleteLater)
        self.thread_worker.start()
    
    # Запуск работы скрипта
    def start(self):
        files_to_print = []
        outdir = self.pathLine.text().replace('/','\\')

        # Если путь не указан, то ничего не происходит
        if not outdir:
            return

        # Собираем все файлы из папки outdir
        inputs_print = next(os.walk(outdir))[2]
        for file in inputs_print:
            if "~" not in file and (file.endswith('.doc') or file.endswith('.docx')):
                files_to_print.append(file)
        n = len(files_to_print)
        message = f"Будет распечатано {n} файлов. Продолжить?"

        # Окно подтверждения печати
        confirm_print = QMessageBox.question(
            self,
            "Подтвержение печати",
            message
            )

        # Запуск процесса
        if confirm_print == QMessageBox.StandardButton.Yes and files_to_print:
            self.disable_buttons(True)
            self.init_progress(n)
            self.start_thread(outdir, files_to_print)
        else:
            self.disable_buttons(False)
            # Окно об отмене операции
            QMessageBox.information(
                self,
                "Подтвержение печати",
                "Печать отменена."
                )


myappid = 'ЦБИ. Департамент ДАС. Бондаренко М.А. \
            Docx2PDF Book Fold Printing. v1.0.0'
windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
app = QApplication(sys.argv)
win = App()
win.show()
sys.exit(app.exec())
