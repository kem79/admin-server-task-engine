from app.task_engine import app
from my_new_relic import application_id_by_name, metric_data
from my_locust.tasks import start, stop

from resources import ApplicationsDal, DistributionsDal, BaselinesDal, RequestsDal

from celery import chain
from time import sleep

@app.task
def create_locust(application_name,
                  url,
                  number_of_users,
                  hatch_rate):
    """
    Create a performance baseline.

    :type application_name: str
    :param application_name: the name of the micro-service

    :type url: str
    :param url: the base url of the micro-service

    :type number_of_users: int
    :param number_of_users: the total count of concurrent users to simulate

    :type hatch_rate: int
    :param hatch_rate: the number of users to create every second until total count is reached.
    """
    # start locust server
    proc_id = start(application_name, url, number_of_users, hatch_rate)
    experience_total_time = int(number_of_users/hatch_rate) + 1
    sleep(experience_total_time*3)
    stop(proc_id)

    # verify the micro-service name is in database, if not create it.
    ad = ApplicationsDal()
    app_id = ad.create_if_not_exist(application_name)

    # Create a baseline for a given number of users and a hatch rate
    bd = BaselinesDal()
    baseline_id = bd.create(app_id, number_of_users, hatch_rate)

    # save locust performance metrics (2 files)
    dd = DistributionsDal()
    dd.create(baseline_id, csv_file=application_name + '_distribution.csv')
    rd = RequestsDal()
    rd.create(baseline_id, csv_file=application_name + '_requests.csv')

    return 'Done'


@app.task
def create(application_name,
           metric_names,
           metric_values,
           dt_from,
           dt_to,
           summarize):
    """
    Create a performance baseline for a particular micro-service API.
    the baseline is established for the following metrics:
    - cpu usage (CPU/User/Utilization, in percent)
    :type  application_name: str
    :param application_name: the name of the micro-service

    :type metric_names: list of str
    :param metric_names: the number of concurrent users to simulate.

    :type metric_values: list of str
    :param metric_values: the number of users who start a session every

    :type dt_from: datetime
    :param dt_from: the starting date

    :type dt_to: datetime
    :param dt_to: the ending date

    :type dt_from: datetime
    :param dt_from: the starting date

    :type summarize: bool
    :param summarize: summarize the data

    :rtype dict
    :return:
    """
    print("Create performance baseline for application {}".format(application_name))
    res = chain(application_id_by_name.s(application_name),
                metric_data.s(metric_names,
                              metric_values,
                              dt_from,
                              dt_to,
                              summarize))()
    return res.get()
