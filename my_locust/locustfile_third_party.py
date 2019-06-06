from locust import TaskSet, task
from datetime import datetime, timedelta
import random


class ThirdPartyService(TaskSet):
    # exercise telemetry collection
    end = datetime.now()
    end_date = datetime.strftime(end, '%Y-%m-%d')
    head = {"x-app-key": "804c41d8cfd74926185087402f166277",
            "uid": "1206540"}

    @task
    def get_all_psnt(self):
        self.client.get('/api/v1/psnt-versions?all=true&start_date={}&end_date={}'.format(
            self.random_start(self.end),
            self.end_date),
            headers=self.head)

    @task
    def get_psnt(self):
        self.client.get('/api/v1/psnt-versions',headers=self.head)

    @task
    def get_latest_psnt(self):
        self.client.get('/api/v1/psnt-versions?start_date={}&end_date={}'.format(
            self.random_start(self.end),
            self.end_date),
            headers=self.head)

    @staticmethod
    def random_start(end):
        start = end - timedelta(days=random.randint(1, 24) * 30)
        return datetime.strftime(start, '%Y-%m-%d')
