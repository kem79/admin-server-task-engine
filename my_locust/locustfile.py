from locust import HttpLocust, TaskSet, task


class UserBehavior(TaskSet):

    # @task(1)
    # def info(self):
    #     self.client.get('/api/v1/entities?psnt=FNP5YK20000000',
    #                     headers={'x-app-key': '804c41d8cfd74926185087402f166277',
    #                              'uid': '1075884'})

    @task(1)
    def info(self):
        self.client.get('/api/v1/info')


class WebSiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000