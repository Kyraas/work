# -*- coding: utf-8 -*-
# антипаттерн UPSERT https://habr.com/ru/company/otus/blog/547094/
import requests  # Получение HTTP-запросов, удобнее и стабильнее в работе, чем встроенная библиотека urllib
from bs4 import BeautifulSoup  # Парсинг полученного контента
import sqlite3  # Импортируем библиотеку, соответствующую типу нашей базы данных
from datetime import datetime
from orm import Certificate as tbl, Session
sqlite3.paramstyle = "named"

# Константы
URL = "https://fstec.ru/tekhnicheskaya-zashchita-informatsii/dokumenty-po-sertifikatsii/153-sistema-sertifikatsii/591"
  
# Заголовки нужны для того, чтобы сервер не посчитал нас за ботов и не заблокировал   
HEADERS = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/96.0.4664.110 Safari/537.36 OPR/82.0.4227.43", "accept": "*/*"}


# params - дополнительные параметры (опционально), например номер страницы
def get_html(url, params=None):
    try:
        r = requests.get(url, headers=HEADERS, params=params)
        return r
    except requests.exceptions.ConnectionError:
        # print("Ошибка соединения")
        return False
        

def get_content(html):
    headers = {
        0:'id',
        1:'date_start',
        2:'date_end',
        3:'name',
        4:'docs',
        5:'scheme',
        6:'lab',
        7:'certification',
        8:'applicant',
        9:'requisites',
        10:'support'
    }
    item = {}
    cells, data = [], []
    
    soup = BeautifulSoup(html, "html.parser")  # второй параметр это тип документа, с которым мы работаем (опциональный, но использование желательно)
    table = soup.find("table", id="at_227")  # находим нужную нам таблицу

    for row in table.find("tbody").find_all("tr"):  # находим все строки в таблице (их 1914 шт.)
        cell = []
        for td in row.find_all("td"):  # находим ячейки в каждой строке
            cell.append(td.text.replace("\xa0", " "))  # вычленяем текст из каждой ячейки строки
        if cell:  # если он есть, то добавляем его в список cells
            cells.append(cell)  # данный список содержит данные всех ячеек таблицы

    for row in cells:  # цикл по строкам в cells
        item = {}
        for i in headers:  # цикл по заголовкам
            item[headers[i]] = row[i]  # каждому заголовку сопостовляем ячейку из строки
        data.append(item)  # полученный item добавляем в общий список данных data
    return data
        

# Основная функция
def parse():
    html = get_html(URL)
    if html != False:
        if html.status_code == 200:  # Код ответа об успешном статусе "The HTTP 200 OK" 
            return get_content(html.text)
        else:
            return False
    else:
        return False

def count_rows(data):
    return(len(data))

def update_table(data):
    k = 0
    try:
        # изменяем формат даты на YYYY-MM-DD для дальнейшей обработки в SQLite
        for i in data:
            i['date_start'] = datetime.strptime(i['date_start'], "%d.%m.%Y").date()
            if i['date_end'] != '' and i['date_end'] != 'бессрочно' and i['date_end'] != '#Н/Д':
                i['date_end'] = datetime.strptime(i['date_end'], "%d.%m.%Y").date()
            if i['support'] != '' and i['support'] != 'бессрочно' and i['date_end'] != '#Н/Д':
                i['support'] = datetime.strptime(i['support'], "%d.%m.%Y").date()
            tbl.upsert(i)
            k += 1
            yield(k)

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite: ", error)
    
    finally:
        Session.commit()   # сохраняем изменения в бд

def commit_db():
    success = "База данных успешно обновлена."
    return success
