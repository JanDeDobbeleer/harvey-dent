from jira import Issue
from typing import Dict
from .base.jirabase import JiraBase


class JiraStoryPointCounter(JiraBase):

    def __init__(self, settings: Dict, config: Dict) -> None:
        super().__init__(settings, config)

    def get_points(self, issue: Issue) -> float:
        if hasattr(issue.fields, 'customfield_10708') and issue.fields.customfield_10708 is not None:
            return issue.fields.customfield_10708
        return 0

    def has_story_points(self, issue: Issue) -> bool:
        return hasattr(issue.fields, 'customfield_10708') and issue.fields.customfield_10708 > 0.0

    def log_issues_without_points(self, key: str, value: str) -> None:
        strkey = key + ".missing"
        self._write_point(strkey, value, super()._get_timestamp(), None)

    def retrieve_data(self, jql: str) -> str:
        issues = self.retrieve_issues(jql)
        total_story_points = 0.0
        total_issues_without_points = 0
        for issue in issues:
            full_issue = self.jira.issue(issue.id)
            total_story_points += self.get_points(full_issue)
            total_issues_without_points += 0 if self.has_story_points(issue) else 1
        return str(total_story_points)
