from celery import Celery

from configuration import deployment_configuration

app = Celery('railai-admin-server-task-engine')
app.config_from_object(deployment_configuration)

if __name__ == '__main__':
    app.start(['-A=task_engine',
               'worker',
               '-l=info',
               '--pool=eventlet'])
