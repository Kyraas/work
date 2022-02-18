from winreg import *
import win32api
import win32con
import pywintypes

def get_cur_resolution():
    res = ()
    device = win32api.EnumDisplayDevices()
    settings = win32api.EnumDisplaySettings(device.DeviceName, -1)
    for attr in ['PelsWidth', 'PelsHeight', 'DisplayFrequency', 'DisplayFlags']:
        num = getattr(settings, attr)
        t = (num,)
        res += t
    return res

def get_resolutions():
    i = 0
    res = set()   # сохраняет только неповторяющиеся значения
    try:
        while True:
            ds = win32api.EnumDisplaySettings(None, i)
            res.add(f"{ds.PelsWidth} {ds.PelsHeight} {ds.DisplayFrequency} {ds.DisplayFlags}")
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
        one_res = (int(j[0]), int(j[1]), int(j[2]), int(j[3]))
        new_dict.append(one_res)
    new_dict.sort()
    return(new_dict)

def set_resolution(width=None, height=None, frequency=None, flag=0):
    try:
        # mode = pywintypes.modeType()
        device = win32api.EnumDisplayDevices()
        mode = win32api.EnumDisplaySettings(device.DeviceName)
        mode.PelsWidth = width
        mode.PelsHeight = height
        mode.DisplayFrequency = frequency
        mode.DisplayFlag = flag

        mode.Fields = win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT | win32con.DM_DISPLAYFREQUENCY | win32con.DM_DISPLAYFLAGS

        print(mode.PelsWidth, mode.PelsHeight, mode.DisplayFrequency, mode.DisplayFlag)
        device = win32api.EnumDisplayDevices()
        status = win32api.ChangeDisplaySettingsEx(device.DeviceName, mode, 0)    # 0 - Графический режим для текущего экрана будет изменяться динамически.

        print(status)
        if status == 0:
            mes = "Разрешение применено."
            print("Разрешение применено.")
        else:
            mes = "Не удалось применить."
            print("Не удалось применить.")
            win32api.ChangeDisplaySettings(None, 0)
    # except Exception:
    #     mes = "Ошибка. Не удалось применить. Выставлено по умолчанию"
    #     print("Ошибка. Не удалось применить. Выставлено по умолчанию")
    finally:
        return mes

def set_default():
    win32api.ChangeDisplaySettings(None, 0)
    print("Выставлено по умолчанию.")
    mes = "Выставлено по умолчанию."
    return mes
