import requests
from requests.cookies import RequestsCookieJar
import re
import time
from typing import Dict, Tuple
from .base.multipointsbase import MultiPointsBase


class Crashlytics(MultiPointsBase):

    def __init__(self, settings: Dict, config: Dict) -> None:
        super().__init__(settings=settings, config=config)
        self.url_base = 'https://www.fabric.io/api/v2/organizations/{}/apps/{}/growth_analytics/'
        self.url_crashes = 'crash_free_users_for_top_builds.json?transformation=weighted&limit=3&start={}&end={}'
        self.url_active_users = 'daily_active.json?start={}&end={}&build=all&transformation=seasonal'
        self.url_os_distribution = 'os_distribution_timeseries.json?start={}&end={}&platform=android&limit=9'
        self.url_devices = 'device_distribution_timeseries.json?start={}&end={}&platform=android&limit=9'

    def get_description(self) -> str:
        return 'Running Crashlytics data fetching'

    def _get_cookies_and_csrf_token(self) -> Tuple[RequestsCookieJar, str]:
        auth_data = requests.get('https://fabric.io/login')
        csrf_regex = "<meta content=\"(.*)\" name=\"csrf-token\" \/>"
        csrf_match = re.search(csrf_regex, auth_data.text)
        if csrf_match is None:
            raise Exception('Could not get CSRF token')
        return auth_data.cookies, csrf_match[1]

    def _login(self, csrf_token: str, cookies: RequestsCookieJar) -> RequestsCookieJar:
        login_data = {
            'email': self.config['crash_user'],
            'password': self.config['crash_pass']
        }
        sessions_data = requests.post('https://fabric.io/api/v2/session',
                                      headers=self._get_request_headers(csrf_token),
                                      data=login_data,
                                      cookies=cookies)
        return sessions_data.cookies

    def _build_url(self, url: str, organization: str, app: str, from_date: str, until_date: str) -> str:
        base_url = self.url_base.format(organization, app)
        endpoint = url.format(
            from_date,
            until_date
        )
        return base_url + endpoint

    def _get_data(self, url: str, csrf_token: str, cookies: RequestsCookieJar) -> Dict:
        data = requests.get(url,
                            cookies=cookies,
                            headers=self._get_request_headers(csrf_token))
        return data.json()

    def _get_request_headers(self, csrf_token: str) -> Dict:
        return {
            'X-CRASHLYTICS-DEVELOPER-TOKEN': self.config['crash_dev_token'],
            'X-CSRF-Token': csrf_token,
            'X-Requested-With': 'XMLHttpRequest'
        }

    def get_data(self, key_value: str) -> Dict:
        cookies, csrf_token = self._get_cookies_and_csrf_token()
        cookies = self._login(csrf_token, cookies)
        # take the last 24 hours
        from_date = str(int(time.time()) - (24 * 60 * 60))
        until_date = str(int(time.time()))
        organization = key_value.split('|')[0]
        app = key_value.split('|')[1]
        url = self._build_url(self.url_crashes, organization, app, from_date, until_date)
        data = self._get_data(url, csrf_token, cookies)
        crash_free = data['builds']['all'][-1][1]
        app_details = dict()
        app_details['crash_free_users'] = float(crash_free * 1000) / 10
        url = self._build_url(self.url_active_users, organization, app, from_date, until_date)
        data = self._get_data(url, csrf_token, cookies)
        app_details['active_user_count'] = data['series'][-1][1]
        url = self._build_url(self.url_os_distribution, organization, app, from_date, until_date)
        data = self._get_data(url, csrf_token, cookies)
        for operating_system in data['series'][0][1].items():
            app_details["active_os_{}".format(operating_system[0].replace(' ', ''))] = operating_system[1]
        url = self._build_url(self.url_devices, organization, app, from_date, until_date)
        data = self._get_data(url, csrf_token, cookies)
        for device in data['series'][0][1].items():
            app_details["active_device_{}".format(device[0].replace(' ', ''))] = device[1]
        return app_details
