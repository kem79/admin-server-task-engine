"""
Performance test of data-collection service data ingestion.
the test creates performance metrics data packages and push them to the file server (which simulates ESRS).
the test then creates the JSON messages and send them to data-collection to trigger data ingestion.
the following environment variables can be declared to configure the test load:
- CLUSTER_COUNT: to configure the number of clusters which report data in the performance metric package.
- HOST_COUNT: to configure the number of hosts per cluster which report data in the performance metric package.
_ VM_COUNT: to configure the number of vms per host which report data in the performance metric package.

"""
import json
import math
import os

import sys
from celery.utils.log import get_task_logger
from pika.exceptions import ChannelClosed

from factory_boy.data.cluster_factory import ClusterFactory
from factory_boy.data.host_factory import HostFactory
from factory_boy.data.vm_factory import VMFactory
from rabbitmq import get_client
from railai_tfw.util import random_site_id, random_psnt
from railai_tfw.factory_boy.data.alarm_metrics_factory import AlarmMetricsFactory
from railai_tfw.factory_boy.data.data_center_factory import DataCenterFactory
from railai_tfw.factory_boy.mft_packages.mft_package import MftPackage
from railai_tfw.factory_boy.data.alarm_factory import AlarmFactory
from railai_tfw.client.file_server.FileServerClient import FileServerClient
from railai_tfw.factory_boy import rfactory

from locust import Locust, TaskSet, task, events
from locust.exception import StopLocust, LocustError
import uuid
import datetime

esrs_messages = []
fs = FileServerClient()
# duration of the performance test, in seconds
simulation_time = 5*60
# target RPM, also equal to the umber of customer per minute
rps = 5
# count of data metrics packages to sustain RPM for simulation time
number_of_packages_of_data = math.ceil(simulation_time * rps)
print('Will create {} packages of metrics on FTP server.'.format(number_of_packages_of_data))
now = datetime.datetime.now().strftime('%Y-%M-%d')
logger = get_task_logger(__name__)


class RabbitTaskSet(TaskSet):
    already_run = False
    @task
    def publish(self):
        try:
            message = esrs_messages.pop()
            logger.info('send message')
            get_client().publish(str(os.getenv('MQ_EXCHANGE_ESRS_MFT')),
                                 str(os.getenv('MQ_ROUTING_KEY_ESRS_MFT')),
                                 json.dumps(message))
        except IndexError:
            logger.info('No more packages to ingest.')
            try:
                self.interrupt(reschedule=False)
            except LocustError:
                if not self.already_run:
                    events.locust_stop_hatching.fire()
                    events.quitting.fire()
                    raise StopLocust()
                    # self.already_run = True


class MyLocust(Locust):

    already_run = False

    @staticmethod
    def setup():
        """
        Test data preparation.
        1) Create N packages of metrics data and put them on ftp file server (this represent ESRS storage)
        2) create N rabbitMQ messages
        3) publish the messages to the front end queue of data-collection-service to initiate data ingestion
        4) messages are published randomly over a 1 hour time frame to simulate the actual production behavior.
        :return:
        """
        # test data preparation
        with fs.sftp_connect(auto_delete_packages=False) as conn:
            for counter in range(number_of_packages_of_data):
                cluster_uuid = uuid.uuid4()
                psnt = random_psnt()
                site_id = random_site_id()


                # create data metrics package
                package = MftPackage(
                    name='DC_1.0.0_Performance_{}_{}-00-44-11_11145361'.format(cluster_uuid, now))

                clusters = ClusterFactory.build_batch(
                    os.getenv('CLUSTER_COUNT', 1),
                    hosts=HostFactory.build_batch(
                        os.getenv('HOST_COUNT', 3),
                        vms=VMFactory.build_batch(
                            os.getenv('VM_COUNT', 7)
                        )))

                perf = DataCenterFactory.build(
                    site_id=site_id,
                    psnt=psnt,
                    clusters=[{"clusters": clusters}])

                package.add_data_collection(perf, obj_type='cms')

                # create alarms data and add to metrics package
                alarm = AlarmMetricsFactory.build(data=AlarmFactory.build_batch(5),
                                                  site_id=site_id,
                                                  psnt=psnt)
                package.add_data_collection(alarm, obj_type='alarm')


                # load perf metrics data packages to ftp server
                with package.build() as package:
                    remote_file_name = '{}.tgz'.format(package.name)
                    print('upload {}'.format(remote_file_name))
                    conn.ftp_put(localpath=package.path,
                                 remote_file_name=remote_file_name)

                # build ESRS message
                notification_id = str(uuid.uuid4())
                esrs_message = rfactory.mft.message.build(
                    file_location_uri='{ftp_server_uri}{package_name}.tgz'.format(ftp_server_uri=fs.uri,
                                                                                  package_name=package.name),
                    file_name='{package_name}.tgz'.format(package_name=package.name),
                    notification_id=notification_id).to_json()
                esrs_messages.append(esrs_message)

    def teardown(self):
        logger.info('Delete performance data packages on remote FTP server.')
        fs.delete_packages()

    task_set = RabbitTaskSet
    min_wait = 1000
    max_wait = 1000


def on_locust_stop_hatching():
    try:
        get_client().disconnect()
    except ChannelClosed:
        logger.warning('Channel is already closed.')


events.locust_stop_hatching += on_locust_stop_hatching

if __name__ == '__main__':

    clusters = ClusterFactory.build_batch(
        os.getenv('CLUSTER_COUNT', 1),
        hosts=HostFactory.build_batch(
            os.getenv('HOST_COUNT', 3),
            vms=VMFactory.build_batch(
                os.getenv('VM_COUNT', 7)
            )))

    perf = DataCenterFactory.build(
        site_id='111',
        psnt='222',
        clusters=[{"clusters": clusters}])

    print(sys.getsizeof(str(perf))/1024/1024, "MB")