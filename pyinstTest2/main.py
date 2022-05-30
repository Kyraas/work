import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def print_file(file_path):
    file_path = resource_path(file_path)
    with open(file_path) as fp:
        for line in fp:
            print(line)


if __name__ == '__main__':
    a = input("Введите что-то")
    print("suka blea tvar")
    print_file('data_files/data.txt')
    my_file = open("BabyFile.txt", "w+")
    my_file.write("Привет, файл!")
    my_file.close()
    b = input("И еще че-нибудь введи")