from app.task_engine import app
from my_new_relic.new_relic_base_task import NewRelicBaseTask
from newrelic_api.applications import Applications


@app.task(base=NewRelicBaseTask)
def application_id_by_name(name):
    """
    Return the New Relic application Id given the application name
    :type str
    :param name: the name of the application, for instance "data-storage-mongo-prod"

    :rtype int
    :return: the id of the application in New Relic database. Return None if no application was found.
    """
    print('Retrieve application {} id...'.format(name))
    nr_apps = Applications(application_id_by_name.api_key)

    applications = nr_apps.list(filter_name=name)
    if 'applications' in applications.keys() and applications['applications']:
        app_ids = [app['id'] for app in applications['applications'] if app['name'] == name]
        if len(app_ids) == 1:
            return int(app_ids[0])
    return None


@app.task(base=NewRelicBaseTask)
def metric_data(application_id,
                metric_names,
                metric_values,
                from_timestamp,
                to_timestamp,
                summarize
                ):
    """
    Retrieve metric data from new relic.

    :type  application_id: int
    :param application_id: the micro-service id in new relic.

    :type  metric_names: list of str
    :param metric_names: the name of metric to get values for.

    :type  metric_values: list of str
    :param metric_values: the values to retrieve for the metric names

    :type  from_timestamp: datetime
    :param from_timestamp: the starting timestamp

    :type: to_timestamp: datetime
    :param to_timestamp: the ending timestamp

    :type   summarize: bool
    :param summarize: summarize the data

    :rtype dict
    :return: a JSON representing the metrics data.
    """
    nr_apps = Applications(metric_data.api_key)
    print('Collect metrics data for application id {}.'.format(application_id))
    response = nr_apps.metric_data(application_id,
                                   metric_names,
                                   metric_values,
                                   from_timestamp,
                                   to_timestamp,
                                   summarize)
    return response
