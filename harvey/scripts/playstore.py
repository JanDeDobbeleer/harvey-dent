import requests
from bs4 import BeautifulSoup
from .scriptbase import ScriptBase

class PlayStore(ScriptBase):

    def __init__(self, settings):
        super().__init__()
        self.settings = settings

    def _get_playstore_info(self, app):
        url = "https://play.google.com/store/apps/details?id={}".format(app)
        app_page = requests.get(url)
        soup = BeautifulSoup(app_page.content, 'html.parser')
        ratingsValue = soup.find("meta", {"itemprop": "ratingValue"})['content']
        ratingsCount = soup.find("meta", {"itemprop": "ratingCount"})['content']
        num_downloads = soup.find("div", {"itemprop": "numDownloads"}).text
        num_downloads_abs = num_downloads.split("-")[1]
        app_details = dict()
        app_details['rating'] = float(ratingsValue)
        app_details['rated_by'] = int(ratingsCount)
        app_details['downloads_absolute'] = int(num_downloads_abs.replace(" ", "").replace(".", ""))
        return app_details

    def _write_points(self, key, details, timestamp):
        for (detail, value) in details.items():
            point = "{}_{}".format(key, detail)
            super()._write_point(point, value, timestamp)
            print("Inserted value {} for key {}".format(value, point))

    def run(self):
        try:
            print('Running Play Store data fetching')
            timestamp = super()._get_timestamp()
            for (key, app) in self.settings.items():
                details =  self._get_playstore_info(app)
                self._write_points(key, details, timestamp)
        except Exception as e:
            print(e)
