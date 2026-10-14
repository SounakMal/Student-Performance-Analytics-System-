# Student Performance Analytics System

A beginner-friendly Python data-analysis project using **Python, NumPy and Pandas**. It calculates student totals and averages, assigns grades, identifies pass/fail outcomes, analyzes subjects and departments, and exports processed reports.

> The included 20-row dataset is synthetic sample data created for demonstration. Replace it with approved data if your instructor provides a dataset.

## Features
- Loads and validates CSV student data using Pandas.
- Uses NumPy for pass/fail and attendance-status conditions.
- Uses reusable functions, loops, conditionals and DataFrame operations.
- Calculates total and average marks across four subjects.
- Assigns grades using a documented grading scale.
- Reports class statistics, pass percentage, subject averages, top five students, department summaries and grade distribution.
- Exports detailed results and a subject summary to `output/`.

## Project structure
```text
student-performance-analytics/
├── data/
│   └── students.csv
├── docs/
│   └── Project_Documentation.md
├── tests/
│   └── test_main.py
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

## Requirements
- Python 3.10 or later
- NumPy
- Pandas

## Run locally
```bash
python -m venv .venv
```
Windows:
```powershell
.venv\Scripts\Activate.ps1
```
macOS/Linux:
```bash
source .venv/bin/activate
```
Install packages and run:
```bash
python -m pip install -r requirements.txt
python main.py
```

## Rules used
- Each subject is marked out of 100.
- Total marks are the sum of four subjects (maximum 400).
- Average marks = total marks / 4.
- A student passes only if **every subject mark is at least 40**.
- Attendance of 75% or higher is labelled `Eligible`; this is an attendance flag and does not change the academic result.
- Grades: A+ (90–100), A (80–89.99), B (70–79.99), C (60–69.99), D (50–59.99), E (40–49.99), F (below 40).

## Output files
Running `main.py` creates:
- `output/student_results.csv`
- `output/subject_summary.csv`

The `output/` folder is generated locally and excluded from Git by default.

## Testing
Run:
```bash
python -m unittest discover -s tests -v
```
