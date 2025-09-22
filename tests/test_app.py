
import os
import sys
import tempfile
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, get_db_connection

@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    app.config['DATABASE_URI'] = db_path
    app.config['TESTING'] = True
    client = app.test_client()
    with app.app_context():
        schema_path = os.path.join(os.path.dirname(__file__), '..', 'schema.sql')
        with open(schema_path, 'rb') as f:
            conn = get_db_connection()
            assert conn != 0, 'DB connection failed in test setup.'
            conn.executescript(f.read().decode('utf8'))
            conn.close()
    yield client
    os.close(db_fd)
    os.unlink(db_path)

def test_index_route(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Wochenplaner' in rv.data

def test_create_task(client):
    rv = client.get('/createTask?year=2025&week=1&taskname=TestTask')
    assert rv.status_code == 302  # Redirect
    # Check if task was created in DB
    con = get_db_connection()
    assert con != 0, 'DB connection failed in test_create_task.'
    cur = con.execute('SELECT * FROM tasks WHERE taskname = ?', ('TestTask',))
    task = cur.fetchone()
    con.close()
    assert task is not None

def test_get_tasks_route(client):
    rv = client.get('/get_tasks?year=2025&week=1')
    assert rv.status_code == 200
    assert b'<li' in rv.data

def test_modify_task(client):
    # Create a task
    con = get_db_connection()
    assert con != 0, 'DB connection failed in test_modify_task (insert).'
    con.execute('INSERT INTO tasks (create_date, taskname, status, priority, position, year, week) VALUES (?, ?, ?, ?, ?, ?, ?)',
                ('2025-01-01', 'ToModify', 'open', 1, 0, 2025, 1))
    taskid = con.execute('SELECT id FROM tasks WHERE taskname = ?', ('ToModify',)).fetchone()['id']
    con.commit()
    con.close()
    # Modify the task
    rv = client.get(f'/modifyTask?taskEditModal-taskid={taskid}&taskEditModal-year=2025&taskEditModal-week=1&taskEditModal-task=Modified')
    assert rv.status_code == 302
    # Check DB
    con = get_db_connection()
    assert con != 0, 'DB connection failed in test_modify_task (check).'
    task = con.execute('SELECT * FROM tasks WHERE id = ?', (taskid,)).fetchone()
    con.close()
    assert task['taskname'] == 'Modified'

def test_delete_task(client):
    con = get_db_connection()
    assert con != 0, 'DB connection failed in test_delete_task (insert).'
    con.execute('INSERT INTO tasks (create_date, taskname, status, priority, position, year, week) VALUES (?, ?, ?, ?, ?, ?, ?)',
                ('2025-01-01', 'ToDelete', 'open', 1, 0, 2025, 1))
    taskid = con.execute('SELECT id FROM tasks WHERE taskname = ?', ('ToDelete',)).fetchone()['id']
    con.commit()
    con.close()
    rv = client.get(f'/deleteTask?taskid={taskid}')
    assert rv.status_code == 200
    con = get_db_connection()
    assert con != 0, 'DB connection failed in test_delete_task (check).'
    task = con.execute('SELECT * FROM tasks WHERE id = ?', (taskid,)).fetchone()
    con.close()
    assert task['status'] == 'deleted'
