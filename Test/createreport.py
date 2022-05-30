from os import path
import win32com.client as win32
from xlsxwriter import Workbook
from datetime import datetime as dt


def convert_xls(file):
    fname = path.abspath(file)
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    wb = excel.Workbooks.Open(fname)
    # FileFormat = 51 is для .xlsx расширения,
    # FileFormat = 56 is для .xls расширения
    wb.SaveAs(fname+"x", FileFormat = 51)
    wb.Close()
    excel.Application.Quit()


def convert_list(data):
    new_data = ""
    if isinstance(data, list):
        for ans in data:
            print(ans)
            new_data = ",".join(str(ans))
    return new_data


def create_new(name, answers, correct_answers, password, data=None):
    fname = f"Отчёт {name}.xlsx"
    report = Workbook(fname)
    sheet = report.add_worksheet()
    headers_format = report.add_format({'text_wrap': True,
                                        'bold': True,
                                        'align': "center",
                                        'valign': "vcenter"})
    reports_format = report.add_format({'text_wrap': True,
                                    'bold': True,
                                    'valign': "vcenter"})
    text_format = report.add_format({'align': "center",
                                    'valign': "vcenter"})

    sheet.set_column(0, 0, 10)  #A
    sheet.set_column(1, 2, 12)  #B,C
    # sheet.set_column(5, 5, 20)  #F
    sheet.set_column(6, 6, 20)  #G
    sheet.write('A1',"Вопрос №", headers_format)
    sheet.write('B1',"Выбранный ответ", headers_format)
    sheet.write('C1',"Правильный ответ", headers_format)
    # sheet.write('D1',"Набрано баллов", headers_format)

    sheet.write('F1',"ФИО студента:", reports_format)
    sheet.write('G1', name)

    # sheet.write('F2',"Дата выполнения теста:", reports_format)
    # sheet.write('F3',"Время начала выполнения теста:", reports_format)
    # sheet.write('F4',"Время завершения выполнения теста:", reports_format)
    # sheet.write('F5',"Длительность выполнения теста:", reports_format)
    # sheet.write('F6',"Набрано баллов всего:", reports_format)
    # sheet.write('F7',"Кол-во вопросов в тесте:", reports_format)
    # sheet.write('F8',"Максимально возможное кол-во баллов:", reports_format)
    # sheet.write('F9',"Дата изменения теста:", reports_format)

    # k = 2
    # for d in data:
    #     sheet.write(f'G{k}', d)
    #     k +=1
    
    for i in range(len(answers)):
        n = str(i+2)
        num = int(answers[i][0])
        answer = answers[i][1]

        if len(correct_answers[i]) == 1:
            correct = correct_answers[i][0]
        else:
            correct = ", ".join(map(str, correct_answers[i]))

        if isinstance(answer, list):
            answer = ", ".join(map(str, answer))

        sheet.write(f'A{n}', num, text_format)
        sheet.write(f'B{n}', answer, text_format)
        sheet.write(f'C{n}', correct, text_format)

    report.close()
    protect_file(fname, password)


def protect_file(file, password):
    fname = path.abspath(file)
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    excel.DisplayAlerts = False
    wb = excel.Workbooks.Open(fname)
    wb.SaveAs(fname, 51, password)                                               
    wb.Close() 
    excel.Application.Quit()

# create_new("Иванов И.И.", [[1,2], [2,2], [3,[1,2]]], [[2],[3],[1,2]], "admin", )
