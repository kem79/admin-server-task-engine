from sqlalchemy.orm.exc import NoResultFound

from resources.dao.applications_dao import Application


class ApplicationsDal:

    def __init__(self, session):
        super().__init__()
        self.session = session

    def create_if_not_exist(self, application_name):
        if not self.exists(application_name):
            new_application = Application(name=application_name)
            self.session.add(new_application)
            self.session.commit()
            return new_application.id
        else:
            return self.session.query(Application).filter(Application.name == application_name).one().id

    def exists(self, application_name):
        try:
            self.session.query(Application).filter(Application.name == application_name).one()
            return True
        except NoResultFound:
            return False

    def get(self, application_name):
        try:
            application = self.session.query(Application).filter(Application.name == application_name).one()
            return application
        except NoResultFound:
            return None

