# ZenWeek Project To-Do List

This document tracks all actionable steps identified in the initial analysis and PRD review. Each item includes a status and a comment section for progress notes.

---

## Legend
- [ ] Not started
- [~] In progress
- [x] Completed

---

## MVP & Best Practices Checklist
- [x] Add .gitignore to exclude venv, DB, and sensitive files
  - _Comment: Completed 2025-09-22. .gitignore added to mask prod.sqlite3, venv, .env, and other non-relevant data._

### Immediate (MVP)
- [x] Add `requirements.txt` with Flask, python-dotenv, etc.
  - _Comment: Completed 2025-09-22. All dependencies listed._
  
- [x] Add 4–6 unit tests (DB, routes, utils)
  - _Comment: Completed 2025-09-22. 5 tests added using pytest and Flask test client; all tests pass._
  
- [x] Add docstrings and key comments in `app.py` and helpers
  - _Comment: Completed 2025-09-22. Added module, function docstrings, and key inline comments for clarity._
  
- [x] Refactor SQL queries to use parameterized queries
  - _Comment: Completed 2025-09-22. All SQL queries in app.py now use parameterized queries for security; all tests pass._
  
- [ ] Extract/organize drag-and-drop JS (move from inline in `index.html` to a separate JS file)
  - _Comment:_
  
- [ ] Add error handling for DB and user input
  - _Comment:_
  
- [ ] Add linter config (e.g., flake8 or black)
  - _Comment:_

---

## Environment Setup (Completed)
- [x] Create and activate new venv
  - _Comment: Completed 2025-09-22. venv created and activated._
- [x] Install requirements in venv
  - _Comment: Completed 2025-09-22. All packages installed._
- [x] Test if Flask app runs
  - _Comment: Completed 2025-09-22. App started successfully in new environment._

### Next Steps (Best Practices)
- [ ] Add backup/restore script for DB
  - _Comment:_
- [ ] Add weekly summary and open-task badge (stretch)
  - _Comment:_
- [ ] Add CI config for lint/test automation
  - _Comment:_
- [ ] Improve UX: auto-focus new task, consistent box sizes, etc.
  - _Comment:_
- [ ] Update README with setup/test instructions
  - _Comment:_

---

## Stretch Goals
- [ ] Automated DB backups
  - _Comment:_
- [ ] Weekly summary view (all tasks, filters)
  - _Comment:_
- [ ] Simple chart: tasks by day/week
  - _Comment:_
- [ ] Open-task badge on each week tab
  - _Comment:_
- [ ] After creating a new task, automatically enter the new task entry field again
  - _Comment:_

---

*Last updated: September 22, 2025*
