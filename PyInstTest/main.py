def read_file(fname):
    try:
        with open(fname, "r") as f:
            print(f.read())
    except FileNotFoundError:
        print(f"Файл {fname} не найден!")

if __name__ == "__main__":
    read_file("data_files\\file.txt")
    input("Для продолжения нажмите любую клавишу...")