from app.task_engine import app
from base_tasks.new_relic import application_id_by_name, metric_data

from celery import chain


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
    return res
