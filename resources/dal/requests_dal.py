import os
from resources.dao.requests_dao import Request


class RequestsDal:

    def __init__(self, session):
        super().__init__()
        self.session = session

    def create(self, baseline_id, csv_file):
        """
        Read Locust the requests csv file and
        store the result in database

        :type baseline_id: str
        :param baseline_id: the id of the baseline in database.

        :param csv_file: the name of the csv file containing the request distribution.
        the name of the file follows Locust convention, <application_name>_distribution.csv

        :return: None
        """
        new_requests = []
        with open(csv_file, 'r') as csv:
            # exclude first line (headers) and last line (total)
            csv_lines = csv.readlines()[1:-1]
        for line in csv_lines:
            line_tokens = [tokens.replace('"', '') for tokens in line.split(',')]
            new_request = Request(method=line_tokens[0],
                                  name=line_tokens[1],
                                  number_of_requests=line_tokens[2],
                                  number_of_failures=line_tokens[3],
                                  median_response_time=line_tokens[4],
                                  average_response_time=line_tokens[5],
                                  min_response_time=line_tokens[6],
                                  max_response_time=line_tokens[7],
                                  average_content_size=line_tokens[8],
                                  requests_per_second=line_tokens[9],
                                  baseline_id=baseline_id)
            new_requests.append(new_request)
        os.remove(csv_file)
        self.session.bulk_save_objects(new_requests)
        self.session.commit()
