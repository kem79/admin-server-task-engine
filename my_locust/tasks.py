import subprocess

from celery.utils.log import get_task_logger

proc_ids = {}
logger = get_task_logger(__name__)


def start(application_name, url, number_of_users, hatch_rate, locust_file):
    """
    starts the locust server
    :type application_name: str
    :param application_name: the name of the micro-service

    :type url: str
    :param url the micro-service base url.

    :type number_of_users: int
    :param number_of_users: the number of users to simulate

    :type hatch_rate: int
    :param hatch_rate: the number of user session to start every second at the start
    of the loading phase.

    :type locust_file: str
    :param locust_file: the name of the locust file.

    :return: PID of the process
    """
    proc = subprocess.Popen(['locust',
                             '--host', 'https://' + url,
                             '-f', 'my_locust/{}'.format(locust_file),
                             '--csv', application_name,
                             '--no-web',
                             '-c', str(number_of_users),
                             '-r', str(hatch_rate)])
    logger.info("started locust (PID {}).".format(proc.pid))
    proc_ids[proc.pid] = proc
    return proc.pid


def stop(proc_id):
    """
    Stop the locust server
    :return:
    """
    logger.info('Stop process id {}...'.format(proc_id))
    try:
        proc_ids[proc_id].terminate()
    except KeyError:
        logger.error('Sorry, can\'t find process id {}'.format(proc_id))