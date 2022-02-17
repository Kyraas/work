import pyedid
from winreg import *
import win32api
import win32con
import pywintypes

def myFunc(e):
    return e[2]

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
    i=0
    res=set()   # сохраняет только неповторяющиеся значения
    try:
        while True:
            ds=win32api.EnumDisplaySettings(None, i)
            res.add(f"{ds.PelsWidth} {ds.PelsHeight} {ds.DisplayFrequency}")
            i+=1
    except:
        pass
    return(convert_set(res))

def convert_set(res):
    one_res = ()
    dict_res = list(res)
    new_dict = []
    for i in range(len(dict_res)):
        j = dict_res[i].split()
        one_res = (int(j[0]), int(j[1]), int(j[2]))
        new_dict.append(one_res)
    new_dict.sort()
    return(new_dict)

def set_resolution(width=None, height=None, frequency=None):
    try:
        devmode = pywintypes.DEVMODEType()
        # mode = win32api.EnumDisplaySettings()
        devmode.PelsWidth = width
        devmode.PelsHeight = height
        devmode.DisplayFrequency = frequency

        devmode.Fields = win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT | win32con.DM_DISPLAYFREQUENCY

        print(devmode.PelsWidth, devmode.PelsHeight, devmode.DisplayFrequency)
        # status = win32api.ChangeDisplaySettings(devmode, 0)    # 0 - Графический режим для текущего экрана будет изменяться динамически.
        device = win32api.EnumDisplayDevices()
        # print(device.DeviceName)
        status = win32api.ChangeDisplaySettingsEx(device.DeviceName, devmode, 0)    # 0 - Графический режим для текущего экрана будет изменяться динамически.

        print(status)
        if status == 0:
            mes = "Разрешение применено."
            print("Разрешение применено.")
        else:
            mes = "Не удалось применить."
            print("Не удалось применить.")
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

# print(set_resolution(1920, 1080, 30))