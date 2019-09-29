from sqlalchemy.ext.declarative import declarative_base
from .database import session, now_utc
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String, DateTime
from sqlalchemy.orm import column_property, relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.sql.expression import cast
from urllib.parse import quote

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

class Edit(Base):
    __tablename__ = 'edit'
    username = Column(String, primary_key=True)
    painting_id = Column(Integer, primary_key=True)
    depicts_id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=now_utc())

    painting_qid = column_property('Q' + cast(painting_id, String))
    depicts_qid = column_property('Q' + cast(depicts_id, String))

    @property
    def user_page_url(self):
        start = 'https://www.wikidata.org/wiki/User:'
        return start + quote(self.username.replace(' ', '_'))
