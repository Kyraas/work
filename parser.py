import requests  # Получение HTTP-запросов, удобнее и стабильнее в работе, чем встроенная библиотека urllib
from bs4 import BeautifulSoup  # Парсинг полученного контента

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
    soup = BeautifulSoup(html, 'html.parser')  # второй параметр это тип документа, с которым мы работаем (опциональный, но использование желательно)
    headers = {}
    item = {}
    data = []
    # cells = []
    
    rows = soup.find_all('tr')  # находим все строки (1918 шт.)
    thead = soup.find("thead").find_all("th")  # находим все заголовки (их 11 шт.)
    
    for i in range(len(thead)):
        headers[i] = thead[i].text.replace("\n", " ")  # вычленяем текст заголовков из html

    for row in rows:
        cells = row.find_all("td")  # получаем ячейки из каждой строки
    print(cells)  # !!! хранит почему-то только последнюю ячейку
        
    for i in headers:
        item[headers[i]] = cells[i].text.replace("\xa0", " ")
        data.append(item)
            

# Основная функция
def parse():
    html = get_html(URL)
    if html.status_code == 200:  # Код ответа об успешном статусе "The HTTP 200 OK" 
        get_content(html.text)
    else:
        print('Error')


parse()
