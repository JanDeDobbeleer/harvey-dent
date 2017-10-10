#!/usr/bin/env python

import time
import requests
from bs4 import BeautifulSoup
from database import write_point

APPS = {
    "app_store_vikingapp_ios": "viking-app/id893916390",
    "app_store_stievie_ios": "stievie/id1049241602"
}

def get_appstore_info(app):
    url = "https://itunes.apple.com/be/app/{}".format(app)
    app_page = requests.get(url)
    soup = BeautifulSoup(app_page.content, 'html.parser')
    ratingsValue = soup.find("span", {"itemprop": "ratingValue"})
    ratingsCount = soup.find("span", {"itemprop": "reviewCount"})
    app_details = dict()
    app_details['rating'] = float(ratingsValue.string)
    app_details['rated_by'] = int(ratingsCount.string.split(" ")[0])
    return app_details

def write_points(key, details):
    for (detail, value) in details.items():
        point = "{}_{}".format(key, detail)
        #write_point(point, value, tstamp)
        print("Inserted value {} for key {}".format(value, point))

def get_jira_info():
    try:
        print('Running App Store data fetching')
        tstamp = int(time.time()) * 10**9
        for (key, app) in APPS.items():
            details =  get_appstore_info(app)
            write_points(key, details)
    except Exception as e:
        print(e)

get_jira_info()