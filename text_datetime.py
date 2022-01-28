from datetime import *

str_date = '2022-01-28'
cur_date = datetime.date(datetime.strptime(str_date, "%Y-%m-%d"))
print(cur_date)