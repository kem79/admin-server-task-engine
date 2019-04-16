import os

from resources.dao.distributions_dao import Distribution


class DistributionsDal:

    def __init__(self, session):
        self.session = session

    def get_by_baseline_id(self, baseline_id):
        return self.session.query(Distribution).filter_by(baseline_id=baseline_id).all()

    def create(self, baseline_id, csv_file):
        """
        Read Locust csv file containing the request distribution to the service and
        store the result in database

        :type baseline_id: str
        :param baseline_id: the id of the baseline in database.

        :param csv_file: the name of the csv file containing the request distribution.
        the name of the file follows Locust convention, <application_name>_distribution.csv

        :return: None
        """
        new_distributions = []
        with open(csv_file, 'r') as csv:
            # exclude first line (headers) and last line (total)
            csv_lines = csv.readlines()[1:-1]
        for line in csv_lines:
            line_tokens = [tokens.replace('"', '') for tokens in line.split(',')]
            new_distribution = Distribution(name=line_tokens[0],
                                            number_of_requests=line_tokens[1],
                                            fifty_percentile=line_tokens[2],
                                            sixty_six_percentile=line_tokens[3],
                                            seventy_five_percentile=line_tokens[4],
                                            eighty_percentile=line_tokens[5],
                                            ninety_percentile=line_tokens[6],
                                            ninety_five_percentile=line_tokens[7],
                                            ninety_eight_percentile=line_tokens[8],
                                            ninety_nine_percentile=line_tokens[9],
                                            one_hundred_percentile=line_tokens[10],
                                            baseline_id=baseline_id)
            new_distributions.append(new_distribution)
        os.remove(csv_file)
        self.session.bulk_save_objects(new_distributions)
        self.session.commit()
