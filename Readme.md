# ZenWeek – Calm Weekly Planner

![MVP](https://img.shields.io/badge/status-MVP-green)

ZenWeek is a calm, intuitive weekly planner for busy people. Organize your week, move tasks with drag-and-drop, and keep your plans safe—without distractions.

---

## Vision & Objectives
ZenWeek aims to provide a clutter-free, reliable, and beginner-friendly weekly planning experience. See the [ZenWeek_PRD.md](ZenWeek_PRD.md) for full product requirements.

---

## Features (MVP)
- Add, edit, and delete tasks for each day of the week
- Drag-and-drop tasks between days and weeks
- Persistent storage with SQLite
- Simple, responsive UI (Bootstrap)
- All core logic and tests in Python/Flask
- 4–6 unit tests for reliability

---

## Getting Started
### Environment Variables
Copy the provided `.env` file and adjust as needed. The default config uses `prod.sqlite3` for production and `tst.sqlite3` for development.

Or use Flask directly:

```sh
flask run
```
Make sure your `.env` and database are set up first.


### Prerequisites
- Python 3.10+
- pip

### Installation
Clone the repository and install dependencies:

```sh
git clone https://github.com/KateiRen/ZenWeek.git
cd ZenWeek
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
```

### Database Setup
Create the SQLite database and schema:

```sh
python initdb.py
```

### Running the App

```sh
python app.py
```
Visit [http://localhost:5000](http://localhost:5000) in your browser.

---

## Usage
- **Create tasks:** Type in the input field and press Enter or click ➡️
- **Move tasks:** Drag tasks between days or weeks
- **Edit tasks:** Drag a task to the ✏️ (edit) button
- **Delete tasks:** Drag a task to the 🗑️ (delete) button
- **Mark done/undo:** Click the checkbox next to a task

---

## Testing
Tests use `pytest` and the Flask test client. All tests should pass before committing changes.

Check code style with flake8:

```sh
flake8 app.py
```
All linter warnings should be fixed before committing.

### Backup & Restore
Back up or restore your database with:

```sh
python backup_restore.py backup   # Create a timestamped backup
python backup_restore.py list     # List available backups
python backup_restore.py restore  # Restore from a selected backup
```
The script reads the DB name from `.env`.

Run all unit tests with:

```sh
pytest
```

---

## Contributing
### Continuous Integration
All pushes and pull requests are checked by GitHub Actions for lint and test status. See `.github/workflows/ci.yml`.
Contributions are welcome! Please see the [To-Do.md](To-Do.md) for open tasks and improvement ideas. Open issues or submit pull requests for discussion.

---

## License
GNU GPLv3 – see [LICENSE](LICENSE) for details.

---

## Project Status
See [InitialAnalysis.md](InitialAnalysis.md) and [To-Do.md](To-Do.md) for current progress and next steps.

