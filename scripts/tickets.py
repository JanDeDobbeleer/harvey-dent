#!/usr/bin/env python

import time
import os
from jira import JIRAError
from jira.client import GreenHopper
from database import write_point

COUNT_QUERIES = {
    "uwa_open_bugs": "UWA: Open bugs",
    "uwa_backlog_depth": "UWA: Backlog",
    "uwa_sprint_completed": "UWA: Sprint Completed",
    "uwa_sprint_todo": "UWA: Sprint Todo"
}

KEY_FIELD = "key"

def retrieve_issues(jira, jira_filter, fields):
    try:
        jql = "filter='%s'" % jira_filter
        if isinstance(fields, list):
            fields = ",".join(fields)
        return jira.search_issues(jql, fields=fields)
    except JIRAError as exn:
        print(exn)
        exit(3)

def retrieve_issue_count(jira, jira_filter):
    issues = retrieve_issues(jira, jira_filter, fields=[KEY_FIELD])
    return issues.total

def jira_login(endpoint, user, password):
    try:
        basic_auth = (user, password)
        try:
            jira = GreenHopper({'server': endpoint}, basic_auth=basic_auth)
        except JIRAError:
            jira = GreenHopper({'server': endpoint})
        # pylint: disable=protected-access
        if "JSESSIONID" in jira._session.cookies:
            # drop basic auth if we have a cookie (for performance)
            jira._session.auth = None
        return jira
    except JIRAError as exn:
        print(exn)

def get_jira_info():
    print('Running JIRA queries')
    jira = jira_login(os.environ.get('JIRA_ENDPOINT'), os.environ.get('JIRA_USER'), os.environ.get('JIRA_USER_PASSWORD'))
    tstamp = int(time.time()) * 10**9
    for (db_key, jira_filter) in COUNT_QUERIES.items():
        count = retrieve_issue_count(jira, jira_filter)
        write_point(db_key, count, tstamp)
        print("Inserted value {} for key {}".format(count, db_key))
