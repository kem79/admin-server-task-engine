from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from resources.dao.applications_dao import Application
from resources.dao.baselines_dao import Baseline
from resources.dao.distributions_dao import Distribution
from resources.dao.requests_dao import Request