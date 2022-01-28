# -*- coding: utf-8 -*-
import datetime, calendar

def half_year():
    cur_date = datetime.datetime.now()
    month = cur_date.month + 5
    year = cur_date.year + month // 12
    month = month % 12 + 1
    day = min(cur_date.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)
    