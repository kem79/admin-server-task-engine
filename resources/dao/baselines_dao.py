from app import Base
from resources.dao.applications_dao import Application

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref


class Baseline(Base):
    __tablename__ = 'baseline'
    id = Column(Integer, autoincrement='auto', primary_key=True)
    number_of_users = Column(Integer, nullable=False)
    hatch_rate = Column(Integer, nullable=False)
    application_id = Column(Integer, ForeignKey('application.id'), nullable=False)
    application = relationship(Application,
                               backref=backref('baselines',
                                               uselist=True,
                                               cascade='delete,all'))