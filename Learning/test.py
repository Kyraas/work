class Person:

    def __init__(self, surname, forename, old):
        self.surname = surname
        self.forename = forename
        self.old = old

class SortKey:

    def __init__(self, *args):
        self.obj = args

    def __call__(self, lst):
        if "surname" in lst:
            return sorted(lst, key=self.obj.surname)
        

p = [Person("Иванов", "Иван", 20), Person("Петров", "Степан", 21), Person("Сидоров", "Альберт", 25)]

print(Person.__dict__)

# s = SortKey(p)

# print(s("surname"))