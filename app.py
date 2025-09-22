"""
ZenWeek Flask Application
------------------------
This module implements the ZenWeek weekly planner web app, including all Flask routes, database helpers, and utility functions.
"""

from flask import Flask, render_template, request, redirect
import datetime
import os
import sqlite3 as sql
from sqlite3 import Error
from typing import Optional
import importlib.util
import sys


app = Flask(__name__)
app.config.from_object('config.ProdConfig')
 # app.config.from_object('config.DevConfig')


def run_weekly_backup_if_needed():
    # Import backup_restore.py as a module
    backup_restore_path = os.path.join(os.path.dirname(__file__), 'backup_restore.py')
    spec = importlib.util.spec_from_file_location('backup_restore', backup_restore_path)
    if spec is None or spec.loader is None:
        print("Could not import backup_restore.py for weekly backup.")
        return
    backup_restore = importlib.util.module_from_spec(spec)
    sys.modules['backup_restore'] = backup_restore
    spec.loader.exec_module(backup_restore)

    weekly_dir = backup_restore.WEEKLY_DIR
    now = datetime.datetime.now()
    year, week, _ = now.isocalendar()
    # Look for a backup file for this week
    found = False
    if os.path.exists(weekly_dir):
        for fname in os.listdir(weekly_dir):
            if fname.startswith(f"weekly_") and fname.endswith('.sqlite3'):
                # Parse the timestamp: weekly_YYYYMMDD_HHMMSS.sqlite3
                try:
                    ts = fname.split('_')[1]  # YYYYMMDD
                    file_year = int(ts[:4])
                    file_week = datetime.date(int(ts[:4]), int(ts[4:6]), int(ts[6:8])).isocalendar()[1]
                    if file_year == year and file_week == week:
                        found = True
                        break
                except Exception:
                    continue
    if not found:
        print(f"No weekly backup found for week {week} {year}, creating one...")
        backup_restore.weekly_backup()
    else:
        print(f"Weekly backup for week {week} {year} already exists.")

# Run backup check at startup
run_weekly_backup_if_needed()


app = Flask(__name__)
app.config.from_object('config.ProdConfig')
# app.config.from_object('config.DevConfig')


# Verbindung zur DB...
def get_db_connection():
    """
    Establish a connection to the configured SQLite database.
    Returns a sqlite3.Connection object or 0 on failure.
    """
    try:
        db_uri = app.config.get('DATABASE_URI', 'prod.sqlite3')
        conn = sql.connect(db_uri)
        conn.row_factory = sql.Row
        print(f"Verbindung zur DB {db_uri} steht\n")
        return conn
    except Error as e:
        print(e)
        return 0


def get_rows(query, filtercol=None, filterterm=None):
    """
    Execute a SELECT query with optional filtering and return all rows.
    """
    try:
        con = get_db_connection()
        if not con:
            print("DB connection failed in get_rows.")
            return []
        cursor = con.cursor()
        if filtercol and filterterm:
            query = query + f' WHERE {filtercol} = ?;'
            print(query)
            cursor.execute(query, (filterterm,))
        else:
            print(query)
            cursor.execute(query)
        rows = cursor.fetchall()
        con.close()
        return rows
    except Exception as e:
        print(f"DB error in get_rows: {e}")
        return []


def weeks_for_year(year):
    """
    Return the number of ISO calendar weeks in a given year.
    """
    # See: https://stackoverflow.com/questions/29262859/the-number-of-calendar-weeks-in-a-year
    last_week = datetime.date(year, 12, 28)
    return last_week.isocalendar()[1]


def create_week_array(year, week_nr):
    """
    Return a list of (week, year) tuples for the 4 weeks before and after the given week.
    Used for week navigation in the UI.
    """
    week_array = []
    for i in range(-4, 5):
        if week_nr + i < 1:
            week_array.append((weeks_for_year(year - 1) + (week_nr + i), year - 1))
        elif week_nr + i > weeks_for_year(year):
            week_array.append((week_nr + i - weeks_for_year(year), year + 1))
        else:
            week_array.append((week_nr + i, year))
    return week_array


def get_first_day_of_week(year: int, week_number: int) -> Optional[datetime.date]:
    """
    Return the date of the Monday for the given ISO year and week number.
    Returns None if the week number is invalid for the year.
    """
    try:
        # January 4th is always in week 1
        jan4 = datetime.date(year, 1, 4)
        first_day_of_year = jan4 - datetime.timedelta(days=jan4.weekday())  # Get the Monday of week 1
        target_date = first_day_of_year + datetime.timedelta(weeks=week_number - 1)

        # Verify if the calculated week number for the target date matches the input
        if target_date.isocalendar().week == week_number and target_date.isocalendar().year == year:
            return target_date
        else:
            return None  # Week number is likely invalid for the year
    except ValueError:
        return None  # Handle cases like invalid year

# Update function signature to allow None return


# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'),
#         'favicon.ico',mimetype='image/vnd.microsoft.icon')
@app.route('/')
def index():
    """
    Main route: renders the weekly planner for the selected week and year.
    """
    year = request.args.get("year", type=int)
    week = request.args.get("week", type=int)
    if not year:
        year = datetime.datetime.now().year
    if not week:
        week = datetime.datetime.now().isocalendar().week

    dates = {}
    dates["first_day_of_week"] = get_first_day_of_week(year, week)
    if dates["first_day_of_week"] is None:
        return "Invalid week number for the selected year.", 400
    dates["last_day_of_week"] = dates["first_day_of_week"] + datetime.timedelta(days=6)
    dates["current_week"] = datetime.datetime.now().isocalendar().week
    dates["current_year"] = datetime.datetime.now().year
    dates["selected_week"] = week
    dates["selected_year"] = year
    dates["weekday_names"] = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
    dates["weekdays"] = []
    dates["weekdays"].append(dates["first_day_of_week"])
    for i in range(1, 7):
        dates["weekdays"].append(dates["first_day_of_week"] + datetime.timedelta(days=i))

    # Compute open task counts for each week in the navigation
    week_list = create_week_array(year, week)
    open_task_counts = {}
    con = get_db_connection()
    if con:
        cursor = con.cursor()
        for w, y in week_list:
            cursor.execute(
                "SELECT COUNT(*) FROM tasks WHERE status = 'open' AND year = ? AND week = ?",
                (y, w)
            )
            count = cursor.fetchone()[0]
            open_task_counts[(y, w)] = count
        con.close()

    return render_template('index.html', weeks=week_list, dates=dates, open_task_counts=open_task_counts)


@app.route('/get_tasks')
def get_tasks():
    """
    Route: returns the tasks for a given week or day as HTML (for AJAX loading).
    """
    try:
        year = request.args.get('year', type=int)
        week = request.args.get('week', type=int)
        date = request.args.get('date', type=str)
        if not (year and week) and not date:
            return "Missing required parameters.", 400
        con = get_db_connection()
        if not con:
            return "Database connection failed.", 500
        cursor = con.cursor()
        query = 'SELECT id, taskname, description, url, status, priority FROM tasks WHERE status != ? AND '
        if date:
            query = query + 'date = ? ORDER BY position;'
            print(query)
            cursor.execute(query, ("deleted", date))
            rows = cursor.fetchall()
            print('Number of rows is', len(rows))
            con.close()
            fillrows = 5 - len(rows) if len(rows) < 5 else 0
        else:
            query = query + 'year = ? AND week = ? AND date is NULL ORDER BY position;'
            print(query)
            cursor.execute(query, ("deleted", year, week))
            rows = cursor.fetchall()
            print('Number of rows is', len(rows))
            con.close()
            fillrows = 1 - len(rows) if len(rows) < 1 else 0
        return render_template('days.html', tasks=rows, fillrows=fillrows)
    except Exception as e:
        print(f"Error in get_tasks: {e}")
        return "An error occurred while fetching tasks.", 500


@app.route('/createTask')
def create_task():
    """
    Route: creates a new task for a given week or day, then redirects to the planner.
    """
    try:
        for arg in request.args:
            print(f'{arg}: {request.args.get(arg)}')
        year = request.args.get('year', type=int)
        week = request.args.get('week', type=int)
        date = request.args.get('date', type=str)
        taskname = request.args.get('taskname', type=str)
        if not (year and week and taskname):
            return "Missing required parameters.", 400
        con = get_db_connection()
        if not con:
            return "Database connection failed.", 500
        cursor = con.cursor()
        now = datetime.datetime.now()
        if date:
            query = 'INSERT INTO tasks (create_date, taskname, status, priority, position, year, week, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?);'
            params = (now, taskname, "open", 1, 0, year, week, date)
        else:
            query = 'INSERT INTO tasks (create_date, taskname, status, priority, position, year, week) VALUES (?, ?, ?, ?, ?, ?, ?);'
            params = (now, taskname, "open", 1, 0, year, week)
        print(f'Insert-Query: {query} {params}')
        cursor.execute(query, params)
        con.commit()
        con.close()
        return redirect(f'/?year={year}&week={week}')
    except Exception as e:
        print(f"Error in create_task: {e}")
        return "An error occurred while creating the task.", 500

    # return render_template('days.html', tasks=rows, fillrows=fillrows)


@app.route('/moveTask')
def move_task():
    """
    Route: moves a task to a different week or day.
    """
    try:
        taskid = request.args.get('taskid', type=int)
        year = request.args.get('year', type=int)
        week = request.args.get('week', type=int)
        date = request.args.get('date', type=str)
        if taskid and year and week and date:
            data = {"status": "success"}
            return data, 200
        elif taskid and year and week:
            con = get_db_connection()
            if not con:
                return {"status": "error", "message": "Database connection failed."}, 500
            cursor = con.cursor()
            query = 'UPDATE tasks SET date = null, year = ?, week = ? WHERE id = ?;'
            print(f'Update-Query: {query} ({year}, {week}, {taskid})')
            cursor.execute(query, (year, week, taskid))
            con.commit()
            con.close()
            data = {"status": "success"}
            return data, 200
        else:
            data = {"status": "failed"}
            return data, 400
    except Exception as e:
        print(f"Error in move_task: {e}")
        return {"status": "error", "message": str(e)}, 500


@app.route('/updateTask')
def update_task():
    """
    Route: updates the date/position of a task (used for drag-and-drop reordering).
    """
    try:
        taskid = request.args.get('taskid', type=int)
        date = request.args.get('date', type=str)
        order = request.args.get('order', type=int)
        if taskid and order:
            con = get_db_connection()
            if not con:
                return {"status": "error", "message": "Database connection failed."}, 500
            cursor = con.cursor()
            if date:
                query = 'UPDATE tasks SET date = ?, position = ? WHERE id = ?;'
                params = (date, order, taskid)
            else:
                query = 'UPDATE tasks SET date = null, position = ? WHERE id = ?;'
                params = (order, taskid)
            print(f'Update-Query: {query} {params}')
            cursor.execute(query, params)
            con.commit()
            con.close()
            data = {"status": "success"}
            return data, 200
        else:
            print(f'taskid: {taskid}, date: {date}, order: {order}')
            data = {"status": "failed", "message": "Missing taskid or order."}
            return data, 400
    except Exception as e:
        print(f"Error in update_task: {e}")
        return {"status": "error", "message": str(e)}, 500


@app.route("/modifyTask")
def modify_task():
    """
    Route: modifies the name or URL of a task (edit modal).
    """
    try:
        taskid = request.args.get('taskEditModal-taskid', type=int)
        year = request.args.get('taskEditModal-year', type=int)
        week = request.args.get('taskEditModal-week', type=int)
        task = request.args.get('taskEditModal-task', type=str)
        taskurl = request.args.get('taskEditModal-taskurl', type=str)
        if not (taskid and task and year and week):
            return "Missing required parameters.", 400
        con = get_db_connection()
        if not con:
            return "Database connection failed.", 500
        cursor = con.cursor()
        if taskurl:
            query = 'UPDATE tasks SET taskname = ?, url = ? WHERE id = ?;'
            params = (task, taskurl, taskid)
        else:
            query = 'UPDATE tasks SET taskname = ?, url = null WHERE id = ?;'
            params = (task, taskid)
        cursor.execute(query, params)
        con.commit()
        con.close()
        return redirect(f'/?year={year}&week={week}')
    except Exception as e:
        print(f"Error in modify_task: {e}")
        return "An error occurred while modifying the task.", 500


@app.route('/deleteTask')
def delete_task():
    """
    Route: marks a task as deleted (soft delete).
    """
    try:
        taskid = request.args.get('taskid', type=int)
        if taskid:
            con = get_db_connection()
            if not con:
                return {"status": "error", "message": "Database connection failed."}, 500
            cursor = con.cursor()
            query = 'UPDATE tasks SET status = ? WHERE id = ?;'
            print(f'Delete-Query: {query} (deleted, {taskid})')
            cursor.execute(query, ("deleted", taskid))
            con.commit()
            con.close()
            data = {"status": "success"}
            return data, 200
        else:
            data = {"status": "failed", "message": "Missing taskid."}
            return data, 400
    except Exception as e:
        print(f"Error in delete_task: {e}")
        return {"status": "error", "message": str(e)}, 500


@app.route('/editTask')
def edit_task():

    """
    Route: toggles a task's status (done/undo/delete) via AJAX.
    """
    try:
        for arg in request.args:
            print(f'{arg}: {request.args.get(arg)}')
        taskid = request.args.get('taskid', type=int)
        action = request.args.get('action', type=str)
        if not (taskid and action):
            return {"status": "failed", "message": "Missing taskid or action."}, 400
        con = get_db_connection()
        if not con:
            return {"status": "error", "message": "Database connection failed."}, 500
        cursor = con.cursor()
        if action == "done":
            status = "done"
        elif action == "undo":
            status = "open"
        elif action == "delete":
            status = "deleted"
        else:
            return {"status": "failed", "message": "Invalid action."}, 400
        now = datetime.datetime.now()
        query = 'UPDATE tasks SET resolve_date = ?, status = ? WHERE id = ?;'
        print(f'Update-Query: {query} ({now}, {status}, {taskid})')
        cursor.execute(query, (now, status, taskid))
        con.commit()
        con.close()
        data = {"status": "success"}
        return data, 200
    except Exception as e:
        print(f"Error in edit_task: {e}")
        return {"status": "error", "message": str(e)}, 500

    # return render_template('days.html', tasks=rows, fillrows=fillrows)

# --- Summary page route ---
@app.route('/summary')
def summary():
    con = get_db_connection()
    open_tasks = []
    weekly_stats = {}
    if con:
        cursor = con.cursor()
        # Open and overdue tasks
        cursor.execute("SELECT id, taskname, year, week, status, date, url FROM tasks WHERE status = 'open'")
        now = datetime.datetime.now().date()
        # Get current year and week for overdue logic
        today = datetime.date.today()
        current_year, current_week, _ = today.isocalendar()
        for row in cursor.fetchall():
            # Overdue: if date is set and in the past, or if no date but (year, week) < (current_year, current_week)
            is_overdue = False
            show_in_summary = False
            if row['date']:
                try:
                    due = datetime.datetime.strptime(row['date'], '%Y-%m-%d').date()
                    is_overdue = due < now
                    show_in_summary = is_overdue
                except Exception:
                    pass
            else:
                # No due date: check if week is in the past
                task_year = row['year']
                task_week = row['week']
                if (task_year, task_week) < (current_year, current_week):
                    is_overdue = True
                    show_in_summary = True
            if show_in_summary:
                open_tasks.append({
                    'id': row['id'],
                    'taskname': row['taskname'],
                    'year': row['year'],
                    'week': row['week'],
                    'is_overdue': is_overdue,
                    'url': row['url']
                })
        # Weekly stats: total and completed per week (last 10 weeks)
        cursor.execute("SELECT year, week, COUNT(*) as total, SUM(CASE WHEN status = 'done' THEN 1 ELSE 0 END) as completed FROM tasks GROUP BY year, week ORDER BY year DESC, week DESC LIMIT 10")
        stats = cursor.fetchall()
        stats = list(reversed(stats))
        weekly_data = {
            'labels': [f"KW{row['week']} {row['year']}" for row in stats],
            'total': [row['total'] for row in stats],
            'completed': [row['completed'] or 0 for row in stats]
        }
        con.close()
    else:
        weekly_data = {'labels': [], 'total': [], 'completed': []}
    # Sort open_tasks by year, then week (oldest first)
    open_tasks.sort(key=lambda t: (t['year'], t['week']))
    # Group open tasks by year for summary table
    from collections import Counter
    year_counts = Counter(t['year'] for t in open_tasks)
    year_summary = [{'year': y, 'count': year_counts[y]} for y in sorted(year_counts)]
    return render_template('summary.html', open_tasks=open_tasks, weekly_data=weekly_data, year_summary=year_summary)


if __name__ == '__main__':
    """
    Run the Flask development server if this script is executed directly.
    """
    db_uri = app.config.get('DATABASE_URI') or 'prod.sqlite3'
    if os.path.exists(db_uri):
        app.run(debug=True)
    else:
        print('Could not connect to the database. Please first execute initdb.py to create the database.')
