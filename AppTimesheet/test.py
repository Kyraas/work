# Заполнение заказ-нарядов
    # Проверка текущего месяца и месяца в дате заказ-наряда
# Учет отпусков
# Хранение данных о сотрудниках в файле, возможность редактирования этого файла

import openpyxl
import re
from excelfiles import *
from pcalendar import *

vacation = openpyxl.load_workbook("отпуск 2022 бух.xlsx")
sheet = vacation['2021']
fio = "Михайлов Д.С."

# dict_days = get_days()
for i in sheet['A']:
    if i.value == fio:
        print(i.row)
        for j in sheet[i.row]:
            if j.value != None:
                date = j.value
                print(date)

first_day = re.search(r'\d*\.', date).group()
first_day = int(first_day[:1])

first_month = re.search(r'\.\d*\-', date).group() # убираем числа из ФИО
first_month = int(first_month[1:-1])

print(first_day, first_month)
