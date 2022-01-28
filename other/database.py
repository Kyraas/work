# Импортируем библиотеку, соответствующую типу нашей базы данных 
import sqlite3
from parser import data

# Создаем соединение с нашей базой данных
# В нашем примере у нас это просто файл базы
conn = sqlite3.connect('parseddata.db')

# Создаем курсор - это специальный объект который делает запросы и получает их результаты
cursor = conn.cursor()

d = []

for i in data:
    d.append(tuple(i.values()))

# И с использованием именнованных замен:
cursor.execute("SELECT Name from Artist ORDER BY Name LIMIT :limit", {"limit": 3})

# Не забываем закрыть соединение с базой данных
conn.close()