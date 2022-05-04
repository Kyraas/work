# -*- coding: utf-8 -*-
import sqlalchemy as db
from sqlalchemy import Column, Integer, String, Date, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import insert

Base = declarative_base()
engine = create_engine('sqlite:///Database.db',
                        connect_args={'check_same_thread': False})  # Нужно для исключения конфликта потоков GUI и SQLite
conn = engine.connect()
Session = scoped_session(sessionmaker())
Session.configure(bind=engine, autoflush=False, expire_on_commit=False)

class Certificate(Base):
    __tablename__ = 'certificates'
    rowid = Column(Integer)
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

    def __init__(self, id, date_start, date_end, name, docs, scheme,
                 lab, certification, applicant, requisites, support):
        self.id = id
        self.date_start = date_start
        self.date_end = date_end
        self.name = name
        self.docs = docs
        self.scheme = scheme
        self.lab = lab
        self.certification = certification
        self.applicant = applicant
        self.requisites = requisites
        self.support = support

    def __repr__(self):
        return "%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r" % (self.id, self.date_start, self.date_end, self.name,
                                                     self.docs, self.scheme, self.lab, self.certification,
                                                     self.applicant, self.requisites, self.support)

    def upsert(data):
        stmt = insert(Certificate).values(data)
        stmt = stmt.on_conflict_do_update(
            index_elements = ["id"],
            set_ = data
        )
        conn.execute(stmt)

def get_id():
    return conn.execute(db.select(Certificate.id)).fetchall()

def delete_id(list_id):
    for id in list_id:
        conn.execute(db.delete(Certificate).where(Certificate.id == id))

Base.metadata.create_all(engine)
