from app import Base
from resources.dao.baselines_dao import Baseline

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
from datetime import datetime


class Distribution(Base):
    __tablename__ = 'distribution'
    id = Column(Integer(), autoincrement="auto", primary_key=True)
    name = Column(String(250), nullable=False)
    number_of_requests = Column(Integer())
    fifty_percentile = Column(Integer())
    sixty_six_percentile = Column(Integer())
    seventy_five_percentile = Column(Integer())
    eighty_percentile = Column(Integer())
    ninety_percentile = Column(Integer())
    ninety_five_percentile = Column(Integer())
    ninety_eight_percentile = Column(Integer())
    ninety_nine_percentile = Column(Integer())
    one_hundred_percentile = Column(Integer())
    created_on = Column(DateTime, default=datetime.utcnow())
    updated_on = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())
    baseline_id = Column(Integer, ForeignKey('baseline.id'), nullable=False)
    baseline = relationship(Baseline,
                            backref=backref('distributions',
                                            uselist=True,
                                            cascade='delete,all'))