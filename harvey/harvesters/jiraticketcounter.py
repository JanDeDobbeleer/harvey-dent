from typing import Dict
from .base.jirabase import JiraBase


class JiraTicketCounter(JiraBase):

    def __init__(self, settings: Dict, config: Dict) -> None:
        super().__init__(settings, config)

    def retrieve_data(self, jql: str) -> str:
        issues = self.retrieve_issues(jql)
        return str(len(issues))
