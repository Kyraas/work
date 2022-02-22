from winreg import *
import win32api
import ctypes
from ctypes import wintypes


class DISPLAY_DEVICEW(ctypes.Structure):
    _fields_ = [
        ('cb', wintypes.DWORD),
        ('DeviceName', wintypes.WCHAR * 32),
        ('DeviceString', wintypes.WCHAR * 128),
        ('StateFlags', wintypes.DWORD),
        ('DeviceID', wintypes.WCHAR * 128),
        ('DeviceKey', wintypes.WCHAR * 128)
    ]

def get_devices():
    EnumDisplayDevices = ctypes.windll.user32.EnumDisplayDevicesW       # get the function address
    EnumDisplayDevices.restype = ctypes.c_bool                          # set return type to BOOL

    displays = []     
    res = ()      # to store display information
    i = 0                   # iteration variable for 'iDevNum'
    j = 0
    while True:
        INFO = DISPLAY_DEVICEW()            # struct object
        INFO.cb = ctypes.sizeof(INFO)       # setting 'cnSize' prior to calling 'EnumDisplayDevicesW'
        Monitor_INFO = DISPLAY_DEVICEW()   
        Monitor_INFO.cb = ctypes.sizeof(Monitor_INFO)  
        if not EnumDisplayDevices(None, i, ctypes.byref(INFO), 0):
            break       # break as soon as False is returned by 'EnumDisplayDevices'
        #j = 0
        while EnumDisplayDevices(INFO.DeviceName,j,ctypes.byref(Monitor_INFO),0):
            print("monitor name:\t\t",Monitor_INFO.DeviceName,'\n\n')
            j+=1

        displays.append(INFO)       # append information to the list
        i += 1

    # display information in a sequential form
    # print(">    Все дисплеи:\n")
    # for x in displays:
    #     print('DeviceName:\t\t', x.DeviceName)
    #     print("DeviceString:\t", x.DeviceString)
    #     print("StateFlags:\t\t", x.StateFlags)
    #     print("DeviceID:\t\t", x.DeviceID)
    #     print("DeviceKey:\t\t", x.DeviceKey)
    #     print(), print()

get_devices()
