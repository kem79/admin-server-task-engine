from resources.dao import Base
from sqlalchemy import create_engine

if __name__ == '__main__':
    engine = create_engine('postgres://guest:guest@192.168.99.100:5432/guest')
    Base.metadata.create_all(engine)