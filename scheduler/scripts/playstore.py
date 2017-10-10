#!/usr/bin/env python

import time
import requests
from bs4 import BeautifulSoup
from database import write_point

APPS = {
    "app_store_vikingapp_android": "com.vikingco.vikingapp",
    "app_store_stievie_android": "be.stievie"
}

def get_playstore_info(app):
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

def write_points(key, details):
    for (detail, value) in details.items():
        point = "{}_{}".format(key, detail)
        #write_point(point, value, tstamp)
        print("Inserted value {} for key {}".format(value, point))

def get_jira_info():
    try:
        print('Running Play Store data fetching')
        tstamp = int(time.time()) * 10**9
        for (key, app) in APPS.items():
            details =  get_playstore_info(app)
            write_points(key, details)
    except Exception as e:
        print(e)
