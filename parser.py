# -*- coding: utf-8 -*-
import requests  # Получение HTTP-запросов, удобнее и стабильнее в работе, чем встроенная библиотека urllib
from bs4 import BeautifulSoup  # Парсинг полученного контента
import sqlite3  # Импортируем библиотеку, соответствующую типу нашей базы данных 

# Константы
URL = 'https://fstec.ru/tekhnicheskaya-zashchita-informatsii/dokumenty-po-sertifikatsii/153-sistema-sertifikatsii/591'
  
# Заголовки нужны для того, чтобы сервер не посчитал нас за ботов, не заблокировал нас    
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/96.0.4664.110 Safari/537.36 OPR/82.0.4227.43', 'accept': '*/*'}


# params - дополнительные параметры (опционально), например номер страницы
def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    headers, item = {}, {}
    cells, data = [], []
    
    soup = BeautifulSoup(html, 'html.parser')  # второй параметр это тип документа, с которым мы работаем (опциональный, но использование желательно)
    table = soup.find("table", id="at_227")  # находим нужную нам таблицу
    thead = table.find("thead").find_all("th")  # находим все заголовки (их 11 шт.)
    
    for i in range(len(thead)):
        headers[i] = thead[i].text.replace("\n", " ")  # вычленяем текст заголовков из html

    for row in table.find("tbody").find_all("tr"):  # находим все строки в таблице (их 1914 шт.)
        cell = []
        for td in row.find_all('td'):  # находим ячейки в каждой строке
            cell.append(td.text.replace("\xa0", " "))  # вычленяем текст из каждой ячейки строки
        if cell:  # если оно есть, то добавляем его в список cells
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
    if html.status_code == 200:  # Код ответа об успешном статусе "The HTTP 200 OK" 
        return get_content(html.text)
    else:
        print('Error')
        

data = parse()

# Создаем соединение с нашей базой данных
conn = sqlite3.connect('parseddata.db')

# Создаем курсор - это специальный объект который делает запросы и получает их результаты
cur = conn.cursor()

d = []

for i in data:
    d.append(tuple(i.values()))
# print(d)

cur.executemany('INSERT INTO Сертификаты VALUES (?,?,?,?,?,?,?,?,?,?,?)', d)
conn.commit()
# Не забываем закрыть соединение с базой данных
conn.close()
