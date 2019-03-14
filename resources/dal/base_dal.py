from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from resources.dao import Base


class BaseDal:

    def __init__(self):
        self.engine = create_engine('postgres://guest:guest@192.168.99.100:5432/guest')
        Base.metadata.bind = self.engine
        self.db_session = sessionmaker(bind=self.engine)
        self.session = self.db_session()
