from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from configuration import deployment_configuration

Base = declarative_base(metadata=MetaData(schema='admin_server'))

engine = create_engine(deployment_configuration.postgres_url,
                       pool_pre_ping=True)
Base.metadata.bind = engine
db_session = sessionmaker(bind=engine)