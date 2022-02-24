import openpyxl
import re

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
month_list = list(month_dict.values())  # преобразуем словарь в список месяцев, для поиска текущего месяца

wb = openpyxl.load_workbook("Трудоемкость за январь.xlsx")
sheets = wb.sheetnames  # получаем листы
sheet = wb['17 департамент']    # лист с нашим департаментом

cur_month = ""
s = ""
row_start = 0
name = ""
order = ""
full_hours = 0.0
hours = ""
date_order = ""

# rows = sheet.max_row
cols = sheet.max_column

for cell in sheet['B']:
    s = str(cell.value)

    if cur_month == "": # если еще не найдет текущий месяц
        if s != None:
            for i in month_list:
                if s == i.lower():
                    cur_month = i

    if s[:2] == '17':
        name = str(cell.value)
        name = name[2:] # вписать ФИО в новый файл (без числа 17)
        hours = sheet.cell(row=cell.row, column=cols).value # получаем часы из соседней колонки 'С'
        if (hours != None) & (hours != '0ч'):
            hours = hours[:-1]  # убираем букву "ч"
            hours = hours.replace(',', '.') # замена запятой на точку
            full_hours = float(hours)    # суммарные рабочие часы
            row_start = int(cell.row)
            print(name, hours)
    elif (int(cell.row) != row_start) & (row_start != 0):   # получаем заказ-наряды под каждого человека
        hours = sheet.cell(row=cell.row, column=cols).value
        if (hours != None) & (hours != '0ч'):   # если есть рабочие часы на заказ-наряд
            hours = hours[:-1]
            hours = hours.replace(',', '.')
            hours = float(hours)    # рабочие часы на заказ-наряд
            print(str(cell.value), hours)  # заказ-наряд
            date_order = re.search(r'\d\d\.\d\d\.\d\d\d\d', str(cell.value))    # ищем дату в заказ-наряде (формат дд.мм.гггг)
            if date_order != None:  # если есть дата в заказ-наряде
                date_order = date_order.group()
                day = int(date_order[:2])
                m = date_order[3:5]
                year = date_order[6:]
                month = month_dict.get(m)
                print(day, month, year)
        
print(cur_month)