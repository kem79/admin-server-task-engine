from locust import HttpLocust
from locustfile_third_party import ThirdPartyService
from locustfile_management_view_api import ManagementViewApiService
from locustfile_ui_api_service_geo_topo import GetGeoTopology


# class ThirdPartyServiceLocust(HttpLocust):
#     host = "https://third-party-api-marc.cfd.isus.emc.com"
#     task_set = ThirdPartyService
#     weight = 4
#     min_wait = 5000
#     max_wait = 9000


class ManagementViewApiLocust(HttpLocust):
    host = "https://management-view-api-marc.cfd.isus.emc.com"
    task_set = ManagementViewApiService
    weight = 4
    min_wait = 5000
    max_wait = 9000


class GetGeoTopologyBehavior(HttpLocust):
    host = "https://ui-api-service-marc.cfd.isus.emc.com"
    task_set = GetGeoTopology
    weight = 1
    min_wait = 5000
    max_wait = 9000



