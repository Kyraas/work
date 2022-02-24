# Производственный календарь скачан с сайта: http://www.formy-i-blanki.ru/proizvodstvennyj_kalendar/2022
import openpyxl

def set_year(year=2022):
    wb = openpyxl.load_workbook(f"Производственный-календарь-{year}.xlsx")
    calendar = wb['Календарь']    # лист с нашим департаментом
    return calendar

def get_days(n, year):

    calendar = set_year(year)
    row = 4
    col = 3
    month = []
    month_dict = {}
    work, pre_holiday = [], []
    # hours = 0.0
    k = 0

    for _ in range(4):
        for _ in range(3):
            for j in range(col, col + 6): # от C до I (не включительно)
                for i in range(row, row + 7):
                    c = calendar.cell(row = i, column = j)
                    if c.value != None: # если есть число
                        if type(c.fill.start_color.index) == str:   # рабочие дни
                            work.append(c.value)
                        elif c.fill.start_color.index == 0: # предпраздничные дни
                            pre_holiday.append(c.value)
            col += 6
            month_dict["work"] = work
            month_dict["pre_holiday"] = pre_holiday
            month.append(month_dict)
            if k == n:
                return month_dict
            k += 1
            month_dict.clear()
            work = []
            pre_holiday = []
        col = 3
        row += 8

test = get_days(11, 2022)
print(test)