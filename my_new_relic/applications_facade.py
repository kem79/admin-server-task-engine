from my_new_relic.new_relic_base_task import NewRelicBase
from newrelic_api import Applications
from exceptions.admin_server_exceptions import ApplicationDoesNotExist


class ApplicationFacade(NewRelicBase):

    def application_id_by_name(self, name):
        """
        Return the New Relic application Id given the application name
        :type str
        :param name: the name of the application, for instance "data-storage-mongo-prod"

        :rtype int
        :return: the id of the application in New Relic database. Return None if no application was found.
        """
        print('Retrieve application {} id...'.format(name))
        nr_apps = Applications(self.api_key)

        applications = nr_apps.list(filter_name=name)
        if 'applications' in applications.keys() and applications['applications']:
            app_ids = [app['id'] for app in applications['applications'] if app['name'] == name]
            if len(app_ids) == 1:
                return int(app_ids[0])
        raise ApplicationDoesNotExist('Application {} does not exist in New Relic.'.format(name))

    def collect_backend_performance_metrics(self,
                                            application_id,
                                            from_time=None,
                                            to_time=None):
        """
        This methods collects the backend performance metrics of a micro-service
        Right now, it collects:
        - average memory usage for the entire application (as opposed to one single instance)
        - average CPU usage for the entire application
        - average response time including database and external calls

        :type application_id: int
        :param application_id: the application id in New Relic

        :type from_time: date
        :param from_time: start time

        :type to_time: date
        :param to_time: end date

        :rtype: dict
        :return: a dict with average mem, cpu, response time
        """
        app_metrics = self._metric_data(application_id,
                                        from_datetime=from_time,
                                        to_datetime=to_time,
                                        metric_names=['Memory/Physical',
                                                      'CPU/User Time',
                                                      'WebTransactionTotalTime'],
                                        metric_values=['total_used_mb',
                                                       'percent',
                                                       'average_response_time',
                                                       'min_response_time',
                                                       'max_response_time'])
        mem_values = [value['values']['total_used_mb']
                      for value in
                      [metric['timeslices']
                       for metric in app_metrics['metric_data']['metrics']
                       if metric['name'] == 'Memory/Physical'][0]
                      ]
        cpu_values = [value['values']['percent']
                      for value in
                      [metric['timeslices']
                       for metric in app_metrics['metric_data']['metrics']
                       if metric['name'] == 'CPU/User Time'][0]
                      ]
        resp_time_values = [value['values']['average_response_time']
                            for value in
                            [metric['timeslices']
                             for metric in app_metrics['metric_data']['metrics']
                             if metric['name'] == 'WebTransactionTotalTime'][0]
                            ]

        return {
                    'avg_memory_usage': sum(mem_values) / len(mem_values),
                    'avg_cpu_usage': sum(cpu_values) / len(cpu_values),
                    'avg_response_time': sum(resp_time_values) / len(resp_time_values)
                }

    def _metric_data(self,
                     application_id,
                     metric_names,
                     metric_values,
                     from_datetime=None,
                     to_datetime=None,
                     summarize=False
                     ):
        """
        Retrieve metric data from new relic.

        :type  application_id: int
        :param application_id: the micro-service id in new relic.

        :type  metric_names: list of str
        :param metric_names: the name of metric to get values for.

        :type  metric_values: list of str
        :param metric_values: the values to retrieve for the metric names

        :type  from_datetime: date
        :param from_datetime: the starting timestamp

        :type: to_datetime: date
        :param to_datetime: the ending timestamp

        :type   summarize: bool
        :param summarize: summarize the data

        :rtype dict
        :return: a JSON representing the metrics data.
        """
        nr_apps = Applications(self.api_key)
        print('Collect metrics data for application id {}.'.format(application_id))
        response = nr_apps.metric_data(application_id,
                                       metric_names,
                                       metric_values,
                                       from_datetime,
                                       to_datetime,
                                       summarize)
        return response


if __name__ == '__main__':
    s = ApplicationFacade()
    mem, cpu, resp_time = s.collect_backend_performance_metrics(178825455,
                                                                '2019-04-01T8:00:00',
                                                                '2019-04-01T8:30:00')

    print('average mem usage in mb: {:.2f}'.format(mem))
    print('average cpu usage in %: {:.2f}'.format(cpu))
    print('average response time usage in ms: {:.2f}'.format(resp_time))

    # print(datetime.utcnow().strftime('%Y:%m:%dT%H:%M:%S %Z'))
