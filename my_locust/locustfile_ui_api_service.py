

from locust import HttpLocust, TaskSet, task, seq_task


class UiApiService(TaskSet):

    head = {"x-app-key": "804c41d8cfd74926185087402f166277",
            "uid": "1206540"}
    country = 'US'
    region = 'IL'
    vcenterId = '168866bf-8390-4d24-b5b2-b57459de6d1a'
    datacenter = 'L4VXR2_DC'
    clusterId = '52f38501-cbc3-d779-683b-c7964870c48e'
    vcParam = '?vcenter_uuid=' + vcenterId
    dcParam = '?data_center=%s&vcenter_uuid=%s' % (datacenter, vcenterId)
    clusterParam = '?cluster=%s' % clusterId
    countryParam = '?country=%s' % country
    regionParam = '?country=%s&region=%s' % (country, region)

    # One task per page that calls UI-API-service
    # ---------------------All vCenter Servers-----------------------------
    @seq_task(1)
    def logical_all_summary(self):
        self.vcenter_topology('')
        self.inventory_summary('')
        self.alarms_summary('')
        self.storage_usage('')
        self.vms_summary('')

    @seq_task(2)
    def logical_all_healthscore(self):
        self.inventory_summary('')

    @seq_task(3)
    def logical_all_alarms(self):
        self.alarms('')

    @seq_task(4)
    def logical_all_storage(self):
        self.storage_usage('')

    @seq_task(5)
    def logical_all_vms(self):
        self.vms_summary('')
        self.vms('')

    # ----------------------One vCenter Server-------------------------------
    @seq_task(6)
    def logical_vc_summary(self):
        self.inventory_summary(self.vcParam)
        self.alarms_summary(self.vcParam)
        self.storage_usage(self.vcParam)
        self.vms_summary(self.vcParam)

    @seq_task(7)
    def logical_vc_healthscore(self):
        self.inventory_summary(self.vcParam)

    @seq_task(8)
    def logical_vc_alarms(self):
        self.alarms(self.vcParam)

    @seq_task(9)
    def logical_vc_storage(self):
        self.storage_usage(self.vcParam)

    @seq_task(10)
    def logical_vc_vms(self):
        self.vms_summary(self.vcParam)
        self.vms(self.vcParam)

    # ---------------------One Datacenter-------------------------------------
    @seq_task(11)
    def logical_dc_summary(self):
        self.inventory_summary(self.dcParam)
        self.alarms_summary(self.dcParam)
        self.storage_usage(self.dcParam)
        self.vms_summary(self.dcParam)

    @seq_task(12)
    def logical_dc_healthscore(self):
        self.inventory_summary(self.dcParam)

    @seq_task(13)
    def logical_dc_alarms(self):
        self.alarms(self.dcParam)

    @seq_task(14)
    def logical_dc_storage(self):
        self.storage_usage(self.dcParam)

    @seq_task(15)
    def logical_dc_vms(self):
        self.vms_summary(self.dcParam)
        self.vms(self.dcParam)

    # ----------------------One Cluster---------------------------------------
    @seq_task(16)
    def logical_cluster_summary(self):
        self.inventory(self.clusterParam)
        self.inventory_summary(self.clusterParam)
        self.alarms_summary(self.clusterParam)
        self.storage_usage(self.clusterParam)
        self.vms_summary(self.clusterParam)

    @seq_task(17)
    def logical_cluster_healthscore(self):
        self.inventory_summary(self.clusterParam)

    @seq_task(18)
    def logical_cluster_alarms(self):
        self.alarms(self.clusterParam)

    @seq_task(19)
    def logical_cluster_storage(self):
        self.storage_usage(self.clusterParam)

    @seq_task(20)
    def logical_cluster_vms(self):
        self.vms_summary(self.clusterParam)
        self.vms(self.clusterParam)

    @seq_task(21)
    def logical_cluster_inventory(self):
        self.inventory(self.clusterParam)
    # ----------------------The World--------------------------------
    @seq_task(22)
    def physical_world_summary(self):
        self.geo_topology_summary('')
        self.inventory_summary('')
        self.alarms_summary('')
        self.storage_usage('')
        self.vms_summary('')
    #   Healthscore, Alarms, Storage, Vms requests are same to logic view

    # -----------------------Country----------------------------------
    @seq_task(23)
    def physical_country_summary(self):
        self.inventory_summary(self.countryParam)
        self.alarms_summary(self.countryParam)
        self.storage_usage(self.countryParam)
        self.vms_summary(self.countryParam)

    @seq_task(24)
    def physical_country_healthscore(self):
        self.inventory_summary(self.countryParam)

    @seq_task(25)
    def physical_country_alarms(self):
        self.alarms(self.countryParam)

    @seq_task(26)
    def physical_country_storage(self):
        self.storage_usage(self.countryParam)

    @seq_task(27)
    def physical_country_vms(self):
        self.vms_summary(self.countryParam)
        self.vms(self.countryParam)

    # -----------------------Region---------------------------------
    @seq_task(28)
    def physical_region_summary(self):
        self.inventory_summary(self.regionParam)
        self.alarms_summary(self.regionParam)
        self.storage_usage(self.regionParam)
        self.vms_summary(self.regionParam)

    @seq_task(29)
    def physical_region_healthscore(self):
        self.inventory_summary(self.regionParam)

    @seq_task(30)
    def physical_region_alarms(self):
        self.alarms(self.regionParam)

    @seq_task(31)
    def physical_region_storage(self):
        self.storage_usage(self.regionParam)

    @seq_task(32)
    def physical_region_vms(self):
        self.vms_summary(self.regionParam)
        self.vms(self.regionParam)


    # APIs in UI-API-Service

    def vcenter_topology(self, params):
        self.sendGetRequest('/api/v1/vcenter_topology' + params)

    def geo_topology_summary(self, params):
        self.sendGetRequest('/api/v1/geo_topology/summary' + params)

    def hosts_summary(self, params):
        self.sendGetRequest('/api/v1/hosts/summary' + params)

    def vms(self, params):
        self.sendGetRequest('/api/v1/vms' + params)

    def vms_summary(self, params):
        self.sendGetRequest('/api/v1/vms/summary' + params)

    def storage_usage(self, params):
        self.sendGetRequest('/api/v1/storage/usage' + params)

    def inventory(self, params):
        self.sendGetRequest('/api/v1/inventory' + params)

    def inventory_summary(self, params):
        self.sendGetRequest('/api/v1/inventory/summary' + params)

    def alarms(self, params):
        self.sendGetRequest('/api/v1/alarms' + params)

    def alarms_summary(self, params):
        self.sendGetRequest('/api/v1/alarms/summary' + params)

    # Send get request
    def sendGetRequest(self, path):
        self.client.get(path, headers=self.head)


# Set time interval for every task
class DashboardUserBehavior(HttpLocust):
    task_set = UiApiService
    min_wait = 5000
    max_wait = 9000

