import os

from app import Base
from sqlalchemy import create_engine

from resources.dao.applications_dao import Application
from resources.dao.baselines_dao import Baseline
from resources.dao.distributions_dao import Distribution
from resources.dao.requests_dao import Request
from resources.dao.backend_metrics_dao import BackendMetric

if __name__ == '__main__':
    if 'POSTGRES_URI' not in os.environ:
        raise RuntimeError('Create POSTGRES_URI environment variable (format: postgres://user:password@host.port/db).')
    engine = create_engine(os.environ['POSTGRES_URI'])
    if 'CLEAN_FIRST' in os.environ and os.environ['CLEAN_FIRST'].lower() == 'true':
        Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)