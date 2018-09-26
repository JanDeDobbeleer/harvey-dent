import abc
from typing import Dict, List
from jira import JIRAError
from jira.client import GreenHopper, ResultList
from .scriptbase import ScriptBase


class JiraBase(ScriptBase):
    """The base script implementation containing all you need."""
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def retrieve_data(self, jql: str) -> str:
        """Retrieve data from the tickets and process what you want"""
        return ""

    def __init__(self, settings: Dict, config: Dict) -> None:
        super().__init__()
        self.settings = settings
        self.config = config
        self.jira = self._jira_login(self.config['jira_endpoint'],
                                     self.config['jira_user'],
                                     self.config['jira_user_password'])

    def retrieve_issues(self, jql: str, fields: List[str] = ['key']) -> ResultList:
        try:
            if isinstance(fields, list):
                strfields = ",".join(fields)
            return self.jira.search_issues(jql, fields=strfields)
        except JIRAError as e:
            raise e

    def _jira_login(self, endpoint: str, user: str, password: str) -> GreenHopper:
        try:
            basic_auth = (user, password)
            jira = GreenHopper({'server': endpoint}, basic_auth=basic_auth)
            # pylint: disable=protected-access
            if "JSESSIONID" in jira._session.cookies:
                # drop basic auth if we have a cookie (for performance)
                jira._session.auth = None
            return jira
        except JIRAError as e:
            raise e

    def run(self) -> None:
        try:
            print('Running JIRA queries')
            tstamp = super()._get_timestamp()
            for (db_key, jql) in self.settings.items():
                count = self.retrieve_data(jql)
                self._write_point(db_key, count, tstamp, None)
        except Exception as e:
            print("Failed to retrieve JIRA data: {}".format(e))
