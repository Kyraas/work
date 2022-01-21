import sqlite3
from peewee import *
# import sqlite3
con = SqliteDatabase('parseddata.db')
cur = con.cursor()

class BaseModel(Model):
    class Meta:
        database = con

