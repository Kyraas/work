import win32api

def get_device():
    i = 0
    try:
        while True:
            device = win32api.EnumDisplayDevices(None, i)
            res = ()
            settings = win32api.EnumDisplaySettings(device.DeviceName, -1)
            for attr in ['PelsWidth', 'PelsHeight', 'DisplayFrequency', 'DisplayFlags']:
                num = getattr(settings, attr)
                t = (num,)
                res += t
            if res != None:
                get_resolutions(device)
                # print("Size:", device.Size)
                print("DeviceName:", device.DeviceName, res)
                print("DeviceString:", device.DeviceString)
                print("StateFlags:", device.StateFlags)
                print("DeviceID:", device.DeviceID)
                print("DeviceKey:", device.DeviceKey, "\n\n")
            i += 1
    except:
        pass

def get_resolutions(device):
    i = 0
    res = set()   # сохраняет только неповторяющиеся значения
    try:
        while True:
            ds = win32api.EnumDisplaySettings(device.DeviceName, i)
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
    print(new_dict)
    return(new_dict)

# get_device()

# monitor = win32api.EnumDisplayMonitors()
# for i in range(len(monitor)):
#     s = monitor[i]  # (hMonitor, hdcMonitor, PyRECT)
#     print(s)
#     k = s[0]
#     info = win32api.GetMonitorInfo(k)
#     print(info, "\n\n")

device = win32api.EnumDisplayDevices(None, 0)
print(device.DeviceName)
# settings = win32api.EnumDisplaySettings(device.DeviceName, -1)
settings = win32api.EnumDisplaySettings(None, -1)
print(settings.PelsWidth, settings.PelsHeight, settings.DisplayFrequency)

# k = input("Нажмите любую кнопку") \\.\DISPLAY2