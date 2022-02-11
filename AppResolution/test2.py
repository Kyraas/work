import ctypes
import struct

def set_res(width, height, bpp=32):
    DM_BITSPERPEL = 0x00040000
    DM_PELSWIDTH = 0x00080000
    DM_PELSHEIGHT = 0x00100000
    CDS_UPDATEREGISTRY = 0x00000001
    SIZEOF_DEVMODE = 148

    user32 = ctypes.windll.user32
    DevModeData = struct.calcsize("32BHH") * bytes('\x00','utf')
    print(struct.calcsize("32BHH"))
    DevModeData += struct.pack("H", SIZEOF_DEVMODE)
    # print(struct.unpack('H', DevModeData))
    DevModeData += struct.calcsize("H") * bytes('\x00','utf')
    print(struct.calcsize("H"))
    # print(struct.unpack('H', DevModeData))
    dwFields = (width and DM_PELSWIDTH or 0) | (height and DM_PELSHEIGHT or 0) | (bpp and DM_BITSPERPEL or 0)
    DevModeData += struct.pack("L", dwFields)
    # print(struct.unpack('L', DevModeData))
    DevModeData += struct.calcsize("l9h32BHL") * bytes('\x00','utf')
    print(struct.calcsize("l9h32BHL"))
    DevModeData += struct.pack("LLL", bpp or 0, width or 0, height or 0)
    # print(struct.unpack('LLL', DevModeData))
    DevModeData += struct.calcsize("8L") * bytes('\x00','utf')
    print(struct.calcsize("8L"))
    # result = user32.ChangeDisplaySettingsA(DevModeData, CDS_UPDATEREGISTRY)

set_res(1024, 768)