# -*- coding: utf-8 -*-
# антипаттерн UPSERT https://habr.com/ru/company/otus/blog/547094/
import requests  # Получение HTTP-запросов, удобнее и стабильнее в работе, чем встроенная библиотека urllib
from bs4 import BeautifulSoup  # Парсинг полученного контента
import sqlite3  # Импортируем библиотеку, соответствующую типу нашей базы данных
from datetime import datetime
sqlite3.paramstyle = "named"

# Константы
URL = "https://fstec.ru/tekhnicheskaya-zashchita-informatsii/dokumenty-po-sertifikatsii/153-sistema-sertifikatsii/591"
  
# Заголовки нужны для того, чтобы сервер не посчитал нас за ботов, не заблокировал нас    
HEADERS = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/96.0.4664.110 Safari/537.36 OPR/82.0.4227.43", "accept": "*/*"}


# params - дополнительные параметры (опционально), например номер страницы
def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


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
    # thead = table.find("thead").find_all("th")  # находим все заголовки (их 11 шт.)
    # for i in range(len(thead)):
    #     headers[i] = thead[i].text.replace("\n", " ")  # вычленяем текст заголовков из html

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
    if html.status_code == 200:  # Код ответа об успешном статусе "The HTTP 200 OK" 
        return get_content(html.text)
    else:
        print("Error")


def update_table(data):
    try:
        conn = sqlite3.connect("parseddata.db") # соединение с бд
        cur = conn.cursor() # создание курсора
        print("Установлено соединение с SQLite")

        # d = []  # создаем список для будущих кортежей
        # for i in data:
        #     d.append(tuple(i.values())) # добавляем в список данные, преобразованные в кортежи

        update_query = """INSERT INTO Сертификаты VALUES (:id,:date_start,:date_end,:name,:docs,:scheme,:lab,:certification,:applicant,:requisites,:support) ON CONFLICT("№ сертификата") DO UPDATE SET "Дата внесения в реестр" = date(:date_start), "Срок действия сертификата" = :date_end, "Наименование средства (шифр)" = :name, "Наименования документов, требованиям которых соответствует средство" = :docs, "Схема сертификации"= :scheme, "Испытательная лаборатория" = :lab, "Орган по сертификации" = :certification, "Заявитель" = :applicant, "Реквизиты заявителя (индекс, адрес, телефон)" = :requisites, "Информация об окончании срока технической поддержки, полученная от заявителя" = :support WHERE "№ сертификата" = :id """

        for i in data:
            i['date_start'] = datetime.strptime(i['date_start'], "%d.%m.%Y").date()
            i['date_end'] = datetime.strptime(i['date_end'], "%d.%m.%Y").date()
            if i['support'] != '' and i['support'] != 'бессрочно':
                i['support'] = datetime.strptime(i['support'], "%d.%m.%Y").date()
            cur.execute(update_query, i)
        cur.close()
        conn.commit()   # сохраняем изменения в бд
        if conn.total_changes != 0:
            print("Записи успешно добавлены")

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite: ", error)

    finally:
        if conn:
            print(f"Всего изменено {conn.total_changes} строк.")
            conn.close()    # закрываем соединение с бд
            print("Соединение с SQLite закрыто")

def main():
    data = parse()  # получаем результат функции parse
    update_table(data)

main()
