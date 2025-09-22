import sqlite3
from app import create_week_array 
import datetime
import random

db = sqlite3.connect('prod.sqlite3')

with open('schema.sql') as f:
    db.executescript(f.read())

cursor = db.cursor()

current_week = datetime.datetime.now().isocalendar().week
current_year = datetime.datetime.now().year
weeks  = create_week_array(current_year,current_week)
status_list = ["open", "done", "deleted"]
for i in range(0, 50):
    week, year = weeks[random.randint(2,6)] # select a week from two weeks ago until two weeks in the future
    first_day_of_week = datetime.datetime.strptime(f'{year}-W{week}-1', '%Y-W%W-%w')
    task_day = first_day_of_week + datetime.timedelta(days=random.randint(0,6)) # select a random date in the selected week
    task_day = task_day.strftime('%Y-%m-%d')
    if random.randint(0,4) == 0: # for some cases make a weekly task, leaving the date open
        task_day = None

    y = random.randint(0,1)
    status = status_list[random.randint(0,2)]
    if status != status_list[0]:
        r_date = datetime.datetime.now()
    else:
        r_date = None
    
    cursor.execute("INSERT INTO tasks (create_date, resolve_date, taskname, status, priority, position, year, week, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (datetime.datetime.now(), r_date, f"demotask No. {i}", status, random.randint(0,2), 0, year, week, task_day))


db.commit()
db.close()
