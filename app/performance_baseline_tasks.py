import json

from app.task_engine import app
from app import db_session
from my_locust.tasks import start, stop

from resources import ApplicationsDal, DistributionsDal, BaselinesDal, RequestsDal

from time import sleep


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
            results = {}
            rd = RequestsDal(session)
            requests_performance = rd.get_by_baseline_id(baseline.id)
            for one_request_type in requests_performance:
                one_request_type_dict = one_request_type.__dict__
                del one_request_type_dict['_sa_instance_state']
                del one_request_type_dict['id']
                del one_request_type_dict['baseline_id']
                request_method = one_request_type_dict.pop('method')
                request_method_name = one_request_type_dict.pop('name')
                results[request_method] = {request_method_name: one_request_type_dict}
            return results
        else:
            return None
    else:
        return None


@app.task
def delete(application_name,
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
    baseline_id = bd.delete(application_name, number_of_users, hatch_rate)
    return baseline_id


@app.task
def create(application_name,
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
    # create a session
    session = db_session()

    # start locust server
    proc_id = start(application_name, url, number_of_users, hatch_rate)
    experience_total_time = int(number_of_users/hatch_rate) + 1
    sleep(experience_total_time*3)
    stop(proc_id)

    # verify the micro-service name is in database, if not create it.
    ad = ApplicationsDal(session)
    app_id = ad.create_if_not_exist(application_name)

    # Create a baseline for a given number of users and a hatch rate
    bd = BaselinesDal(session)
    baseline_id = bd.create(app_id, number_of_users, hatch_rate)

    # save locust performance metrics (2 files)
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
    from resources.dao.requests_dao import Request
    requ = session.query(Request)
    res = requ.get(1).__dict__
    del res['_sa_instance_state']
    print(res)
    print(json.dumps(res))
    # print(session.query(Request).column_descriptions)
