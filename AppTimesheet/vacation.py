import openpyxl
from pcalendar import *

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

def get_initials(name):
    name_dict = name.split()
    initials = name_dict[0] + " "
    for i in range(1, 3):
        s = name_dict[i]
        initials = initials + s[0] + "."
        s = ""
    return initials

def parse_file(name):
    date = None
    employee = get_initials(name)
    try:
        vacation = openpyxl.load_workbook("отпуск 2022 бух.xlsx")
        sheet = vacation['2021']

        for i in sheet['A']:
            if i.value == employee:
                for j in sheet[i.row]:
                    if j.value != None:
                        date = j.value
        vacation.close()
    except FileNotFoundError:
        print("Файл 'отпуск 2022 бух.xlsx' не найден.")
        date = False
    finally:
        return date

def get_vacation(name, month):
    date = parse_file(name)
    if date == None:
        return 0, None, False
    elif date == False:
        return 0, None, True
    s = date.replace("-", " ")
    s = s.replace(".", " ").split()

    start_day = int(s[0])
    start_month = month_dict.get(s[1])
    end_day = int(s[2])
    end_month = month_dict.get(s[3])
    
    if month == start_month:
        return start_day, True, False
    elif month == end_month:
        return end_day, False, False
    else:
        return 0, None, False

def get_days(name, month):
    dict_days = get_workdays(month)
    day, f, err = get_vacation(name, month)

    d = []
    for i in dict_days:
        for x in dict_days[i]:
            if f:
                if x >= day:
                    break
                else:
                    d.append(x)
            elif not f:
                if x <= day:
                    continue
                else:
                    d.append(x)
            else:
                break
        dict_days[i] = d
        d = []
    return dict_days, err
