from app import Base
from sqlalchemy import create_engine

from resources.dao.applications_dao import Application
from resources.dao.baselines_dao import Baseline
from resources.dao.distributions_dao import Distribution
from resources.dao.requests_dao import Request

if __name__ == '__main__':
    engine = create_engine('postgres://guest:guest@192.168.99.100:5432/guest')
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)