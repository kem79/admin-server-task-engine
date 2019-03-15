from resources.dal.base_dal import BaseDal
from resources.dao.applications_dao import Application
from resources.dao.baselines_dao import Baseline


class BaselinesDal(BaseDal):

    def __init__(self):
        super().__init__()

    def delete(self, application_name, number_of_users, hatch_rate):
        application = self.session.query(Application).filter(Application.name == application_name).one()
        baseline = self.session.query(Baseline).filter(Baseline.number_of_users == number_of_users,
                                                       Baseline.hatch_rate == hatch_rate,
                                                       Baseline.application_id == application.id).one()
        self.session.delete(baseline)
        self.session.commit()
        return baseline.id

    def create(self, application_id, number_of_users, hatch_rate):
        new_baseline = Baseline(number_of_users=number_of_users,
                                hatch_rate=hatch_rate,
                                application_id=application_id)
        self.session.add(new_baseline)
        self.session.commit()
        return new_baseline.id

