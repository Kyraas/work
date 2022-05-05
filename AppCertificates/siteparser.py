# -*- coding: utf-8 -*-
# антипаттерн UPSERT https://habr.com/ru/company/otus/blog/547094/

from datetime import datetime
from sqlite3 import Error   # Импортируем библиотеку,
                            # соответствующую типу нашей базы данных.

from bs4 import BeautifulSoup  # Парсинг полученного контента
from requests import get, exceptions    # Получение HTTP-запросов.
                                        # Удобнее и стабильнее в работе,
                                        # чем встроенная библиотека urllib.

from orm import Certificate as tbl, Session, get_id, delete_id

month = {
    "января": "01",
    "февраля": "02",
    "марта": "03",
    "апреля": "04",
    "мая": "05",
    "июня": "06",
    "июля": "07",
    "августа": "08",
    "сентября": "09",
    "октября": "10",
    "ноября": "11",
    "декабря": "12",
    }

# Константы
URL = "https://fstec.ru/tekhnicheskaya-zashchita-informatsii/\
        dokumenty-po-sertifikatsii/153-sistema-sertifikatsii/591"
  
# Заголовки нужны для того, чтобы сервер
# не посчитал нас за ботов и не заблокировал.
HEADERS = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/96.0.4664.110 Safari/537.36 OPR/82.0.4227.43",
            "accept": "*/*"}

# params - дополнительные параметры (опционально),
# например номер страницы.
def get_html(url, params=None):
    try:
        r = get(url, headers=HEADERS, params=params)
        return r
    except exceptions.ConnectionError:
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
    
    soup = BeautifulSoup(html, "html.parser")   # Второй параметр это тип документа,
                                                # с которым мы работаем.
                                                # (опциональный,
                                                # но использование желательно)
    table = soup.find("table", id="at_227") # Находим нужную нам таблицу.

    for row in table.find("tbody").find_all("tr"):  # Находим все строки
                                                    # в таблице.
        cell = []
        for td in row.find_all("td"):   # Находим ячейки в каждой строке.
            cell.append(td.text.replace("\xa0", " "))   # Вычленяем текст
                                                        # из каждой ячейки строки.
        if cell:    # Если он есть, то добавляем его в список cells.
            cells.append(cell)  # Данный список содержит данные
                                # всех ячеек таблицы.

    for row in cells:  # цикл по строкам в cells
        item = {}
        for i in headers:  # цикл по заголовкам
            item[headers[i]] = row[i]   # Каждому заголовку сопостовляем
                                        # ячейку из строки.
        data.append(item)   # Полученный item добавляем в
                            # общий список данных data.
    return data


def get_update_date(html):
    soup = BeautifulSoup(html, "html.parser")   # Второй параметр это
                                                # тип документа,
                                                # с которым мы работаем.
                                                # (опциональный,
                                                # но использование желательно)
    label = soup.find("dd", class_="modified").text.strip()
    text = label.replace("Обновлено: ", "")
    text = text.split()
    m = month.get(text[1])
    text[1] = m
    date = ".".join(text[:3])
    str_time = " ".join(text[3:])
    actual_date = "Актуальность базы ФСТЭК: " + date + " " + str_time
    return actual_date

# Основная функция
def parse(flag=False):
    html = get_html(URL)
    if html != False:
        if html.status_code == 200: # Код ответа об успешном статусе
                                    # "The HTTP 200 OK"
            if flag:
                return get_update_date(html.text)
            else:
                return get_content(html.text)
        else:
            return False
    else:
        return False


def count_rows(data):
    return(len(data))


def update_table(data):
    k = 0

    # Изменяем формат даты на YYYY-MM-DD
    # для дальнейшей обработки в SQLite.
    try:
        for i in data:
            i['date_start'] = datetime.strptime(i['date_start'],
                                                "%d.%m.%Y").date()
            try:
                i['date_end'] = datetime.strptime(i['date_end'],
                                                "%d.%m.%Y").date()
            except ValueError:
                pass
            try:
                i['support'] = datetime.strptime(i['support'],
                                                "%d.%m.%Y").date()
            except ValueError:
                pass
            tbl.upsert(i)
            k += 1
            yield(k)
    except Error as error:
        print("Ошибка при работе с SQLite: ", error)
    finally:
        Session.commit()    # Сохраняем изменения в БД.

# Сравниваем id в новых и старых данных.
def check_database(data):
    old_id = []
    new_id = []
    old_data = get_id()

    for i in data:
        new_id.append(i['id'])

    for i in old_data:
        d = ''.join(i)
        old_id.append(d)

    result = list(set(old_id) - set(new_id))
    delete_id(result)
    Session.commit()
