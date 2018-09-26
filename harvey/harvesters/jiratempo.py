from datetime import datetime, timedelta
from typing import Dict
from .base.jirabase import JiraBase


class TempoExporter(JiraBase):

    def __init__(self, settings: Dict, config: Dict) -> None:
        super().__init__(settings, config)

    def retrieve_worklog(self, db_key: str, team: str) -> None:
        projects = self.jira.projects()
        date_from = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        date_to = datetime.now().strftime("%Y-%m-%d")
        url = f'https://jira.itpservices.be/rest/tempo-timesheets/3/worklogs/?teamId={team}&dateFrom={date_from}&dateTo={date_to}' # noqa
        data = self.jira._session.get(url, params=None)
        for worklog in data.json():
            project = next((project for project in projects if project.id == str(worklog['issue']['projectId'])), None) # noqa
            if project is None:
                continue
            excluded_projects = self.config['excluded_jira_projects'] if self.config['excluded_jira_projects'] is not None else []
            if project.id in excluded_projects:
                continue
            project_name = project.name if project is not None else 'Unknown'
            category = project.projectCategory.name if hasattr(project, 'projectCategory') else 'Unknown'
            metadata = {
                'id': worklog['issue']['id'],
                'project_id': worklog['issue']['projectId'],
                'author': worklog['author']['key'],
                'project_name': project_name,
                'project_category': category,
            }
            self._write_point(db_key, worklog['timeSpentSeconds'], worklog['dateStarted'], metadata)

    def run(self) -> None:
        try:
            print('Running Tempo Worklog update')
            for (db_key, team) in self.settings.items():
                self.retrieve_worklog(db_key, team)
        except Exception as e:
            print("Failed to retrieve Worklog: {}".format(e))
