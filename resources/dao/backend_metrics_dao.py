from app import Base
from resources.dao.baselines_dao import Baseline

from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
from datetime import datetime


class BackendMetric(Base):
    __tablename__ = 'backend_performance_metric'
    id = Column(Integer(), autoincrement="auto", primary_key=True, index=True)
    average_cpu_usage = Column(Float(precision=2))
    average_memory_usage = Column(Float(precision=2))
    average_response_time = Column(Float(precision=2))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    created_on = Column(DateTime, default=datetime.utcnow())
    updated_on = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())
    baseline_id = Column(Integer, ForeignKey('baseline.id'), nullable=False)
    baseline = relationship(Baseline,
                            backref=backref('baseline',
                                            uselist=True,
                                            cascade='delete,all'))
