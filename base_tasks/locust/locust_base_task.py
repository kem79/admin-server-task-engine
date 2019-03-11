from celery import Task
import os


class LocustBaseTask(Task):

    def __init__(self):
        self.locust_hostname = os.getenv('LOCUST_HOSTNAME', 'task_engine')
        self.locust_port = os.getenv('LOCUST_PORT', 18861)
        super.__init__()


    def run(self):
        pass