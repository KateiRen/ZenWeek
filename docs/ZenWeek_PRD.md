# ZenWeek Product Requirements Document (PRD)

## 1. Vision & Objectives
ZenWeek aims to provide a calm, intuitive weekly planner that helps busy people organize tasks with minimal friction. The MVP focuses on reliability, maintainability, and a clutter-free experience.

## 2. User Stories
- As a busy professional, I want to add and move tasks across my week so that I can adapt to changing priorities.
- As a freelancer, I want my tasks to be saved automatically so that I never lose my plans.
- As a new contributor, I want clear code and basic tests so that I can confidently improve the app.
- As a student, I want to see all my weekly tasks at a glance so that I can plan my workload.

## 3. Feature List
**MVP:**
- The existing project already can add, edit, and delete tasks for each day of the week and drag-and-drop tasks between days
- Analyze the existing code and suggest improvements
- Improve functionality of the drag-and-drop feature
- Persistent storage using SQLite database
- Basic code documentation and 4–6 unit tests

**Stretch Goals:**
- Automated DB backups
- Weekly summary view (all tasks, filters)
- Simple chart: tasks by day/week
- Open-task badge on each week tab
- after creating a new task automatically enter the new task entry field again

## 4. Success Metrics
- MVP shipped in under 1 hour
- All core features work without errors
- Codebase passes all tests and lints cleanly
- At least 1 new contributor can set up and run tests in <10 min

## 5. Constraints or Assumptions
- Data stored in SQLite DB
- No synchronisation to cloud/other devices
- No authentication or external APIs
- Single-page app, minimal dependencies
- Designed for beginner-friendly code and rapid iteration