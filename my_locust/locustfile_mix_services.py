from locust import HttpLocust
from locustfile_ui_api_service import UiApiService
from locustfile_score_engine_service import ScoreEngineService
from locustfile_data_metrics_api import DataMetricsService


class UiApiLocust(HttpLocust):
    host = "https://ui-api-service-yolanda.cfd.isus.emc.com"
    task_set = UiApiService
    weight = 280
    min_wait = 5000
    max_wait = 9000


class ScoreEngineLocust(HttpLocust):
    host = "https://score-engine-service-yolanda.cfd.isus.emc.com"
    task_set = ScoreEngineService
    weight = 165
    min_wait = 5000
    max_wait = 9000


class DataMetricsLocust(HttpLocust):
    host = "https://data-metrics-api-yolanda.cfd.isus.emc.com"
    task_set = DataMetricsService
    weight = 55
    min_wait = 5000
    max_wait = 9000
