# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.dialects.sqlite import insert

Base = declarative_base()
engine = create_engine('sqlite:///parseddata_eng.db')
conn = engine.connect()
print("Установлено соединение с SQLite")
Session = scoped_session(sessionmaker())
Session.configure(bind=engine, autoflush=False, expire_on_commit=False)

class Certificate(Base):
    __tablename__ = 'certificates'
    id = Column(String, primary_key=True)
    date_start = Column(Date, nullable=False)
    date_end = Column(String, nullable=False)
    name = Column(String, nullable=False)
    docs = Column(String, nullable=False)
    scheme = Column(String, nullable=False)
    lab = Column(String, nullable=False)
    certification = Column(String)
    applicant = Column(String, nullable=False)
    requisites = Column(String, nullable=False)
    support = Column(String)

    def __repr__(self):
        return "%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r" % (self.id, self.date_start, self.date_end, self.name, self.docs, self.scheme, self.lab, self.certification, self.applicant, self.requisites, self.support)

    def upsert(data):
        stmt = insert(Certificate).values(data)
        stmt = stmt.on_conflict_do_update(
            index_elements = ["id"],
            set_ = data
        )
        conn.execute(stmt)
