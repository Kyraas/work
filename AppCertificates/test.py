from datetime import datetime
n = ""
date = datetime.strptime(n, "%d.%m.%Y").date()
print(date)