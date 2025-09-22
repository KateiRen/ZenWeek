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
  
- [x] Extract/organize drag-and-drop JS (move from inline in `index.html` to a separate JS file)
  - _Comment: Completed 2025-09-22. All drag-and-drop and task JS logic modularized into static/dragdrop.js; index.html updated to reference it. Tests pass and integration verified._
  
- [x] Add error handling for DB and user input
  - _Comment: Completed 2025-09-22. Added try/except blocks and user feedback for all DB operations and user input in app.py. All tests pass._
  
- [x] Add linter config (e.g., flake8 or black)
  - _Comment: Completed 2025-09-22. .flake8 config added, flake8 installed, and all linter warnings in app.py fixed._

---

## Environment Setup (Completed)
- [x] Create and activate new venv
  - _Comment: Completed 2025-09-22. venv created and activated._
- [x] Install requirements in venv
  - _Comment: Completed 2025-09-22. All packages installed._
- [x] Test if Flask app runs
  - _Comment: Completed 2025-09-22. App started successfully in new environment._

### Next Steps (Best Practices)
- [x] Add CI config for lint/test automation
  - _Comment: Completed 2025-09-22. GitHub Actions workflow added to run flake8 and pytest on push/PR to main branch._
- [x] Improve UX: auto-focus new task, consistent box sizes, etc.
  - _Comment: Completed 2025-09-22. Auto-focus returns to the last used input field after task creation; card heights are dynamically matched per visual row for consistent layout._
- [x] Update README with setup/test instructions
  - _Comment: Completed 2025-09-22. README now includes setup, environment, linting, backup/restore, and CI instructions for new developers._

---

## Stretch Goals
  - _Comment: Completed 2025-09-22. UI toggle switch in top right allows switching between workdays (Mon-Fri) and all days (Mon-Sun); setting is persisted in localStorage._
  - _Comment:_
  - _Comment: Completed 2025-09-22. backup_restore.py script added, reads DB name from .env, supports backup/list/restore, and tested successfully._
  - _Comment:_
  - _Comment:_
  - _Comment:_
  - _Comment:_

---

*Last updated: September 22, 2025*
