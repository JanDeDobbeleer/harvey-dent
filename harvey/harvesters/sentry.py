import requests
from typing import Dict
from .base.multipointsbase import MultiPointsBase


class Sentry(MultiPointsBase):

    def __init__(self, settings: Dict, config: Dict) -> None:
        super().__init__(settings=settings, config=config)

    def get_description(self) -> str:
        return 'Running Sentry data fetching'

    def get_data(self, key_value: str) -> Dict:
        url = "{}/api/0/projects/{}/issues/?statsPeriod=24h".format(self.config['sentry_url'], key_value)
        sentry_issues = requests.get(url, headers={'Authorization': "Bearer {}".format(self.config['sentry_token'])})
        sentry_details = dict()
        sentry_details['issue_distinct_count_24h'] = len(sentry_issues.json())
        sentry_details['issue_occurance_count_24h'] = sum(len(issue['stats']['24h']) for issue in sentry_issues.json())
        return sentry_details
