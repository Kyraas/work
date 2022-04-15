import os
import time

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

path = os.path.abspath("Database.db")   # получаем абсолютный путь
def get_update_date():
    try:
        c_time = os.path.getmtime(path) # получаем дату последнего обновления файла Database.db
        date = time.ctime(c_time)   # конвертируем секунды в дату
        textdate = str(date).split()    # конвертируем в список
        m = month.get(textdate[1])
        s = textdate[3]
        new_date = ""
        new_date = "Актуальность текущей базы: " + textdate[2] + "." + m + "." + textdate[4] + " г. " + s[:-3]
    except OSError:
        print(f"По указанному пути: {path} файл не существует, либо был перемещён.")
        new_date = "База данных не найдена."
    finally:
        return new_date
