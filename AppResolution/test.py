# https://progi.pro/pywin32-excel-nayti-skolko-listov-nahoditsya-v-knige-i-indeksirovat-po-nomeru-13838302
# https://progi.pro/izmenenie-pereschet-i-izvlechenie-rezultatov-iz-excel-v-python-13554791
# https://runebook.dev/ru/docs/python/library/winreg

import pyedid
from winreg import *

aReg = ConnectRegistry(None,HKEY_LOCAL_MACHINE)

aKey = OpenKey(aReg, r"SYSTEM\CurrentControlSet\Enum\DISPLAY")
for i in range(1024):
    try:
        device_name = EnumKey(aKey, i) # Нумеровываем подклавиши открытого ключа реестра,возвращая строку.
        device_key = OpenKey(aKey, device_name)   # открываем
        print(i,"-",device_name)

        for j in range(1024):
            try:
                device = EnumKey(device_key, j)
                key = OpenKey(device_key, device)
                print("  ", j,"-",device, end="\n")

                params = EnumKey(key, 0)
                Device_Parameters = OpenKey(key, params)
                print("   ", params, end="\n")

                hex = QueryValueEx(Device_Parameters, "EDID")
                # print("EDID: ", hex[0], end="\n\n")
                edid = pyedid.parse_edid(hex[0])
                # print(edid.name,"\n",edid.manufacturer,"\n",edid.serial,"\n",edid.width,"\n",edid.height,"\n",edid.resolutions,"\n")
                # for k in edid:
                #     print(k)
                print(edid)

            except EnvironmentError:
                break
            finally:
                CloseKey(Device_Parameters)
                CloseKey(key)

    except EnvironmentError:
        break
    finally:
        CloseKey(device_key)
