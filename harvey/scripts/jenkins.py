import requests
import os
from scriptbase import ScriptBase

class Jenkins(ScriptBase):

    def __init__(self, settings):
        super().__init__()
        self.settings = settings

    def _get_jenkins_info(self, build):
        master_build = "{}/job/{}/job/master/lastBuild/api/json?pretty=true".format(os.environ.get('JENKINS_SERVER'), build)
        data = requests.get(master_build, auth=(os.environ.get('JENKINS_USER'), os.environ.get('JENKINS_PASSWORD')))
        app_details = dict()
        app_details['crash_free_users'] = 'tralala'
        return app_details

    def _write_points(self, key, details, timestamp):
        for (detail, value) in details.items():
            point = "{}_{}".format(key, detail)
            #super()._write_point(point, value, timestamp)
            print("Inserted value {} for key {}".format(value, point))

    def run(self):
        try:
            print('Running Jenkins data fetching')
            timestamp = super()._get_timestamp()
            for (key, app) in self.settings.items():
                details = self._get_jenkins_info(app)
                self._write_points(key, details, timestamp)
        except Exception as e:
            print(e)

_settings = {
    "uwa": "VikingCo/job/unleashed-web-api/",
    "mvne": "VikingCo/job/mvne-platform/",
    "viking_app_ios": "VikingCo/job/viking-app-ios",
    "viking_app_android": "Viking App Android"
}
jenky = Jenkins(_settings)
jenky.run()
