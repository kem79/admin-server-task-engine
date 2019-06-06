from locust import HttpLocust, TaskSet, task


class GetGeoTopology(TaskSet):

    head = {"x-app-key": "804c41d8cfd74926185087402f166277",
            "uid": "1206540"}

    @task
    def get_geo_topology(self):
        self.client.get('/api/v1/geo_topology/summary', headers=self.head)


