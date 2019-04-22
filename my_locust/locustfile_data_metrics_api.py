

from locust import HttpLocust, TaskSet, task, seq_task

class DataMetricsService(TaskSet):

    head = {"x-app-key": "804c41d8cfd74926185087402f166277",
            "uid": "1206540"}
    vcenterId = '27cf6667-26df-4c72-9d32-424bbca30b09'
    datacenter = 'VxRail-Datacenter'
    clusterId = '522dfb0c-20cc-d2f9-9849-0c18707289b4'
    hostId = '8c7c8df8-7c53-1000-8d6b-54ab3a70aa76'
    dcParam = '?data_center=%s&vcenter_uuid=%s' % (datacenter, vcenterId)
    clusterParam = '?cluster_uuid=%s' % clusterId
    clusterParam4usage = '?cluster_uuid=522dfb0c-20cc-d2f9-9849-0c18707289b4'

    # One task per page that calls data-metrics-service

    # -----------------------One Datacenter-------------------------------------
    @seq_task(1)
    def logical_dc_performance(self):
        self.hosts_performance_summary(self.dcParam)

    # -----------------------One Cluster---------------------------------------
    @seq_task(2)
    def logical_cluster_storage(self):
        self.storage_usage_prediction(self.clusterParam4usage)

    @seq_task(3)
    def logical_cluster_performance(self):
        self.hosts_performance_summary(self.clusterParam)

    @seq_task(4)
    def logical_cluster_performance_detail(self):
        self.hosts_performance_details(self.clusterParam)


    # APIs in Data-Metrics-Service
    def storage_usage_prediction(self, params):
        self.sendGetRequest('/api/v1/storage/usage_prediction' + params)

    def hosts_performance_summary(self, params):
        metricType = 'cpu%2Cmem%2Cdisk%2Cnet'
        # Time range is 24 hours as UI default
        fromTime = '1555904860148'
        toTime = '1555912060149'
        self.sendGetRequest('/api/v1/hosts/performance/summary%s&metric_type=%s&from_timestamp=%s&to_timestamp=%s'
                            % (params, metricType, fromTime, toTime))

    def hosts_performance_details(self, params):
        metricType = 'cpu%2Cmem%2Cdisk%2Cnet'
        # Time range is 24 hours as UI default
        fromTime = '1555904860148'
        toTime = '1555912060149'
        self.sendGetRequest('/api/v1/hosts/performance/details%s&host_uuid=%s&from_timestamp=%s&to_timestamp=%s&metric_type=%s&%s'
                            % (params, self.hostId, fromTime, toTime, metricType, 'show_anomalies=true'))

    # Send Get request
    def sendGetRequest(self, path):
        self.client.get(path, headers=self.head)


# Set time interval for every task
class DashboardUserBehavior(HttpLocust):
    task_set = DataMetricsService
    min_wait = 5000
    max_wait = 9000

