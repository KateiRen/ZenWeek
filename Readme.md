
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
Run all unit tests with:

```sh
pytest
```

---

## Contributing
Contributions are welcome! Please see the [To-Do.md](To-Do.md) for open tasks and improvement ideas. Open issues or submit pull requests for discussion.

---

## License
GNU GPLv3 – see [LICENSE](LICENSE) for details.

---

## Project Status
See [InitialAnalysis.md](InitialAnalysis.md) and [To-Do.md](To-Do.md) for current progress and next steps.

