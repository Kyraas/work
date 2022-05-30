from os import path
import win32com.client as win32
from xlsxwriter import Workbook, exceptions


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
    try:
        report = Workbook(fname)
        sheet = report.add_worksheet()
        headers_format = report.add_format({'text_wrap': True,
                                            'bold': True,
                                            'align': "center",
                                            'valign': "vcenter"})
        report_headers = report.add_format({'text_wrap': True,
                                            'bold': True,
                                            'align': "right",
                                            'valign': "vcenter"})
        text_format = report.add_format({'align': "center",
                                        'valign': "vcenter"})
        report_text = report.add_format({'align': "left",
                                        'valign': "vcenter",
                                        'text_wrap': True})

        sheet.set_column(0, 0, 10)  #A
        sheet.set_column(1, 2, 12)  #B,C
        sheet.set_column(5, 5, 18)  #F
        sheet.set_column(6, 6, 25)  #G
        sheet.write('A1',"Вопрос №", headers_format)
        sheet.write('B1',"Выбранный ответ", headers_format)
        sheet.write('C1',"Правильный ответ", headers_format)
        sheet.write('D1',"Набрано баллов", headers_format)

        sheet.write('F1',"ФИО студента:", report_headers)
        sheet.write('G1', name, report_text)

        sheet.write('F2',"Дата выполнения теста:", report_headers)
        sheet.write('F3',"Время начала выполнения теста:", report_headers)
        sheet.write('F4',"Время завершения выполнения теста:", report_headers)
        sheet.write('F5',"Длительность выполнения теста:", report_headers)
        sheet.write('F6',"Набрано баллов всего:", report_headers)
        sheet.write('F7',"Итоговая оценка:", report_headers)
        sheet.write('F8',"Кол-во вопросов в тесте:", report_headers)
        sheet.write('F9',"Максимально возможное кол-во баллов:", report_headers)
        sheet.write('F10',"Дата изменения теста:", report_headers)

        points = data.pop()

        k = 2
        for d in data:
            sheet.write(f'G{k}', d, report_text)
            k +=1
        
        k = 2
        for p in points:
            sheet.write(f'D{k}', p, text_format)
            k +=1

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
    except exceptions.FileCreateError:
        return f"Ошибка: закройте файл {fname}"


def protect_file(file, password):
    fname = path.abspath(file)
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    excel.DisplayAlerts = False
    wb = excel.Workbooks.Open(fname)
    wb.SaveAs(fname, 51, password)                                               
    wb.Close() 
    excel.Application.Quit()
