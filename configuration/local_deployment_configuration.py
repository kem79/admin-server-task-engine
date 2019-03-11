"""
a Configuration to work with rails-ai-service-appliance
"""
from configuration.base_deployment_configuration import _BaseDeploymentConfiguration


class LocalDeploymentConfiguration(_BaseDeploymentConfiguration):
    broker_url = 'pyamqp://guest@192.168.99.100//'
    result_backend = 'redis://192.168.99.100'
