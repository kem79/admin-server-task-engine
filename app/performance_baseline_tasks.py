import json
import os
import traceback

from celery import states
from newrelic_api.exceptions import NewRelicAPIServerException
from sqlalchemy.orm.exc import NoResultFound

from app.task_engine import app
from app import db_session
from my_new_relic.applications_facade import ApplicationFacade
from my_locust.tasks import start, stop

import resources

from time import sleep
from celery.utils.log import get_task_logger
from exceptions.admin_server_exceptions import BaselineAlreadyExist, ApplicationDoesNotExist
from celery.exceptions import Ignore
from datetime import datetime
import logging
from logging import INFO
import sys

from resources import BackendMetricsDal

logger = get_task_logger(__name__)
h = logging.StreamHandler(sys.stdout)
h.setLevel(os.getenv('LOG_LEVEL', INFO))
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
h.setFormatter(formatter)
logger.addHandler(h)

@app.task
def get_all(application_name):
    """
    Return all the baselines for a given application
    :param application_name: the name of the micro-service
    :return: 
    """
    session = db_session()
    try:
        ad = resources.ApplicationsDal(session)
        application = ad.get(application_name)
        if application:
            bd = resources.BaselinesDal(session)
            baselines = bd.get_all(application_id=application.id)
            session.close()
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
    finally:
        session.close()


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
    try:
        ad = resources.ApplicationsDal(session)
        application = ad.get(application_name)
        if application:
            bd = resources.BaselinesDal(session)
            baseline = bd.get(application.id, number_of_users, hatch_rate)
            if baseline:
                results = {'requests': None,
                           'distributions': None,
                           'backend': None}
                requests = []
                distributions = []

                rd = resources.RequestsDal(session)
                requests_performance = rd.get_by_baseline_id(baseline.id)
                for one_request_type in requests_performance:
                    one_request_type_dict = one_request_type.__dict__
                    del one_request_type_dict['_sa_instance_state']
                    del one_request_type_dict['id']
                    del one_request_type_dict['baseline_id']
                    request_method = one_request_type_dict.pop('method')
                    request_method_name = one_request_type_dict.pop('name')
                    requests.append({request_method: {request_method_name: one_request_type_dict}})

                dd = resources.DistributionsDal(session)
                distributions_records = dd.get_by_baseline_id(baseline.id)
                for a_distribution in distributions_records:
                    a_distribution_dict = a_distribution.__dict__
                    del a_distribution_dict['_sa_instance_state']
                    del a_distribution_dict['id']
                    del a_distribution_dict['baseline_id']
                    request_name = a_distribution_dict.pop('name')
                    distributions.append({request_name: a_distribution_dict})

                bmd = resources.BackendMetricsDal(session)
                backend_metrics_record = bmd.get_by_baseline_id(baseline.id).__dict__
                del backend_metrics_record['_sa_instance_state']
                del backend_metrics_record['id']
                del backend_metrics_record['baseline_id']

                results['requests'] = requests
                results['distributions'] = distributions
                results['backend'] = backend_metrics_record

                return {application_name: results,
                        'hach_rate': hatch_rate,
                        'number_of_users': number_of_users,
                        'duration': baseline.duration}
            else:
                return None
        else:
            return None
    finally:
        session.close()


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
    try:
        bd = resources.BaselinesDal(session)
        try:
            baseline_id = bd.delete(application_name, number_of_users, hatch_rate)
            session.close()
            return baseline_id
        except NoResultFound as e:
            self.update_state(state=states.FAILURE, meta={'exc_type': type(e).__name__,
                                                          'exc_message': traceback.format_exc().split('\n'),
                                                          'message': str(e)})
        raise Ignore()
    finally:
        session.close()


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
    try:
        logger.debug('Create application {} if it does not already exist.'.format(application_name))
        ad = resources.ApplicationsDal(session)
        app_id = ad.create_if_not_exist(application_name)

        # Create a baseline for a given number of users and a hatch rate
        bd = resources.BaselinesDal(session)
        try:
            if bd.get(app_id, number_of_users, hatch_rate):
                logger.error('An identical baseline already exit for application {}. Aborting.'.format(
                    application_name
                ))
                raise BaselineAlreadyExist(
                    'The Baseline for {} with number of users {} and hatch rate {} already exists. '
                    'Delete it if you want to re-create the baseline.'.format(application_name,
                                                                              number_of_users,
                                                                              hatch_rate))
        except BaselineAlreadyExist as e:
            session.rollback()
            self.update_state(state=states.FAILURE, meta={'exc_type': type(e).__name__,
                                                          'exc_message': traceback.format_exc().split('\n'),
                                                          'message': str(e)})
            raise Ignore()
        else:
            baseline_id = bd.create(app_id, number_of_users, hatch_rate, duration)

        # start locust server
        start_time = datetime.strftime(datetime.utcnow(), '%Y-%m-%dT%H:%M:00')
        proc_id = start(application_name, url, number_of_users, hatch_rate, locust_file)
        hatch_duration = int(number_of_users / hatch_rate) + 1
        sleep(hatch_duration + duration)
        end_time = datetime.strftime(datetime.utcnow(), '%Y-%m-%dT%H:%M:00')
        stop(proc_id)

        # # save locust performance metrics (2 files)
        logger.debug('Save request performance and distribution to database.')
        dd = resources.DistributionsDal(session)
        dd.create(baseline_id, csv_file=application_name + '_distribution.csv')
        rd = resources.RequestsDal(session)
        rd.create(baseline_id, csv_file=application_name + '_requests.csv')

        # # # save app backend metrics from new relic
        nr_apps_facade = ApplicationFacade()
        app_id = nr_apps_facade.application_id_by_name(application_name)
        logger.debug('Collect backend metrics for time interval [{}, {}]'.format(start_time, end_time))
        res = nr_apps_facade.collect_backend_performance_metrics(app_id,
                                                                 start_time,
                                                                 end_time)
        logger.debug('New Relic metrics for {}:\n{}'.format(application_name,
                                                            json.dumps(res, indent=2)))
        bed = BackendMetricsDal(session)
        bed.create(baseline_id,
                   res,
                   datetime.strptime(start_time, '%Y-%m-%dT%H:%M:00'),
                   datetime.strptime(end_time, '%Y-%m-%dT%H:%M:00'))

        logger.info('Created new baseline for application {}.'.format(application_name))
        return 'Done'
    except ApplicationDoesNotExist:
        logger.exception('Application name {} is not present in New Relic. Verify your monitoring setup.'.format(application_name))
    except NewRelicAPIServerException:
        logger.exception('There was a problem when trying to collect performance data from New Relic.')
    finally:
        session.close()

