import json
import os
import base64

from configuration.base_deployment_configuration import _BaseDeploymentConfiguration


def redis_uri():
    backend_service = [service
                       for service in json.loads(os.getenv('VCAP_SERVICES'))['user-provided']
                       if service['name'] == os.getenv('BACKEND_NAME')][0]

    return 'redis://:{password}@{hostname}'.format(
        password=base64.b64decode(backend_service['credentials']['REDIS_PASSWORD']).decode('utf-8'),
        hostname=backend_service['credentials']['REDIS_SERVER_URL'],
    )


def rabbitmq_uri():
    broker_service_uri = [service['credentials']['protocols']['amqp']['uri']
                          for service in json.loads(os.getenv('VCAP_SERVICES'))['p-rabbitmq']
                          if service['name'] == os.getenv('BROKER_NAME')][0]
    return broker_service_uri


def postgres_uri():
    pg_uri = [service['credentials']['uri']
              for service in json.loads(os.getenv('VCAP_SERVICES'))['credhub']
              if service['name'] == os.getenv('POSTGRES_CREDS_NAME')][0]
    return pg_uri


class PCFConfig(_BaseDeploymentConfiguration):
    broker_url = rabbitmq_uri()
    result_backend = redis_uri()
    postgres_url = postgres_uri()
