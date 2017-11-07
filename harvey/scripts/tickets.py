import os
from jira import JIRAError
from jira.client import GreenHopper
from .scriptbase import ScriptBase
class JiraTickets(ScriptBase):

    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.jira = self.jira_login(os.environ.get('JIRA_ENDPOINT'),
                                    os.environ.get('JIRA_USER'),
                                    os.environ.get('JIRA_USER_PASSWORD'))

    def retrieve_issues(self, jira_filter, fields=['key']):
        try:
            jql = "filter='%s'" % jira_filter
            if isinstance(fields, list):
                fields = ",".join(fields)
            return self.jira.search_issues(jql, fields=fields)
        except JIRAError as exn:
            print(exn)

    def retrieve_issue_count(self, jira_filter):
        issues = self.retrieve_issues(jira_filter)
        return issues.total

    def jira_login(self, endpoint, user, password):
        try:
            basic_auth = (user, password)
            jira = GreenHopper({'server': endpoint}, basic_auth=basic_auth)
            # pylint: disable=protected-access
            if "JSESSIONID" in jira._session.cookies:
                # drop basic auth if we have a cookie (for performance)
                jira._session.auth = None
            return jira
        except JIRAError as exn:
            print(exn)

    def run(self):
        try:
            print('Running JIRA queries')
            jira = self.jira_login(os.environ.get('JIRA_ENDPOINT'), os.environ.get('JIRA_USER'), os.environ.get('JIRA_USER_PASSWORD'))
            tstamp = super()._get_timestamp()
            for (db_key, jira_filter) in self.settings.items():
                count = self.retrieve_issue_count(jira_filter)
                self._write_point(db_key, count, tstamp)
                print("Inserted value {} for key {}".format(count, db_key))
        except Exception as e:
            print("Filed to retrieve JIRA queries: {}".format(e))
