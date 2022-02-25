import openpyxl
import re
from excelfiles import *
from pcalendar import *

employees = {
    "Бондаренко Мария Алексеевна": ["Инженер-стажер", "1"],
    "Михайлов Даниил Сергеевич": ["Инженер", "1"],
    "Перетягин Николай Александрович": ["Начальник отдела", "1"],
    "Поддубский Александр Анатольевич": ["Ведущий инженер", "1"],
    "Федорищев Иван Васильевич": ["Инженер", "1"],
    "Дрявичев Иван Олегович": ["Инженер-стажер", "0,5"],
    "Рыженко Сергей Викторович": ["Директор департамента", "1"],
    "Тараканов Иван Игоревич": ["Инженер", "1"]
}

month_dict = {
    "01": "Январь",
    "02": "Февраль",
    "03": "Март",
    "04": "Апрель",
    "05": "Май",
    "06": "Июнь",
    "07": "Июль",
    "08": "Август",
    "09": "Сентябрь",
    "10": "Октябрь",
    "11": "Ноябрь",
    "12": "Декабрь"
}

def open_file(name):
    try:
        wb = openpyxl.load_workbook(f"Табель 2022 {name}.xlsx")
        print(f"Успешно открыт файл 'Табель 2022 {name}.xlsx'.")
    except FileNotFoundError:
        print("Файл не найден. Создаем новый...")
        create_new(f"Табель 2022 {name}.xlsx")
        print("Вводим данные в новый файл...")
        wb = openpyxl.load_workbook(f"Табель 2022 {name}.xlsx")
        sheet = wb['Январь']    # первый лист
        sheet['A1'] = name
        if name in employees:
            print(employees[name][0])
            sheet['C3'] = employees[name][0]
            print(employees[name][1])
            sheet['AL3'] = employees[name][1]
            print("Сохраняем внесенные изменения...")
            wb.save(f"Табель 2022 {name}.xlsx")
            print("Пробуем снова ввести данные...")
            open_file(name)
        else:
            print("ФИО сотрудника не найдено в списке.")
    finally:
        return wb

def insert_hours(sheet, month, start_col, hours, day=1):
    dict_days = get_days(month)
    day_row = [5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29,	31,	33,	35,	37,	39,	41,	43,	45,	47,	49,	51,	53,	55,	57,	59,	61,	63,	65]
    column = start_col
    row = 0 
    work = 0
    pre_hol = 0
    for index, value in enumerate(day_row, start=1):
        if day > index: # если задана стартовая дата, то пропускаем дни, до этой даты
            pass
        else:
            if index in dict_days["work"]:  # если день рабочий
                print("Число: ", index, "Строка: ", value)
                if hours > 8:
                    hours = hours - 8
                    print("Отработано:", 8, "осталось: ", hours)
                else:
                    print("отработано:", hours)
                    break

columns = ['E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH']

string = ""
cur_month = ""
name = ""
hours = ""
full_hours = 0.0
row_start = 0
j = 0
order = ""
date_order = ""

laborious = openpyxl.load_workbook("Трудоемкость за январь.xlsx")
department = laborious['17 департамент']    # лист с нашим департаментом

month_list = list(month_dict.values())  # преобразуем словарь в список месяцев, для поиска текущего месяца
max_col = department.max_column

for cell in department['B']:
    string = str(cell.value)

    if cur_month == "": # если еще не найдет текущий месяц
        if string != None:
            for month in month_list:
                if string == month.lower():
                    cur_month = month
                    print(cur_month)

    if string[:2] == '17':
        # if name != "":
        #     print("Сохраняем внесенные изменения...")
        #     timesheet.save(f"Табель 2022 {name}.xlsx")  # закрываем ранее открытый табель
        name = str(cell.value)  # получаем ФИО сотрудника
        name = re.search(r'\D+', name).group() # убираем числа из ФИО

        hours = department.cell(row=cell.row, column=max_col).value # получаем часы из соседней колонки 'С'
        # timesheet = open_file(name) # открываем именной табель
        # sheet_month = timesheet[f'{cur_month}']
        # max_rows = sheet_month.max_row
        j = 1

        if (hours != None) & (hours != '0ч'):   # если у сотрудника есть суммарные рабочие часы
            hours = hours.replace(',', '.') # замена запятой на точку
            hours = re.search(r'\d*\.*\d*', hours).group()  # находим только действительные числа
            row_start = int(cell.row)
            print(name, hours)
            
    elif (int(cell.row) != row_start) & (row_start != 0):   # получаем заказ-наряды под каждого человека
        hours = department.cell(row=cell.row, column=max_col).value
        if (hours != None) & (hours != '0ч'):   # если есть рабочие часы на заказ-наряд
            hours = hours.replace(',', '.')
            hours = re.search(r'\d*\.*\d*', hours).group()  # находим только действительные числа
            print(str(cell.value), hours)  # заказ-наряд
            # sheet_month[f'{columns[j]}3'] = str(cell.value)
            # sheet_month[f'{columns[j]}{max_rows-1}'] = hours

            date_order = re.search(r'\d\d\.\d\d\.\d\d\d\d', str(cell.value))    # ищем дату в заказ-наряде (формат дд.мм.гггг)
            if date_order != None:  # если есть дата в заказ-наряде
                date_order = date_order.group()
                day = int(date_order[:2])
                month_num = date_order[3:5]
                year = date_order[6:]
                month_str = month_dict.get(month_num)
                print(day, month_str, year)
                # if year == "2022":
                #     insert_hours(sheet_month, cur_month, columns[j], hours, day)
                # else:
                #     insert_hours(sheet_month, cur_month, columns[j], hours, 1)
            
            j += 1

# insert_data("Бондаренко Мария Алексеевна", "Январь")
# insert_hours("jshd", "Январь", 1, 26, 19)
