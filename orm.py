# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Column, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import sqlalchemy as db

engine = create_engine('sqlite:///parseddata_eng.db')
connection = engine.connect()

Base = declarative_base()
session = Session(bind=engine)

class Certificate(Base):
    __tablename__ = 'certificates'
    id = Column(String, primary_key=True)
    date_start = Column(Date, nullable=False)
    date_end = Column(Date, nullable=False)
    name = Column(String, nullable=False)
    docs = Column(String, nullable=False)
    scheme = Column(String, nullable=False)
    lab = Column(String, nullable=False)
    certification = Column(String)
    applicant = Column(String, nullable=False)
    requisites = Column(String, nullable=False)
    support = Column(String)

query = db.select(Certificate)
ResultProxy = connection.execute(query)
ResultSet = ResultProxy.fetchall()
print(ResultSet)