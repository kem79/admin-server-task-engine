from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

engine = create_engine('postgres://guest:guest@192.168.99.100:5432/guest')
Base.metadata.bind = engine
db_session = sessionmaker(bind=engine)