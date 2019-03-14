import subprocess

proc_ids = {}


def start(application_name, url, number_of_users, hatch_rate):
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

    :return: PID of the process
    """
    proc = subprocess.Popen(['locust',
                             '--host', 'https://' + url,
                             '-f', 'my_locust/locustfile.py',
                             '--csv', application_name,
                             '--no-web',
                             '-c', str(number_of_users),
                             '-r', str(hatch_rate)])
    print("started locust (PID {}).".format(proc.pid))
    proc_ids[proc.pid] = proc
    return proc.pid


def stop(proc_id):
    """
    Stop the locust server
    :return:
    """
    print('Stop process id {}...'.format(proc_id))
    try:
        proc_ids[proc_id].terminate()
    except KeyError:
        print('Sorry, can\'t find process id {}'.format(proc_id))