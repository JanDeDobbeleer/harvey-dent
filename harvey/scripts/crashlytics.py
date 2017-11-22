import requests
import os
import re
import time
from scriptbase import ScriptBase

class Crashlytics(ScriptBase):

    def __init__(self, settings):
        super().__init__()
        self.settings = settings

    def _get_crashlytics_info(self, app):
        # auth on 'https://fabric.io/login, fetch the CRSF token to add it to the header
        auth_data = requests.get('https://fabric.io/login')
        csrf_regex = "<meta content=\"(.*)\" name=\"csrf-token\" \/>"
        csrf_token = re.search(csrf_regex, auth_data.text)[1]
        #set headers
        headers = {
            'X-CRASHLYTICS-DEVELOPER-TOKEN': os.environ.get('CRASH_DEV_TOKEN'),
            'X-CSRF-Token': csrf_token,
            'X-Requested-With': 'XMLHttpRequest'
        }
        # login and start a session
        login_data = {
            'email': os.environ.get('CRASH_USER'),
            'password': os.environ.get('CRASH_PASS')
        }
        sessions_data = requests.post('https://fabric.io/api/v2/session',
                                      headers=headers,
                                      data = login_data,
                                      cookies=auth_data.cookies)
        # take the last 24 hours
        from_date = int(time.time()) - (24*60*60)
        until_date = int(time.time())
        crash_url = "https://fabric.io/api/v2/organizations/{}/apps/{}/growth_analytics/crash_free_users_for_top_builds.json?transformation=weighted&limit=3&start={}&end={}".format(
            app.split('|')[0],
            app.split('|')[1],
            from_date,
            until_date)
        crash_data = requests.get(crash_url,
                                  cookies=sessions_data.cookies,
                                  headers=headers)
        crash_free = crash_data.json()['builds']['all'][-1][1]
        app_details = dict()
        app_details['crash_free_users'] = float(crash_free*1000) / 10
        users_url = "https://fabric.io/api/v2/organizations/{}/apps/{}/growth_analytics/daily_active.json?start={}&end={}&build=all&transformation=seasonal".format(
            app.split('|')[0],
            app.split('|')[1],
            from_date,
            until_date)
        user_data = requests.get(users_url,
                                 cookies=sessions_data.cookies,
                                 headers=headers)
        app_details['active_user_count'] = user_data.json()['series'][-1][1]
        return app_details

    def _write_points(self, key, details, timestamp):
        for (detail, value) in details.items():
            point = "{}_{}".format(key, detail)
            super()._write_point(point, value, timestamp)
            print("Inserted value {} for key {}".format(value, point))

    def run(self):
        try:
            print('Running Crashlytics data fetching')
            timestamp = super()._get_timestamp()
            for (key, app) in self.settings.items():
                details = self._get_crashlytics_info(app)
                self._write_points(key, details, timestamp)
        except Exception as e:
            print(e)
