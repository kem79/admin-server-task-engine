from sqlalchemy.orm.exc import NoResultFound

from resources.dao.backend_metrics_dao import BackendMetric


class BackendMetricsDal:

    def __init__(self, session):
        self.session = session

    def create(self, baseline_id, results, start_time, end_time):
        """
        Store new relic application performance metrics into database

        :type results: dict
        :param results: a dict containing the performance metrics collected from new relic.

        :type baseline_id: int
        :param baseline_id: the id of the baseline

        :type start_time: date
        :param start_time: the staring date of the peformance baseline test

        :type end_time: date
        :param end_time: the end date of the performance test baseline

        :rtype int
        :return: the id of the record created in database
        """
        backend_perf = BackendMetric(average_cpu_usage=results['avg_cpu_usage'],
                                     average_memory_usage=results['avg_memory_usage'],
                                     average_response_time=results['avg_response_time'],
                                     start_time=start_time,
                                     end_time=end_time,
                                     baseline_id=baseline_id)
        self.session.add(backend_perf)
        self.session.commit()
        return backend_perf.id

    def get_by_baseline_id(self, baseline_id):
        try:
            backend_perf_metrics = self.session.query(BackendMetric).filter(
                BackendMetric.baseline_id == baseline_id).one()
            return backend_perf_metrics
        except NoResultFound:
            return None