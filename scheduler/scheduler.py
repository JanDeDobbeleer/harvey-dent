import schedule
import time
from scripts.tickets import get_jira_info

# print a pretty logo, because fork yeah
with open('scheduler.txt', 'r') as fin:
    print(fin.read())

# schedule jobs to run
schedule.every(5).minutes.do(get_jira_info)

while True:
    schedule.run_pending()
    time.sleep(1)