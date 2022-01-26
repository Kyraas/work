# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

Base = declarative_base()
engine = create_engine('sqlite:///parseddata_eng.db')
conn = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()

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

    def __repr__(self):
        return "%r,%r,%r,%r,%r,%r,%r,%r,%r,%r,%r" % (self.id, self.date_start, self.date_end, self.name, self.docs, self.scheme, self.lab, self.certification, self.applicant, self.requisites, self.support)


def alltbl():
    result = session.query(Certificate).all()
    return result

def valid_data():
    result = session.query(Certificate).filter(Certificate.date_end <= func.current_date()).order_by(Certificate.date_end).all()
    return result

# text="Гром"
# res = session.query(Certificate).filter(Certificate.name.ilike(text)).all()