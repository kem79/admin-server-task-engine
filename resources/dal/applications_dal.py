from sqlalchemy.orm.exc import NoResultFound

from functools import lru_cache

from resources.dal.base_dal import BaseDal
from resources.dao.applications_dao import Application


class ApplicationsDal(BaseDal):

    def __init__(self):
        super().__init__()

    @lru_cache(maxsize=20)
    def create_if_not_exist(self, application_name):
        if not self.exists(application_name):
            new_application = Application(name=application_name)
            self.session.add(new_application)
            self.session.commit()
            return new_application.id
        else:
            return self.session.query(Application).filter(Application.name == application_name).one().id


    @lru_cache(maxsize=20)
    def exists(self, application_name):
        try:
            self.session.query(Application).filter(Application.name == application_name).one()
            return True
        except NoResultFound:
            return False

