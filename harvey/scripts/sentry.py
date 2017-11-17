import requests
import os
from .scriptbase import ScriptBase

class Sentry(ScriptBase):

    def __init__(self, settings):
        super().__init__()
        self.settings = settings

    def _get_sentry_info(self, project):
        url = "{}/api/0/projects/{}/issues/?statsPeriod=24h".format(os.environ.get('SENTRY_URL'), project)
        sentry_issues = requests.get(url, headers={'Authorization': "Bearer {}".format(os.environ.get('SENTRY_TOKEN'))})
        sentry_details = dict()
        sentry_details['issue_distinct_count_24h'] = len(sentry_issues.json())
        sentry_details['issue_occurance_count_24h'] = sum(len(issue['stats']['24h']) for issue in sentry_issues.json())
        return sentry_details

    def _write_points(self, key, details, timestamp):
        for (detail, value) in details.items():
            point = "{}_{}".format(key, detail)
            super()._write_point(point, value, timestamp)
            print("Inserted value {} for key {}".format(value, point))

    def run(self):
        try:
            print('Running Sentry data fetching')
            timestamp = super()._get_timestamp()
            for (key, app) in self.settings.items():
                details =  self._get_sentry_info(app)
                self._write_points(key, details, timestamp)
        except Exception as e:
            print(e)
