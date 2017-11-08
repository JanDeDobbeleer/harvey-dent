import time
import schedule
import yaml

# print a pretty logo, because fork yeah
with open('harvey.txt', 'r') as logo:
    print(logo.read())

try:
    with open('tasks.yaml', 'r') as tasks:
        _settings = yaml.load_all(tasks)
        module = __import__("scripts")
        for task in _settings:
            class_ = getattr(module, task['script'])
            instance = class_(task['settings'])
            schedule.every(task['interval']).minutes.do(instance.run)
except Exception as e:
        print(e)

while True:
    schedule.run_pending()
    time.sleep(1)