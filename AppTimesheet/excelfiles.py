import win32com.client as win32
import os

def convert_xls():
    fname = os.path.abspath("Производственный-календарь-2021.xls")   # получаем абсолютный путь
    print("Запускаем Excel...")
    excel = win32.gencache.EnsureDispatch('Excel.Application')  # Запускаем Excel
    print("Открываем файл по пути: ", fname)
    wb = excel.Workbooks.Open(fname)    # Открываем .xls-файл по указанному пути (файл не должен быть открыт)

    print("Сохраняем файл как .xlsx...")
    wb.SaveAs(fname+"x", FileFormat = 51)    # FileFormat = 51 is для .xlsx расширения, FileFormat = 56 is для .xls расширения
    print("Закрываем файл...")
    wb.Close()                               # Закрываем файл
    print("Закрываем Excel.")
    excel.Application.Quit()    # Закрываем Excel

def create_new(timesheet):
    fname = os.path.abspath("Табель 2022 Шаблон.xlsx")   # получаем абсолютный путь
    excel = win32.gencache.EnsureDispatch('Excel.Application')  # Запускаем Excel
    print("Открываем файл по пути: ", fname)
    path = os.path.split(fname) # отделяем последнюю чатсь пути к файлу
    path = path[0] + '\\' + timesheet   # вставляем новое название файла в путь
    print("Новый файл создаётся по пути:", path)
    wb = excel.Workbooks.Open(fname)    # Открываем .xls-файл по указанному пути (файл не должен быть открыт)
    print(f"Сохраняем файл как '{timesheet}' ")
    wb.SaveAs(path, FileFormat = 51)    # FileFormat = 51 is для .xlsx расширения, FileFormat = 56 is для .xls расширения
    wb.Close()                               # Закрываем файл
    excel.Application.Quit()    # Закрываем Excel

def save_file(timesheet):   # необходимо сохранить файл не через библиотеку openpyxl для сохранения кэша. Таким образом Excel произведёт вычисление формул в файле и можно будет получить результат этих формул
    fname = os.path.abspath(timesheet)   # получаем абсолютный путь
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    workbook = excel.Workbooks.Open(fname)
    workbook.Save()
    workbook.Close()
    excel.Quit()        
