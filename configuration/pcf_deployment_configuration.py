import json
import os

from configuration.base_deployment_configuration import _BaseDeploymentConfiguration


def redis_uri():
    backend_service = [service
                       for service in json.loads(os.getenv('VCAP_SERVICES'))['p-redis']
                       if service['name'] == os.getenv('BACKEND_NAME')][0]

    return 'redis://:{password}@{hostname}:{port}'.format(
        password=backend_service['credentials']['password'],
        hostname=backend_service['credentials']['host'],
        port=backend_service['credentials']['port']
    )


def rabbitmq_uri():
    broker_service_uri = [service['credentials']['protocols']['amqp']['uri']
                          for service in json.loads(os.getenv('VCAP_SERVICES'))['p-rabbitmq']
                          if service['name'] == os.getenv('BROKER_NAME')][0]
    return broker_service_uri


class PCFConfig(_BaseDeploymentConfiguration):
    broker_url = rabbitmq_uri()
    result_backend = redis_uri()