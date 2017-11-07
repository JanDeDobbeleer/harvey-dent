import requests
from bs4 import BeautifulSoup
from .scriptbase import ScriptBase

class AppStore(ScriptBase):

    def __init__(self, settings):
        super().__init__()
        self.settings = settings

    def _get_appstore_info(self, app):
        url = "https://itunes.apple.com/be/app/{}".format(app)
        app_page = requests.get(url)
        soup = BeautifulSoup(app_page.content, 'html.parser')
        ratingsValue = soup.find("span", {"itemprop": "ratingValue"})
        ratingsCount = soup.find("span", {"itemprop": "reviewCount"})
        app_details = dict()
        app_details['rating'] = float(ratingsValue.string)
        app_details['rated_by'] = int(ratingsCount.string.split(" ")[0])
        return app_details

    def _write_points(self, key, details, timestamp):
        for (detail, value) in details.items():
            point = "{}_{}".format(key, detail)
            super()._write_point(point, value, timestamp)
            print("Inserted value {} for key {}".format(value, point))

    def run(self):
        try:
            print('Running App Store data fetching')
            timestamp = super()._get_timestamp()
            for (key, app) in self.settings.items():
                details =  self._get_appstore_info(app)
                self._write_points(key, details, timestamp)
        except Exception as e:
            print(e)