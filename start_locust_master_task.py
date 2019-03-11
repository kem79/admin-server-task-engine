from task_engine_app import app

import rpyc
import os

locust_hostname = os.getenv('LOCUST_HOSTNAME', 'https://test-server.cfcd.isus.emc.com')
locust_rpc_port = os.getenv('LOCUST_RPC_PORT', 18861)


@app.task()
def start_locust_master_node(locust_file='locustfile.py', number_of_users=100, hatch_rate=10):
    """
    Start Locust master in distributed mode.
    :param locust_file: the locust file with the performance test specification to run.
    :param number_of_users: the number of concurrent user to simulate.
    :param hatch_rate: the number of users to connect per second.
    :return: the process exi code
    """
    connection = rpyc.connect(locust_hostname,
                              locust_rpc_port)
    res = connection.root.start_master_node(locust_file,
                                            number_of_users,
                                            hatch_rate)
