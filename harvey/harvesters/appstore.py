from bs4 import BeautifulSoup
import json
import requests
from typing import Dict
from .base.multipointsbase import MultiPointsBase


class AppStore(MultiPointsBase):

    def __init__(self, settings: Dict, config: Dict) -> None:
        super().__init__(settings=settings, config=config)

    def get_description(self) -> str:
        return 'Running App Store data fetching'

    def get_data(self, key_value: str) -> Dict:
        url = "https://itunes.apple.com/be/app/{}".format(key_value)
        app_page = requests.get(url)
        soup = BeautifulSoup(app_page.content, 'html.parser')
        json_schema = soup.find("script", {"name": "schema:software-application"}).string
        data = json.loads(json_schema)
        app_details = dict()
        app_details['rating'] = float(data['aggregateRating']['ratingValue'])
        app_details['rated_by'] = int(data['aggregateRating']['reviewCount'])
        return app_details
