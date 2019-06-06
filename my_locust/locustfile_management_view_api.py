from locust import task, TaskSet
import random
from random import choice


class ManagementViewApiService(TaskSet):
    # exercise health-tree collection
    head = {"x-app-key": "804c41d8cfd74926185087402f166277",
            "uid": "1206540"}

    @task
    def get_nodes_by_country(self):
        self.client.get('/api/v1/nodes?month={}'.format(self.random_month_and_year()),
                        headers=self.head)

    @task
    def get_nodes_by_state(self):
        country = 'United States'
        self.client.get('/api/v1/nodes/{}?month={}'.format(country,
                                                           self.random_month_and_year()),
                        headers=self.head)

    @classmethod
    def random_month_and_year(cls):
        year = choice([2018, 2019])
        if year == 2018:
            month = str(random.randint(1, 12)).zfill(2)
        else:
            month = str(random.randint(1, 5)).zfill(2)
        return '{}-{}'.format(year, month)
