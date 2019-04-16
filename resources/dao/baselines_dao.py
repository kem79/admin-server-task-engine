from app import Base
from resources.dao.applications_dao import Application

from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
from datetime import datetime


class Baseline(Base):
    __tablename__ = 'baseline'
    id = Column(Integer, autoincrement='auto', primary_key=True)
    number_of_users = Column(Integer, nullable=False)
    hatch_rate = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    created_on = Column(DateTime, default=datetime.utcnow())
    updated_on = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())
    application_id = Column(Integer, ForeignKey('application.id'), nullable=False)
    application = relationship(Application,
                               backref=backref('baselines',
                                               uselist=True,
                                               cascade='delete,all'))
