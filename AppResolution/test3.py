import ctypes
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
print(screensize)
screensize = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)   # Разрешение виртуального экрана
print(screensize)