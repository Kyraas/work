# def read_file():
#     with open("employees.txt", "r", encoding='utf-8') as f:
#         for line in f:
#             print(line.strip())

def add_employee():
    name = input("Введите ФИО сотрудника: ")
    dol = input("Введите должность сотрудника: ")
    stav = input("Введите ставку сотрудника: ")
    employee = name + " " + dol + " " + stav
    answer = input(f"Добавить {employee} ?\n")
    # with open("employees.txt", "w", encoding='utf-8') as f:

def read_file(name):

    with open("employees.txt", "r", encoding='utf-8') as f:
        for line in f:
            if name in line:
                line = line.strip().split()
                line = line[3:]
                stav = line[-1:]
                line = line[:-1]
                dol = " ".join(line)
                return dol, *stav
    

print(read_file("Бондdfа"))
