from datetime import datetime
from dateutil.parser import parse
from typing import Dict
from .base.jirabase import JiraBase


class JiraBoardInfo(JiraBase):

    def __init__(self, settings: Dict, config: Dict) -> None:
        super().__init__(settings, config)

    def retrieve_board_info(self, db_key: str, board: int) -> None:
        backlog_info = self.get_agile_info(f'/rest/agile/1.0/board/{board}/backlog')
        self._write_point(f"{db_key}.backlog_size", backlog_info['total'], super()._get_timestamp(), None)
        sprint_info = self.get_agile_info(f'/rest/greenhopper/latest/sprintquery/{board}?includeHistoricSprints=true&includeFutureSprints=true') # noqa
        active_sprints = [sprint for sprint in sprint_info['sprints'] if sprint['state'] == 'ACTIVE']
        if len(active_sprints) != 1:
            return
        current_sprint = active_sprints[0]
        current_sprint_info = self.get_agile_info(f"/rest/agile/1.0/sprint/{current_sprint['id']}")
        start_date = parse(current_sprint_info['startDate'])
        self._write_point(f"{db_key}.sprint_goal", current_sprint['goal'], super()._get_timestamp(), None)
        burn_down_chart = self.get_agile_info(f"/rest/greenhopper/1.0/rapid/charts/scopechangeburndownchart.json?rapidViewId={board}&sprintId={current_sprint['id']}&statisticFieldId=field_{self.config['story_points_field']}") # noqa
        initial_story_points = 0.0
        for tick, values in burn_down_chart['changes'].items():
            change_date = datetime.fromtimestamp(int(tick) / 1000)
            if change_date.date() <= start_date.date():
                initial_story_points += self.get_story_points_for_date(values)
        self._write_point(f"{db_key}.spint_commitment", initial_story_points, super()._get_timestamp(), None)

    def get_story_points_for_date(self, changes: Dict) -> float:
        story_points = 0.0
        for change in changes:
            story_points += self.get_story_points_for_change(change)
        return story_points

    def get_story_points_for_change(self, change: Dict) -> float:
        if 'statC' in change and 'newValue' in change['statC']:
            return float(change['statC']['newValue'])
        return 0.0

    def get_agile_info(self, url: str) -> Dict:
        url = f"{self.config['jira_endpoint']}{url}"
        data = self.jira._session.get(url, params=None)
        return data.json()

    def run(self) -> None:
        try:
            print('Running Jira sprint info gathering')
            for (db_key, board) in self.settings.items():
                self.retrieve_board_info(db_key, board)
        except Exception as e:
            print("Failed to retrieve Jira Sprint info: {}".format(e))
