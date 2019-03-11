import os

from configuration.local_deployment_configuration import LocalDeploymentConfiguration


def get_deployment_configuration():
    expected_envs = ['it', 'prod', 'test', 'stage', 'dev', 'local']
    if 'ENVIRONMENT' not in os.environ:
        raise Exception('define your ENVIRONMENT environment variable')
    else:
        environment = os.getenv('ENVIRONMENT').lower()

    if environment in ['it', 'prod', 'stage', 'dev']:
        print("PCF deployment configuration selected.")
        from configuration.pcf_deployment_configuration import PCFConfig
        return PCFConfig
    elif environment == 'local':
        print("Local deployment selected.")
        return LocalDeploymentConfiguration
    else:
        raise Exception('environment type must be in {}'.format(expected_envs))