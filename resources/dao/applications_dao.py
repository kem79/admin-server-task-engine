from app import Base

from sqlalchemy import Column, Integer, String


class Application(Base):
    __tablename__ = 'application'
    id = Column(Integer(), autoincrement="auto", primary_key=True, index=True)
    name = Column(String(250), unique=True, nullable=False)
