import traceback

from celery import states
from sqlalchemy.orm.exc import NoResultFound

from app.task_engine import app
from app import db_session
from my_locust.tasks import start, stop

from resources import ApplicationsDal, DistributionsDal, BaselinesDal, RequestsDal

from time import sleep
from celery.utils.log import get_task_logger
from exceptions.admin_server_exceptions import BaselineAlreadyExist
from celery.exceptions import Ignore

logger = get_task_logger(__name__)


@app.task
def get_all(application_name):
    """
    Return all the baselines for a given application
    :param application_name: the name of the micro-service
    :return: 
    """
    session = db_session()
    ad = ApplicationsDal(session)
    application = ad.get(application_name)
    if application:
        bd = BaselinesDal(session)
        baselines = bd.get_all(application_id=application.id)
        if baselines:
            result = []
            for baseline in baselines:
                a_baseline_dict = baseline.__dict__
                del a_baseline_dict['_sa_instance_state']
                del a_baseline_dict['application_id']
                del a_baseline_dict['id']
                result.append(a_baseline_dict)
            return {application_name: result}
        else:
            return None
    else:
        return None


@app.task
def get(application_name,
        number_of_users,
        hatch_rate):
    """
    Get a performance baseline of the micro-service
    :type application_name: str
    :param application_name: the name of the micro-service
    :type number_of_users: int
    :param number_of_users: the number of users used to create the baseline
    :type hatch_rate: int
    :param hatch_rate: the hatch rate of user session to create the baseline
    :rtype dict
    :return: a JSON representing the requests and distribution of the performance baseline
    """
    session = db_session()
    ad = ApplicationsDal(session)
    application = ad.get(application_name)
    if application:
        bd = BaselinesDal(session)
        baseline = bd.get(application.id, number_of_users, hatch_rate)
        if baseline:
            results = {'requests': None,
                       'distributions': None}
            requests = []
            distributions = []

            rd = RequestsDal(session)
            requests_performance = rd.get_by_baseline_id(baseline.id)
            for one_request_type in requests_performance:
                one_request_type_dict = one_request_type.__dict__
                del one_request_type_dict['_sa_instance_state']
                del one_request_type_dict['id']
                del one_request_type_dict['baseline_id']
                request_method = one_request_type_dict.pop('method')
                request_method_name = one_request_type_dict.pop('name')
                requests.append({request_method: {request_method_name: one_request_type_dict}})

            dd = DistributionsDal(session)
            distributions_records = dd.get_by_baseline_id(baseline.id)
            for a_distribution in distributions_records:
                a_distribution_dict = a_distribution.__dict__
                del a_distribution_dict['_sa_instance_state']
                del a_distribution_dict['id']
                del a_distribution_dict['baseline_id']
                request_name = a_distribution_dict.pop('name')
                distributions.append({request_name: a_distribution_dict})

            results['requests'] = requests
            results['distributions'] = distributions

            return {application_name: results,
                    'hach_rate': hatch_rate,
                    'number_of_users': number_of_users,
                    'duration': baseline.duration}
        else:
            return None
    else:
        return None


@app.task(bind=True)
def delete(self,
           application_name,
           number_of_users,
           hatch_rate):
    """
    Delete a performance baseline
    :param application_name: the name of the micro-service
    :param number_of_users: the number of users used in the baseline
    :param hatch_rate: th number of new user to simulate every second
    :return: the id of the baseline deleted
    """
    # create session
    session = db_session()
    bd = BaselinesDal(session)
    try:
        baseline_id = bd.delete(application_name, number_of_users, hatch_rate)
        return baseline_id
    except NoResultFound as e:
        self.update_state(state=states.FAILURE, meta={'exc_type': type(e).__name__,
                                                      'exc_message': traceback.format_exc().split('\n'),
                                                      'message': str(e)})
    raise Ignore()


@app.task(bind=True)
def create(self,
           application_name,
           url,
           number_of_users,
           hatch_rate,
           locust_file,
           duration):
    """
    Create a performance baseline.

    :type application_name: str
    :param application_name: the name of the micro-service

    :type url: str
    :param url: the base url of the micro-service

    :type number_of_users: int
    :param number_of_users: the total count of concurrent users to simulate

    :type locust_file: str
    :param locust_file: the name of the locut file (locustfile_<application_name>.py)

    :type duration: int
    :param duration: the duration of the performance baseline test in seconds.

    :type hatch_rate: int
    :param hatch_rate: the number of users to create every second until total count is reached.
    """
    # create a session
    session = db_session()

    logger.info('Create application {} if it does not already exist.'.format(application_name))
    ad = ApplicationsDal(session)
    app_id = ad.create_if_not_exist(application_name)

    # Create a baseline for a given number of users and a hatch rate
    bd = BaselinesDal(session)
    try:
        if bd.get(app_id, number_of_users, hatch_rate):
            logger.warning('An identical baseline already exit for application {}. Aborting.'.format(
                application_name
            ))
            raise BaselineAlreadyExist('The Baseline for {} with number of users {} and hatch rate {} already exists. '
                                       'Delete it if you want to re-create the baseline.'.format(application_name,
                                                                                                 number_of_users,
                                                                                                 hatch_rate))
    except BaselineAlreadyExist as e:
        self.update_state(state=states.FAILURE, meta={'exc_type': type(e).__name__,
                                                      'exc_message': traceback.format_exc().split('\n'),
                                                      'message': str(e)})
        raise Ignore()
    else:
        logger.info('Create new baseline for application {}'.format(application_name))
        baseline_id = bd.create(app_id, number_of_users, hatch_rate, duration)

    # start locust server
    proc_id = start(application_name, url, number_of_users, hatch_rate, locust_file)
    hatch_duration = int(number_of_users / hatch_rate) + 1
    sleep(hatch_duration + duration)
    stop(proc_id)

    # save locust performance metrics (2 files)
    logger.info('Save request performance and distribution to database.')
    dd = DistributionsDal(session)
    dd.create(baseline_id, csv_file=application_name + '_distribution.csv')
    rd = RequestsDal(session)
    rd.create(baseline_id, csv_file=application_name + '_requests.csv')

    return 'Done'


# @app.task
# def create(application_name,
#            metric_names,
#            metric_values,
#            dt_from,
#            dt_to,
#            summarize):
#     """
#     Create a performance baseline for a particular micro-service API.
#     the baseline is established for the following metrics:
#     - cpu usage (CPU/User/Utilization, in percent)
#     :type  application_name: str
#     :param application_name: the name of the micro-service
#
#     :type metric_names: list of str
#     :param metric_names: the number of concurrent users to simulate.
#
#     :type metric_values: list of str
#     :param metric_values: the number of users who start a session every
#
#     :type dt_from: datetime
#     :param dt_from: the starting date
#
#     :type dt_to: datetime
#     :param dt_to: the ending date
#
#     :type dt_from: datetime
#     :param dt_from: the starting date
#
#     :type summarize: bool
#     :param summarize: summarize the data
#
#     :rtype dict
#     :return:
#     """
#     print("Create performance baseline for application {}".format(application_name))
#     res = chain(application_id_by_name.s(application_name),
#                 metric_data.s(metric_names,
#                               metric_values,
#                               dt_from,
#                               dt_to,
#                               summarize))()
#     return res.get()

if __name__ == '__main__':
    session = db_session()
    # from resources.dao.requests_dao import Request
    # requ = session.query(Request)
    # res = requ.get(1).__dict__
    # del res['_sa_instance_state']
    # print(res)
    # print(json.dumps(res))
    # print(session.query(Request).column_descriptions)

    # from resources.dao.baselines_dao import Baseline
    # baselines = session.query(Baseline).filter(Baseline.application_id == 2).all()
    # for baseline in baselines:
    #     print(baseline)

    from resources.dao.requests_dao import Request

    requs = session.query(Request)
    for req in requs:
        print(req)
