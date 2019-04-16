from locust import HttpLocust, TaskSet, seq_task


class ScoreEngineService(TaskSet):

    head = {"x-app-key": "804c41d8cfd74926185087402f166277",
            "uid": "1206540"}
    country = 'US'
    region = 'IL'
    vcenterId = '168866bf-8390-4d24-b5b2-b57459de6d1a'
    datacenter = 'L4VXR2_DC'
    clusterId = '52f38501-cbc3-d779-683b-c7964870c48e'
    vcParam = '?vcenter_uuid=' + vcenterId
    dcParam = '?data_center=%s&vcenter_uuid=%s' % (datacenter, vcenterId)
    clusterParam = '?cluster_uuid=%s' % clusterId
    countryParam = '?country=%s' % country
    regionParam = '?country=%s&region=%s' % (country, region)

    # One task per page that calls score-engine-service
    # ---------------------All vCenter Servers-----------------------------
    @seq_task(1)
    def logical_all_summary(self):
        self.healthscore_summary('')

    @seq_task(2)
    def logical_all_healthscore(self):
        self.healthscore_history('')
        self.healthscore_summary('')

    @seq_task(3)
    def logical_all_healthscore_issue(self):
        self.healthscore_issues('')

    # ---------------------One vCenter Server-------------------------------
    @seq_task(4)
    def logical_vc_summary(self):
        self.healthscore_summary(self.vcParam)

    @seq_task(5)
    def logical_vc_healthscore(self):
        self.healthscore_history(self.vcParam)
        self.healthscore_summary(self.vcParam)

    @seq_task(6)
    def logical_vc_healthscore_issue(self):
        self.healthscore_issues(self.vcParam)

    # ---------------------One Datacenter-------------------------------------
    @seq_task(7)
    def logical_dc_summary(self):
        self.healthscore_summary(self.dcParam)

    @seq_task(8)
    def logical_dc_healthscore(self):
        self.healthscore_history(self.dcParam)
        self.healthscore_summary(self.dcParam)

    @seq_task(9)
    def logical_dc_healthscore_issue(self):
        self.healthscore_issues(self.dcParam)

    # ----------------------One Cluster---------------------------------------
    @seq_task(10)
    def logical_cluster_summary(self):
        self.healthscore_summary(self.clusterParam)

    @seq_task(11)
    def logical_cluster_healthscore(self):
        self.healthscore_history(self.clusterParam)
        self.healthscore_summary(self.clusterParam)

    @seq_task(12)
    def logical_cluster_healthscore_issue(self):
        self.healthscore_issues(self.clusterParam)
    # The World is same to all vCenter Service

    # -----------------------Country----------------------------------
    @seq_task(13)
    def physical_country_summary(self):
        self.healthscore_summary(self.countryParam)

    @seq_task(14)
    def physical_country_healthscore(self):
        self.healthscore_history(self.countryParam)
        self.healthscore_summary(self.countryParam)

    @seq_task(15)
    def physical_country_healthscore_issue(self):
        self.healthscore_issues(self.countryParam)
    # -----------------------Region---------------------------------
    @seq_task(16)
    def physical_region_summary(self):
        self.healthscore_summary(self.regionParam)

    @seq_task(17)
    def physical_region_healthscore(self):
        self.healthscore_history(self.regionParam)
        self.healthscore_summary(self.regionParam)

    @seq_task(18)
    def physical_region_healthscore_issue(self):
        self.healthscore_issues(self.regionParam)


    # APIs in Score-Engine-Service

    def healthscore_summary(self, params):
        self.sendGetRequest('/api/v1/health_score/summary' + params)

    def healthscore_history(self, params):
        if params != '':
            self.sendGetRequest('/api/v1/health_score/history' + params + '&time_range=2')
        else:
            self.sendGetRequest('/api/v1/health_score/history?time_range=2')

    def healthscore_issues(self, params):
        self.sendGetRequest('/api/v1/health_score/issues' + params)

    # Send get request
    def sendGetRequest(self, path):
        self.client.get(path, headers=self.head)


# Set time interval for every task
class DashboardUserBehavior(HttpLocust):
    task_set = ScoreEngineService
    min_wait = 5000
    max_wait = 9000

