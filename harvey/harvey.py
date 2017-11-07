try:
    import time
    import schedule
    import scripts
except Exception as e:
    print("Error during import: "+ e)

# print a pretty logo, because fork yeah
with open('harvey.txt', 'r') as logo:
    print(logo.read())

JIRA_QUERIES = {
    "uwa_open_bugs": "UWA: Open bugs",
    "uwa_backlog_depth": "UWA: Backlog",
    "uwa_sprint_completed": "UWA: Sprint Completed",
    "uwa_sprint_todo": "UWA: Sprint Todo"
}

APPS = {
    "app_store_vikingapp_android": "com.vikingco.vikingapp",
    "app_store_stievie_android": "be.stievie"
}

APPS2 = {
    "app_store_vikingapp_ios": "viking-app/id893916390",
    "app_store_stievie_ios": "stievie/id1049241602"
}

try:
    j = scripts.JiraTickets(JIRA_QUERIES)
    schedule.every(5).minutes.do(j.run)
    p = scripts.PlayStore(APPS)
    schedule.every(1440).minutes.do(p.run)
    a = scripts.AppStore(APPS2)
    schedule.every(1440).minutes.do(a.run)
except Exception as e:
    print(e)

while True:
    schedule.run_pending()
    time.sleep(1)