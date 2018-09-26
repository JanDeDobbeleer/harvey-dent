from bs4 import BeautifulSoup
import requests
from typing import Dict
from .base.multipointsbase import MultiPointsBase


class PlayStore(MultiPointsBase):

    def __init__(self, settings: Dict, config: Dict) -> None:
        super().__init__(settings=settings, config=config)

    def get_description(self) -> str:
        return 'Running Play Store data fetching'

    def get_data(self, key_value: str) -> Dict:
        url = "https://play.google.com/store/apps/details?id={}".format(key_value)
        app_page = requests.get(url)
        soup = BeautifulSoup(app_page.content, 'html.parser')
        ratingsValue = soup.find("meta", {"itemprop": "ratingValue"})['content']
        ratingsCount = soup.find("meta", {"itemprop": "reviewCount"})['content']
        app_details = dict()
        app_details['rating'] = float(ratingsValue)
        app_details['rated_by'] = int(ratingsCount)
        return app_details
