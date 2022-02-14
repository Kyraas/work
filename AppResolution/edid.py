import pyedid
from winreg import *
# import ctypes
import win32api

# def get_cur_resolution():
#     ctypes.windll.shcore.SetProcessDpiAwareness(2)  # Игнорирует изменение масштаба, позволяя корректно выдавать текущее разрешение экрана (применимо для Windows 8.1 и выше)
#     user32 = ctypes.windll.user32
#     screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
#     return screensize

def get_cur_resolution():
    res = ()
    device = win32api.EnumDisplayDevices()
    settings = win32api.EnumDisplaySettings(device.DeviceName, -1)
    for attr in ['PelsWidth', 'PelsHeight', 'DisplayFrequency']:
        num = getattr(settings, attr)
        t = (num,)
        res += t
    return res

def get_resolutions():
    aReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)

    MonitorKey = OpenKey(aReg, r"SYSTEM\CurrentControlSet\Services\monitor\Enum")   # узнаем какой монитор подключен к компьютеру на данный момент
    path = QueryValueEx(MonitorKey, "0")    # получаем путь к нужному монитору
    CloseKey(MonitorKey)    # закрываем текущую открытую ветку

    EdidKey = OpenKey(aReg, rf"SYSTEM\CurrentControlSet\Enum\{path[0]}\Device Parameters")  # открываем нужную ветку, используя полученные данные
    hex = QueryValueEx(EdidKey, "EDID") # получаем EDID
    edid = pyedid.parse_edid(hex[0])    # конвертируем х16 EDID в читаемый вид
    CloseKey(EdidKey)
    return edid.resolutions

def set_resolution(width=None, height=None, frequency=None):
    try:
        mode = win32api.EnumDisplaySettings()
        mode.PelsWidth = width
        mode.PelsHeight = height
        mode.DisplayFrequency = frequency
        print(mode.PelsWidth, mode.PelsHeight, mode.DisplayFrequency)
        win32api.ChangeDisplaySettings(mode, 0)
        mes = "Разрешение применено."
        print("Разрешение применено.")
    except:
        win32api.ChangeDisplaySettings(None, 0)
        mes = "Не удалось применить."
        print("Не удалось применить.")
    finally:
        return mes

def set_default():
    win32api.ChangeDisplaySettings(None, 0)
    print("Выставлено по умолчанию.")
    mes = "Выставлено по умолчанию."
    return mes
