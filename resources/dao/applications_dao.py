from app import Base

from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime


class Application(Base):
    __tablename__ = 'application'
    id = Column(Integer(), autoincrement="auto", primary_key=True, index=True)
    name = Column(String(250), unique=True, nullable=False)
    created_on = Column(DateTime, default=datetime.utcnow())
    updated_on = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())
