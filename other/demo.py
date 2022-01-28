from PyQt5.QtWidgets import QApplication, QWidget, QTableView, QVBoxLayout
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Date
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as db

Base = declarative_base()

engine = db.create_engine('sqlite:///parseddata_eng.db')
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

class DemoWindow(QWidget):
    def __init__(self, header, *args):
        QWidget.__init__(self, *args)
        self.setWindowTitle("Demo QTableView")

        self.table_model = DemoTableModel(self, header)
        self.table_view = QTableView()
        self.table_view.setModel(self.table_model)
        layout = QVBoxLayout(self)
        layout.addWidget(self.table_view)
        self.setLayout(layout)

class DemoTableModel(QAbstractTableModel):

    def __init__(self, parent, header, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        # 5. fetch data
        results = conn.execute(db.select([Certificate])).fetchall()
        self.mylist = results
        self.header = header

    def rowCount(self, parent=None):
        return len(self.mylist)

    def columnCount(self, parent=None):
        return len(self.mylist[0])

    def data(self, index, role):
        # 5. populate data
        if not index.isValid():
            return None
        if (role == Qt.DisplayRole):
            return self.mylist[index.row()][index.column()]
        else:
            return QVariant()

if __name__ == '__main__':
    app = QApplication([])
    header = ['code', 'decription', 'uom']
    win = DemoWindow(header)
    win.show()
    app.exec()