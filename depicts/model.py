from sqlalchemy.ext.declarative import declarative_base
from .database import session
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import column_property, relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.sql.expression import cast

Base = declarative_base()
Base.query = session.query_property()

class DepictsItem(Base):
    __tablename__ = 'depicts'
    item_id = Column(Integer, primary_key=True, autoincrement=False)
    label = Column(String)
    description = Column(String)
    commons = Column(String)
    count = Column(Integer)
    qid = column_property('Q' + cast(item_id, String))
    db_alt_labels = relationship('DepictsItemAltLabel',
                                 collection_class=set,
                                 cascade='save-update, merge, delete, delete-orphan',
                                 backref='item')
    alt_labels = association_proxy('db_alt_labels', 'alt_label')

class DepictsItemAltLabel(Base):
    __tablename__ = 'depicts_alt_label'
    item_id = Column(Integer,
                     ForeignKey('depicts.item_id'),
                     primary_key=True,
                     autoincrement=False)
    alt_label = Column(String, primary_key=True)

    def __init__(self, alt_label):
        self.alt_label = alt_label
