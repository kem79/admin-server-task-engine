from locust import HttpLocust, TaskSet, task


class BashboardBehavior(TaskSet):

    # @task(1)
    # def info(self):
    #     self.client.get('/api/v1/entities?psnt=FNP5YK20000000',
    #                     headers={'x-app-key': '804c41d8cfd74926185087402f166277',
    #                              'uid': '1075884'})

    # ----------------- Dashboard ------------------ #
    # @task(1)
    # def get_all_countries_dashboard(self):
    #     self.client.get('/api/v1/dashboard/overview?country=all')
    #
    @task(1)
    def get_us_dashboard(self):
        self.client.get('/api/v1/dashboard/overview?country=US',
                        headers={'x-app-key': '804c41d8cfd74926185087402f166277',
                                 'uid': '1143052'})

    #
    # @task(1)
    # def get_cluster_list(self):
    #     self.client.get('/api/v1/dashboard/clusterlist?country=US&region=CA')

    @task(1)
    def get_topology(self):
        self.client.get('/api/v1/dashboard/vcenterview/topology',
                        headers={'x-app-key': '804c41d8cfd74926185087402f166277',
                                 'uid': '1075884'})

    # @task(1)
    # def get_vcenter_view(self):
    #     vcuuid = '9375b7cc-d823-11e8-9f8b-f2801f1b9fd1'
    #     dcname = 'VxRail-Datacenter'
    #     clusteruuid = '52f30881-9af2-6f4a-a509-ad23c3ddf1d3'
    #     self.client.get('/dashboard/vcenterview/overview?vcuuid={}&dcname={}&clusteruuid={}'.format(
    #         vcuuid,
    #         dcname,
    #         clusteruuid
    #     ))

    # @task(1)
    # def get_vcenter_listview(self):
    #     vcuuid = '9375b7cc-d823-11e8-9f8b-f2801f1b9fd1'
    #     dcname = 'VxRail-Datacenter'
    #     self.client.get('/dashboard/vcenterview/listview?vcuuid={}&dcname={}'.format(vcuuid,
    #                                                                                  dcname))
    # @task(1)
    # def get_region_cluster_list(self):
    #     self.client.get('/dashboard/region-clusterlist?country=US&region=CA')


class DashboardUserBehavior(HttpLocust):
    task_set = BashboardBehavior
    min_wait = 5000
    max_wait = 9000
