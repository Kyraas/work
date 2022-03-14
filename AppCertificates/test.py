# -*- coding: utf-8 -*-
from datetime import datetime

from datetime import datetime
import time

start_time = datetime.now()

#Тут выполняются действия
time.sleep(1)

s1 = (datetime.now() - start_time).total_seconds()

time.sleep(3)

s2 = (datetime.now() - start_time).total_seconds()

time.sleep(2)

s3 = (datetime.now() - start_time).total_seconds()

print(s1,"\n",s2-s1,"\n",s3-s2-s1)