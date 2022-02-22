import pyedid
from winreg import *

def get_all_EDID():
    print("\n\n")
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

def get_EDID():
    aReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    MonitorKey = OpenKey(aReg, r"SYSTEM\CurrentControlSet\Services\monitor\Enum")   # узнаем какой монитор подключен к компьютеру на данный момент
    path = QueryValueEx(MonitorKey, "0")    # получаем путь к нужному монитору
    print("\nТекущий монитор: ", path[0], "\n")
    CloseKey(MonitorKey)    # закрываем текущую открытую ветку

    EdidKey = OpenKey(aReg, rf"SYSTEM\CurrentControlSet\Enum\{path[0]}\Device Parameters")  # открываем нужную ветку, используя полученные данные
    hex = QueryValueEx(EdidKey, "EDID") # получаем EDID
    edid = pyedid.parse_edid(hex[0])    # конвертируем х16 EDID в читаемый вид
    CloseKey(EdidKey)

    print(edid)
