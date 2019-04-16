from locust import HttpLocust, TaskSet, seq_task


class DataMetricsService(TaskSet):

    head = {"x-app-key": "804c41d8cfd74926185087402f166277",
            "uid": "1206540"}
    vcenterId = '168866bf-8390-4d24-b5b2-b57459de6d1a'
    datacenter = 'L4VXR2_DC'
    clusterId = '52f38501-cbc3-d779-683b-c7964870c48e'
    hostId = '4c4c4544-004a-3510-8036-c4c04f485132'
    dcParam = '?data_center=%s&vcenter_uuid=%s' % (datacenter, vcenterId)
    clusterParam = '?cluster_uuid=%s' % clusterId
    clusterParam4usage = '?cluster_uuid=5242fd84-1c73-2279-38aa-f5d2020e6f64'

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
        metricType = 'cpu,mem,disk,net'
        # Time range is 24 hours as UI default
        fromTime = '1554862256241'
        toTime = '1554948656241'
        self.sendGetRequest('/api/v1/hosts/performance/summary%s&metric_type=%s&from_timestamp=%s&to_timestamp=%s'
                            % (params, metricType, fromTime, toTime))

    def hosts_performance_details(self, params):
        metricType = 'cpu,mem,disk,net'
        # Time range is 24 hours as UI default
        fromTime = '1554862256241'
        toTime = '1554948656241'
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

