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
- [x] Toggle work week / full week
  - _Comment: Completed 2025-09-22. UI toggle switch in top right allows switching between workdays (Mon-Fri) and all days (Mon-Sun); setting is persisted in localStorage._
- [x] Automated DB backups
  - _Comment: Completed 2025-09-22. Weekly auto-backup now runs at app startup if no backup exists for the current week; only last 5 are kept. Integrated with backup_restore.py._
- [x] Add backup/restore script for DB
  - _Comment: Completed 2025-09-22. backup_restore.py script added, reads DB name from .env, supports backup/list/restore, and tested successfully._
- [x] Weekly summary view (all tasks, filters)
  - _Comment: Completed 2025-09-22. Summary page added with open/overdue tasks table, weekly statistics chart, and yearly summary. Hyperlink icons display for tasks with URLs._
- [x] Simple chart: tasks by day/week
  - _Comment: Completed 2025-09-22. Chart functionality implemented in summary page with weekly statistics._
- [x] Open-task badge on each week tab
  - _Comment: Completed 2025-09-22. Color-coded Bootstrap badge shows open tasks for each week (green=current, red=past, yellow=future); badge for current week updates live on task complete/undo. Added toggle switch to show/hide all badges, state is persisted._
- [x] Fix hyperlink icons in summary page for tasks with URLs
  - _Comment: Completed 2025-09-22. Fixed backend to include URL field in summary route SQL query and task data. Hyperlink icons now properly display in "Offene & Überfällige Aufgaben" section when tasks have URLs attached._
- [x] UI improvements: Week styling and visual enhancements
  - _Comment: Completed 2025-09-23. Added clickable logo navigation, task count display in summary header, current week soft mint green background, selected week green borders, light grey borders for all weeks, and improved task badge positioning for better visual association._
- [x] Day card layout improvements
  - _Comment: Completed 2025-09-23. Aligned "Neue Aufgabe" input fields to bottom of day cards using flexbox layout. All cards now have consistent height with inputs always positioned at the bottom for better visual consistency._
- [~] Improve overall layout
- [ ] Improve Drag-N-Drop ability at the top of the list
- [ ] Improve Visual effects when hovering a task above a list
- [ ] display a mouse-over menu for fast actions
---

*Last updated: September 23, 2025*
