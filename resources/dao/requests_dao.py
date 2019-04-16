from app import Base
from resources.dao.baselines_dao import Baseline

from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship, backref
from datetime import datetime


class Request(Base):
    __tablename__ = 'request'
    id = Column(Integer, autoincrement='auto', primary_key=True)
    method = Column(String(250), nullable=False)
    name = Column(String(250), nullable=False)
    number_of_requests = Column(Integer)
    number_of_failures = Column(Integer)
    median_response_time = Column(Float(precision=2))
    average_response_time = Column(Float(precision=2))
    min_response_time = Column(Float(precision=2))
    max_response_time = Column(Float(precision=2))
    average_content_size = Column(Integer)
    requests_per_second = Column(Float(precision=2))
    created_on = Column(DateTime, default=datetime.utcnow())
    updated_on = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())
    baseline_id = Column(Integer, ForeignKey('baseline.id'), nullable=False)
    baseline = relationship(Baseline,
                            backref=backref('request',
                                            uselist=True,
                                            cascade='delete,all'))
