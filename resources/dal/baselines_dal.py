from sqlalchemy.orm.exc import NoResultFound

from resources.dao.applications_dao import Application
from resources.dao.baselines_dao import Baseline


class BaselinesDal:

    def __init__(self, session):
        super().__init__()
        self.session = session

    def delete(self, application_name, number_of_users, hatch_rate):
        application = self.session.query(Application).filter(Application.name == application_name).one()
        baseline = self.session.query(Baseline).filter(Baseline.number_of_users == number_of_users,
                                                       Baseline.hatch_rate == hatch_rate,
                                                       Baseline.application_id == application.id).one()
        self.session.delete(baseline)
        self.session.commit()
        return baseline.id

    def create(self, application_id, number_of_users, hatch_rate, duration):
        new_baseline = Baseline(number_of_users=number_of_users,
                                hatch_rate=hatch_rate,
                                duration=duration,
                                application_id=application_id)
        self.session.add(new_baseline)
        self.session.commit()
        return new_baseline.id

    def get(self, application_id, number_of_users, hatch_rate):
        try:
            baseline = self.session.query(Baseline).filter(Baseline.number_of_users == number_of_users,
                                                           Baseline.hatch_rate == hatch_rate,
                                                           Baseline.application_id == application_id).one()
            return baseline
        except NoResultFound:
            return None

    def get_all(self, application_id):
        try:
            baselines = self.session.query(Baseline).filter(Baseline.application_id == application_id).all()
            return baselines
        except NoResultFound:
            return None
