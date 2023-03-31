import os
import time

import win32com.client
from PyPDF2 import PdfReader, PdfMerger
import win32com.client as win32com
from PyQt6.QtCore import pyqtSignal, QObject, pyqtSlot

# Основной процесс считывания и внесения данных
class Worker(QObject):
    change_status = pyqtSignal(str)
    update_progressbar = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self, outdir, files_list, parent=None):
        super(Worker, self).__init__(parent)
        self.outdir = outdir
        self.files_list = files_list


    @pyqtSlot()
    def run(self):
        # Создаем объект Word
        self.change_status.emit("Запуск Miscrosoft Word...")
        word = win32com.Dispatch('Word.Application')
        k = 0

        self.change_status.emit("Конвертирование файлов в PDF...")
        for file in self.files_list:
            input_path = os.path.join(self.outdir, file)
            output_path = os.path.join(self.outdir, f'{os.path.splitext(file)[0]}.pdf')
            convert_to_pdf(word, input_path, output_path)
            k+=1
            self.update_progressbar.emit(k)

        self.change_status.emit("Выход из Miscrosoft Word...")
        word.Quit()

        # Путь к выходному файлу
        # output_file = r'C:\Users\ddas\Documents\Virtual env\PrintMany\output.pdf'

        # Объединяем все PDF файлы в один большой файл
        self.change_status.emit("Объединение в единый файл...")
        merge_pdfs(self.outdir, "output.pdf")
        self.finished.emit()


# Конвертируем каждый файл в .pdf в формате брошюры
def convert_to_pdf(word, input_path, output_path):

    # Открываем документ
    doc = word.Documents.Open(input_path)
    # doc.PageSetup.BookFoldPrinting = True

    # Изменяем настройки печати
    doc.PrintOut(False, False, 0, output_path, "Microsoft Print to PDF")

    # Закрываем документ и выходим из Word
    doc.Close()


# Объединяем полученные файлы в один
def merge_pdfs(input_dir, output_path):
    # Создаем объект PdfMerger
    merger = PdfMerger()

    # Сканируем директорию и добавляем все PDF файлы в объект merger
    for filename in os.listdir(input_dir):
        if "~" not in filename and filename.endswith('.pdf'):
            filepath = os.path.join(input_dir, filename)
            time.sleep(1) # добавляем задержку на 1 секунду
            pdf = PdfReader(filepath, 'rb')
            merger.append(pdf)

    # Сохраняем объединенный PDF файл
    merger.write(output_path)
    merger.close()
