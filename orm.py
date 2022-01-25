# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///parseddata_eng.db')

class Certificate(Base):
    __tablename__ = 'certificates'
    id = Column(String, primary_key=True)
    date_start = Column(String, nullable=False)
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