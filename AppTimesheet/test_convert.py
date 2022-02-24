import win32com.client as win32
import os

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