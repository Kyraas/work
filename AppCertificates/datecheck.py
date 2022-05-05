# -*- coding: utf-8 -*-
from datetime import datetime, date
from calendar import monthrange
from time import ctime
from os import path

month = {
    "Jan": "01",
    "Feb": "02",
    "Mar": "03",
    "Apr": "04",
    "May": "05",
    "Jun": "06",
    "Jul": "07",
    "Aug": "08",
    "Sep": "09",
    "Oct": "10",
    "Nov": "11",
    "Dec": "12",
    }

def half_year():
    cur_date = datetime.now()
    month = cur_date.month + 5
    year = cur_date.year + month // 12
    month = month % 12 + 1
    day = min(cur_date.day, monthrange(year, month)[1])
    return date(year, month, day)


def get_update_date():

    # Получаем абсолютный путь
    database_path = path.abspath("Database.db")
    try:
        # Получаем дату последнего обновления файла Database.db
        c_time = path.getmtime(database_path)

        # Конвертируем секунды в дату
        date = ctime(c_time)

        # Конвертируем в список
        textdate = str(date).split()
        m = month.get(textdate[1])
        s = textdate[3]
        new_date = ""
        new_date = "Актуальность текущей базы: " + textdate[2] + \
            "." + m + "." + textdate[4] + " г. " + s[:-3]
    except OSError:
        print(f"По указанному пути: {database_path} \
                файл не существует, либо был перемещён.")
        new_date = "База данных не найдена."
    finally:
        return new_date
