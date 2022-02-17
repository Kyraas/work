import win32api


i=0
res=set()
try:
  while True:
    ds=win32api.EnumDisplaySettings(None, i)
    res.add(f"{ds.PelsWidth}x{ds.PelsHeight}, {ds.DisplayFrequency} Гц")
    i+=1
except: pass

print(res)